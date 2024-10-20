from fastapi import APIRouter
from src.controllers import graphs_controller, threads_controller, chat_controller

api_router = APIRouter()
api_router.include_router(graphs_controller.router, tags=["graphs"])
api_router.include_router(threads_controller.router, tags=["threads"])
api_router.include_router(chat_controller.router, tags=["chats"])
