import logging
from http import HTTPStatus

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from keyboards.main_kb import get_main_kb

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

main_router = Router()
