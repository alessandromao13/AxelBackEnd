from typing import Optional
from fastapi import APIRouter, Body
from src.services.chat import execute_chat_system
from src.persistence.mongoDB import get_graph_by_id, get_graph_by_user_id, get_user_threads
from tests.dev.graph_generation_manager import run_graph_generation_system

router = APIRouter()


# 1. The user generates a KG --> generate graph
@router.post("/generate-graph/{user_id}")
def generate_graph(user_id: str, input_text: str = Body(...), topic: str = Body(...), summary: str = Body(...)):
    print(f"GOT topic {topic}, summary {summary}")
    #  fixme: generate_kg uses transformer, run_graph_generation_system uses llama
    # generate_kg(input_text, user_id, topic, summary)
    print("GENERATE GRAPH ENDPOINT GOT", input_text, user_id, topic, summary)
    run_graph_generation_system(input_text, user_id, topic, summary)
    return "OK"


# 2. The user wants to see / interact / chat with the kg --> get graph by graph id
@router.get("/get-graph-by-id/{graph_id}")
def get_graph_by_graph_id(graph_id: str):
    return get_graph_by_id(graph_id)


# 3. The user opens the chat or the gallery --> get graphs by user id

@router.get("/get-graph-by-user-id/{user_id}")
def get_graph_by_users_id(user_id):
    return get_graph_by_user_id(user_id)

