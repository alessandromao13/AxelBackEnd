from typing import Optional
from fastapi import APIRouter, Body

from src.persistence.mongoDB import count_thread_id, remove_thread_by_id
from src.services.chat import execute_chat_system, execute_chat_system_pdf

router = APIRouter()


@router.post("/chat/{user_id}")
def chat(user_id: str, user_query: str = Body(...), graph_id: str = Body(...), rag_id: str = Body(...), thread_id: Optional[str] = Body(None)):
    # print("++ CHAT GOT GRAPH ID", graph_id)
    # print("++ CHAT GOT RAG ID", rag_id)
    # print("++ CHAT GOT USE QUERY", user_query)
    # print("++ CHAT GOT THREAD ID", thread_id)
    if rag_id:
        # print(f"++ Executing chat system with RAG {rag_id}")
        llm_res = execute_chat_system_pdf(user_query, user_id, rag_id, thread_id)

    else:
        # a rag_id was passed
        # print(f"++ Executing chat system with GRAPH {graph_id}")
        llm_res = execute_chat_system(user_query, user_id, graph_id, thread_id)

    return llm_res


@router.post("/chat-document/{user_id}")
def chat(user_id: str, user_query: str = Body(...), rag_id: str = Body(...), thread_id: Optional[str] = Body(None)):
    print("++ CHAT GOT GRAPH ID", rag_id)
    print("++ CHAT GOT RAG ID", thread_id)
    print("++ CHAT GOT USE QUERY", user_query)
    print("++ CHAT GOT THREAD ID", thread_id)
    return execute_chat_system_pdf(user_query, user_id, rag_id, thread_id)


@router.get("/new-thread")
def new_thread():
    return str(count_thread_id())


@router.get("/delete-thread/{thread_id}")
def delete_thread(thread_id: str):
    remove_thread_by_id(thread_id)

