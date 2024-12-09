import opik
from opik.integrations.langchain import OpikTracer

from src.config import OPIK_API_KEY, OPIK_WORKSPACE, OPIK_PROJECT_NAME
from src.utils import logger

opik.configure(use_local=False, api_key=OPIK_API_KEY, workspace=OPIK_WORKSPACE)
opik_tracer = OpikTracer(tags=["production-chat"], project_name=OPIK_PROJECT_NAME)
logger.info("Opik configured")
