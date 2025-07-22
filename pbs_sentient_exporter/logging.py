
from logging import Logger, StreamHandler, getLogger
from typing import Literal

LogLevel = Literal["error"] | Literal["warning"] | Literal["info"] | Literal["debug"]

DEFAULT_LOG_LEVEL: LogLevel = "warning"


def get_logger(name: str, level: LogLevel = DEFAULT_LOG_LEVEL) -> Logger:
    logger = getLogger(name)
    logger.setLevel(level.upper())
    if not logger.handlers:
        logger.addHandler(StreamHandler())
    return logger
