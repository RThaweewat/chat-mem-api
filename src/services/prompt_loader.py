import opik
import yaml

from src.config import OPIK_API_KEY
from src.utils import log_success

if OPIK_API_KEY is None:
    def load_prompts(path: str = "src/prompts/prompts.yaml"):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        log_success("Prompts loaded successfully")
        return data

client = opik.Opik()
prompt = client.get_prompt(name="main_prompt")
formatted_prompt = prompt.format()
log_success("Prompt loaded successfully")
