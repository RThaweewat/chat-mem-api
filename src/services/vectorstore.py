import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from src.config import OPENAI_API_KEY

os.makedirs("data/chroma", exist_ok=True)
persist_dir = "data/chroma"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                              model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="data/chroma"
)
