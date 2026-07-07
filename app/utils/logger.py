"""Logging utilities."""
import sys

from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> | "
           "<level>{level}</level> | "
           "{message}",
    level="INFO"
)


def get_logger():
    return logger