from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.chat import router

app = FastAPI(title="LangChain Chat API with Chat, Doc Vector DB, Memory, and Opik")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
