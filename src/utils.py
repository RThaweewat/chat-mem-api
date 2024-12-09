import os

from loguru import logger

os.makedirs("logs", exist_ok=True)
logger.add("logs/logs.log", rotation="1 week")
logger.add("logs/error.log", rotation="1 week", level="ERROR", filter=lambda record: record["level"].name == "ERROR")


def log_info(message: str):
    logger.info(message)


def log_error(message: str):
    logger.error(message)


def log_success(message: str):
    logger.success(message)


def log_warning(message: str):
    logger.warning(message)
