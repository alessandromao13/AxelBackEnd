import os
import uuid

import pdfplumber
from pathlib import Path

from langchain.retrievers import MultiVectorRetriever
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.stores import InMemoryStore
from unstructured.partition.pdf import partition_pdf


from langchain.embeddings.base import Embeddings
import requests

from src.llm.ollama_embeddings import OllamaEmbeddings
from src.llm.ollama_prod import OllamaProdLLM



def extract_tables_with_pdfplumber(content_path, file_to_read):
    # Convert to Path object
    full_path = Path(content_path) / file_to_read
    print(f"Reading from: {full_path} using pdfplumber")
    got_tables = []
    try:
        with pdfplumber.open(full_path) as pdf:  # Ensure full_path is a valid Path object
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                if page_tables:
                    got_tables.extend(page_tables)
                    print(f"Found {len(page_tables)} tables on page {page_num + 1}")
    except Exception as e:
        print(f"An error occurred while extracting tables: {e}")

    return got_tables


def doc_partition(content_path, file_to_read):
    full_path = os.path.join(content_path, file_to_read)
    print(f"Reading from: {full_path}")

    try:
        raw_pdf_elems = partition_pdf(filename=full_path)

    except Exception as e:
        print(f"An error occurred while partitioning the PDF: {e}")
        return []

    return raw_pdf_elems


def data_category(raw_pdf_elems):
    data_tables = []
    data_texts = []

    for element in raw_pdf_elems:
        print(f"Processing element of type: {element.__class__.__name__}")

        element_type = element.__class__.__name__

        if element_type == "Table":
            data_tables.append(str(element))
        elif element_type in ["Text", "NarrativeText", "CompositeElement", "ListItem"]:
            data_texts.append(str(element))
        elif element_type == "Title":
            data_texts.append(str(element))
        else:
            print(f"Skipping unknown element type: {element_type}")

    return data_texts, data_tables


def tables_summarize(data_cat):
    prompt_text = ("You are an assistant tasked with summarizing tables. Give a concise summary of the table. "
                   "Table chunk: {element}")
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = OllamaProdLLM()
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
    produced_table_summaries = summarize_chain.batch(data_cat, {"max_concurrency": 5})
    return produced_table_summaries


if __name__ == '__main__':
    path = "./"
    file_name = "Temporizzatori.pdf"
    print("EXTRACTING RAW ELEMENTS")
    raw_pdf_elements = doc_partition(path, file_name)
    texts, _ = data_category(raw_pdf_elements)
    print("TEXTS:", texts)
    tables = extract_tables_with_pdfplumber(path, file_name)
    print("TABLES:", tables)
    table_summaries = tables_summarize(tables)
    chroma_persistence_path = "/home/alessandroaw/Desktop/chroma_store"
    print("Creating vectorstore")
    vectorstore = Chroma(collection_name="multi_modal_rag",
                         embedding_function=OllamaEmbeddings(),
                         persist_directory=chroma_persistence_path)

    store = InMemoryStore()
    id_key = "doc_id"
    print("Creating retriever")
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key=id_key)

    print("+++++ Adding text")
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(texts)
    ]
    print("Adding document")
    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(doc_ids, texts)))

    print("++++ Adding tables")

    # Add tables
    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_tables = [
        Document(page_content=s, metadata={id_key: table_ids[i]})
        for i, s in enumerate(table_summaries)
    ]
    print("Adding document")
    retriever.vectorstore.add_documents(summary_tables)
    retriever.docstore.mset(list(zip(table_ids, tables)))

    print("Persisting")
    vectorstore.persist()
    print("DONE")

