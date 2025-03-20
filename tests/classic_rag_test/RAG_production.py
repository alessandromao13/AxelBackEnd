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
    path = '../../assets/pdf/1234/ChatGPT_A_brief_narrative_review.pdf'
    # print(f"Reading from: {full_path} using pdfplumber")
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


def manage_rag_production(user_id, file_name):
    path = f"../../assets/pdf/{user_id}"
    raw_pdf_elements = doc_partition(path, file_name)
    print("GOT RAW ELEMS", raw_pdf_elements)
    texts, _ = data_category(raw_pdf_elements)
    print("GOT TEXT", texts)
    tables = extract_tables_with_pdfplumber(path, file_name)
    print("GOT TABLES", tables)
    table_summaries = tables_summarize(tables)
    rag_id = str(uuid.uuid4())
    print("CHECKING PERSISTENCE PATH")
    chroma_persistence_path = f"/home/alessandroaw/Desktop/RAG/{user_id}/chroma_store_{rag_id}"
    if not os.path.exists(chroma_persistence_path):
        os.makedirs(chroma_persistence_path)
        print(f"Directory '{chroma_persistence_path}' created.")
    else:
        print(f"Directory '{chroma_persistence_path}' already exists.")
    print("GENERATING VECTOR STORE")
    vectorstore = Chroma(collection_name="multi_modal_rag",
                         embedding_function=OllamaEmbeddings(),
                         persist_directory=chroma_persistence_path)

    store = InMemoryStore()
    id_key = "doc_id"
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key=id_key)
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(texts)
    ]
    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(doc_ids, texts)))
    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_tables = [
        Document(page_content=s, metadata={id_key: table_ids[i]})
        for i, s in enumerate(table_summaries)
    ]
    retriever.vectorstore.add_documents(summary_tables)
    retriever.docstore.mset(list(zip(table_ids, tables)))
    print("PERSIST")
    vectorstore.persist()
    print("ALL GOOD")
    return 200


# fixme --> I can eventually save metadata and reconstruct the ChromaStore later
# def manage_rag_production(user_id, file_name):
#     path = f"../../assets/pdf/{user_id}"
#     raw_pdf_elements = doc_partition(path, file_name)
#     texts, _ = data_category(raw_pdf_elements)
#     tables = extract_tables_with_pdfplumber(path, file_name)
#     table_summaries = tables_summarize(tables)
#     rag_id = str(uuid.uuid4())
#
#     chroma_persistence_path = f"/home/alessandroaw/Desktop/RAG/{user_id}/chroma_store_{rag_id}"
#     if not os.path.exists(chroma_persistence_path):
#         os.makedirs(chroma_persistence_path)
#
#     vectorstore = Chroma(collection_name="multi_modal_rag",
#                          embedding_function=OllamaEmbeddings(),
#                          persist_directory=chroma_persistence_path)
#
#     store = InMemoryStore()
#     id_key = "doc_id"
#     retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key=id_key)
#
#     doc_ids = [str(uuid.uuid4()) for _ in texts]
#     summary_texts = [Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(texts)]
#     retriever.vectorstore.add_documents(summary_texts)
#     retriever.docstore.mset(list(zip(doc_ids, texts)))
#
#     table_ids = [str(uuid.uuid4()) for _ in tables]
#     summary_tables = [Document(page_content=s, metadata={id_key: table_ids[i]}) for i, s in enumerate(table_summaries)]
#     retriever.vectorstore.add_documents(summary_tables)
#     retriever.docstore.mset(list(zip(table_ids, tables)))
#
#     # Save data into MongoDB
#     for doc, doc_id in zip(summary_texts, doc_ids):
#         vector_data = retriever.vectorstore.get_vector(doc)
#         vector_collection.insert_one({
#             "user_id": user_id,
#             "doc_id": doc_id,
#             "text": doc.page_content,
#             "embedding": vector_data
#         })
#
#     # Optionally, store document metadata in MongoDB
#     for table, table_id in zip(summary_tables, table_ids):
#         table_data = retriever.vectorstore.get_vector(table)
#         document_collection.insert_one({
#             "user_id": user_id,
#             "table_id": table_id,
#             "table_content": table.page_content,
#             "embedding": table_data
#         })
#
#     return "OK"

# def load_chroma_from_mongo(user_id):
#     # Load documents and embeddings from MongoDB
#     vectors = vector_collection.find({"user_id": user_id})
#     documents = document_collection.find({"user_id": user_id})
#
#     vectorstore = Chroma(collection_name="multi_modal_rag",
#                          embedding_function=OllamaEmbeddings(),
#                          persist_directory=None)  # In-memory store
#
#     docstore = InMemoryStore()
#
#     for vector in vectors:
#         # Reconstruct documents and embeddings in Chroma
#         doc = Document(page_content=vector['text'], metadata={"doc_id": vector['doc_id']})
#         vectorstore.add_documents([doc])
#         docstore.mset([(vector['doc_id'], vector['text'])])
#
#     return vectorstore

if __name__ == '__main__':
    path = "./"
    file_name = "ChatGPT_A_brief_narrative_review.pdf"
    print("EXTRACTING RAW ELEMENTS")
    raw_pdf_elements = doc_partition(path, file_name)
    texts, _ = data_category(raw_pdf_elements)
    print("TEXTS:", texts)
    # tables = extract_tables_with_pdfplumber(path, file_name)
    # print("TABLES:", tables)
    # table_summaries = tables_summarize(tables)
    # chroma_persistence_path = "/home/alessandroaw/Desktop/chroma_store"
    # print("Creating vectorstore")
    # vectorstore = Chroma(collection_name="multi_modal_rag",
    #                      embedding_function=OllamaEmbeddings(),
    #                      persist_directory=chroma_persistence_path)
    #
    # store = InMemoryStore()
    # id_key = "doc_id"
    # print("Creating retriever")
    # retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key=id_key)
    #
    # print("+++++ Adding text")
    # doc_ids = [str(uuid.uuid4()) for _ in texts]
    # summary_texts = [
    #     Document(page_content=s, metadata={id_key: doc_ids[i]})
    #     for i, s in enumerate(texts)
    # ]
    # print("Adding document")
    # retriever.vectorstore.add_documents(summary_texts)
    # retriever.docstore.mset(list(zip(doc_ids, texts)))
    #
    # print("++++ Adding tables")
    #
    # # Add tables
    # table_ids = [str(uuid.uuid4()) for _ in tables]
    # summary_tables = [
    #     Document(page_content=s, metadata={id_key: table_ids[i]})
    #     for i, s in enumerate(table_summaries)
    # ]
    # print("Adding document")
    # retriever.vectorstore.add_documents(summary_tables)
    # retriever.docstore.mset(list(zip(table_ids, tables)))
    #
    # print("Persisting")
    # vectorstore.persist()
    # print("DONE")

