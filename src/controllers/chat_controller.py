from typing import Optional
from fastapi import APIRouter, Body
from src.services.chat import execute_chat_system
router = APIRouter()


@router.post("/chat/{user_id}")
def chat(user_id: str, user_query: str = Body(...), graph_id: str = Body(...), thread_id: Optional[str] = Body(None)):
    return execute_chat_system(user_query, user_id, graph_id, thread_id)


