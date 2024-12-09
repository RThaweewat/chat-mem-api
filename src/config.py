import os
from dotenv import load_dotenv
from src.utils import log_success

load_dotenv()
log_success("Environment variables loaded successfully")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
OPIK_WORKSPACE = os.getenv("OPIK_WORKSPACE")
OPIK_PROJECT_NAME = os.getenv("OPIK_PROJECT_NAME")
OPIK_API_KEY = os.getenv("OPIK_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set.")
