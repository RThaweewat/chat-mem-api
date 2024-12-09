import os
import shutil
import uuid
from uuid import uuid4

import textract
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.services.vectorstore import vectorstore
from src.utils import log_info

os.makedirs("data/uploaded_docs", exist_ok=True)


def extract_text(file_path: str) -> str:
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text: {e}")


def process_and_store_docs(files):
    processed_docs = []
    for f in files:
        file_id = str(uuid.uuid4())
        file_ext = f.filename.split(".")[-1]
        file_path = f"data/uploaded_docs/{file_id}.{file_ext}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)

        log_info(f"Extracting text from file: {file_path}")
        text = extract_text(file_path)

        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=2000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_text(text)
        docs = [Document(page_content=chunk, metadata={"source": f.filename}) for chunk in chunks]

        # Add docs to vectorstore
        vectorstore.add_documents(docs, ids=[str(uuid4()) for _ in docs])
        processed_docs.append({"file_id": file_id, "filename": f.filename, "num_docs": len(docs)})
    return processed_docs
