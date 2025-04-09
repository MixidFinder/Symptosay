import logging
import os

from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())


def get_admins() -> list[int]:
    return list(map(int, os.getenv("ADMINS", "").split(",")))
