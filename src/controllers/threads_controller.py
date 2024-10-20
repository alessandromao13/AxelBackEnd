from fastapi import APIRouter
from src.persistence.mongoDB import get_threads_by_user_id

router = APIRouter()


@router.get("/get-threads-by-user-id/{user_id}")
def get_user_threads(user_id: str):
    return get_threads_by_user_id(user_id)


# todo verificare se questa e' duplicata /\ --> se si eliminare
# @router.get("/get-graph-by-user-id/{user_id}")
# def get_threads_by_user_id(user_id: str):
#     return get_user_threads(user_id)

