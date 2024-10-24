import os
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form, Body
from src.rag_dev.RAG_production import manage_rag_production
from src.persistence.mongoDB import get_graph_by_id, get_graph_by_user_id, get_user_threads, get_rags_by_user_id, \
    get_document_by_document_id, delete_document_by_document_id
from tests.dev.graph_generation_manager import run_graph_generation_system

load_dotenv()

PDF_DIRECTORY = os.getenv('PDF_DIRECTORY')
router = APIRouter()


@router.post("/generate-graph/{user_id}")
def generate_graph(user_id: str, input_text: str = Body(...), topic: str = Body(...), summary: str = Body(...)):
    # print(f"GOT topic {topic}, summary {summary}")
    # fixme: generate_kg uses transformer, run_graph_generation_system uses llama
    # generate_kg(input_text, user_id, topic, summary)
    run_graph_generation_system(input_text, user_id, topic, summary)
    return "OK"


@router.get("/get-graph-by-id/{graph_id}")
def get_graph_by_graph_id(graph_id: str):
    return get_graph_by_id(graph_id)


@router.get("/get-graph-by-user-id/{user_id}")
def get_graph_by_users_id(user_id):
    return get_graph_by_user_id(user_id)


@router.post("/generate-rag-pdf/{user_id}")
async def generate_graph(user_id: str, uploaded_file: UploadFile = File(...), topic: str = Form(...), summary: str = Form(...)):
    await manage_user_data(user_id, uploaded_file)
    return await manage_rag_production(user_id, uploaded_file)


@router.get("/user-rags/{user_id}")
def get_user_rags(user_id: str):
    got_user_docs = get_rags_by_user_id(user_id)
    return got_user_docs


@router.get("/get-user-document/{user_id}/{document_id}")
def get_user_rags(user_id: str, document_id: str):
    print("GOT REQUEST FOR PDF", document_id)
    got_user_pdf = get_document_by_document_id(document_id, user_id)
    print("GOT USER PDF", got_user_pdf)
    return got_user_pdf


@router.get("/delete-user-document/{user_id}/{document_id}")
def delete_user_document(user_id: str, document_id: str):
    print("GOT REQUEST FOR PDF", document_id)
    return delete_document_by_document_id(document_id, user_id)


async def manage_user_data(user_id: str, uploaded_file: UploadFile):
    """
    Saves the pdf to user's directory
    """
    directory_path = os.path.join(f"../assets/{PDF_DIRECTORY}", user_id)
    os.makedirs(directory_path, exist_ok=True)
    file_location = os.path.join(directory_path, uploaded_file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await uploaded_file.read())

