from langchain_core.runnables import RunnableParallel
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.storage import InMemoryStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from src.llm.ollama_chat import OllamaChatLLM
from src.llm.ollama_embeddings import OllamaEmbeddings


def generate_rag_bot(user_id, rag_id):
    chroma_persistence_path = f"/home/alessandroaw/Desktop/RAG/{user_id}/chroma_store_{rag_id}"
    vectorstore = Chroma(collection_name="multi_modal_rag",
                         embedding_function=OllamaEmbeddings(),
                         persist_directory=chroma_persistence_path)

    # todo --> Check if this does anything, remove in case it does not
    store = InMemoryStore()
    id_key = "doc_id"
    retriever_test = vectorstore.as_retriever()
    model = OllamaChatLLM()

    prompt_str = """Answer the question below using the context:
        Context: {context}
        Question: {question}
        Answer: """
    prompt = ChatPromptTemplate.from_template(prompt_str)

    retrieval = RunnableParallel(
        {"context": retriever_test, "question": RunnablePassthrough()}
    )

    chain = retrieval | prompt | model | StrOutputParser()
    return chain


# if __name__ == '__main__':
#     chroma_persistence_path = "/home/alessandroaw/Desktop/chroma_store"
#     vectorstore = Chroma(collection_name="multi_modal_rag",
#                          embedding_function=OllamaEmbeddings(),
#                          persist_directory=chroma_persistence_path)
#     store = InMemoryStore()
#     id_key = "doc_id"
#     retriever_test = vectorstore.as_retriever()
#     model = OllamaChatLLM()
#
#     prompt_str = """Answer the question below using the context:
#     Context: {context}
#     Question: {question}
#     Answer: """
#     prompt = ChatPromptTemplate.from_template(prompt_str)
#
#     retrieval = RunnableParallel(
#         {"context": retriever_test, "question": RunnablePassthrough()}
#     )
#
#     chain = retrieval | prompt | model | StrOutputParser()
#
#     while True:
#         print("Ask something..")
#         user_input = input()
#         print("BOT:", chain.invoke(user_input))

