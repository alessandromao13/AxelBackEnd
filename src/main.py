import uvicorn
from fastapi import FastAPI
from controllers.base import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
