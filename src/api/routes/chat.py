from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Query
from pydantic import BaseModel, Field

from src.services.document_loader import process_and_store_docs
from src.services.llm import handle_chat, reset_conversation
from src.services.vectorstore import vectorstore

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    metadata: dict = Field(default_factory=dict)


class UploadDocsResponse(BaseModel):
    status: str
    processed_docs: List[dict]


@router.post("/upload-docs", response_model=UploadDocsResponse)
def upload_docs(files: List[UploadFile] = File(...)):
    processed_docs = process_and_store_docs(files)
    return UploadDocsResponse(status="ok", processed_docs=processed_docs)


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    thread_id = request.thread_id or "default_thread"
    answer = handle_chat(request.query, thread_id=thread_id)
    return ChatResponse(answer=answer, metadata={})


@router.post("/reset")
def reset_chat(thread_id: str = Query("default_thread")):
    reset_conversation(thread_id)
    return {"status": "conversation reset"}


@router.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


@router.post("/reset-db")
def reset_db():
    all_docs = vectorstore._collection.get()
    all_ids = all_docs["ids"]
    if all_ids is not None:
        for doc_id in all_ids:
            vectorstore._collection.delete(doc_id)
        return {"status": "vectorstore reset successfully"}
    else:
        # return that db already emtry
        return {"status": "vectorstore is already empty"}
