import logging
import os

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from keyboards.main_kb import get_main_kb
from services import user_service

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

start_router = Router()

USER_SERVICE_URL = "http://user_service:8000/api"


@start_router.message(Command("start"))
async def send_welcome(message: Message) -> None:
    # TODO: process None
    logger.info("Пользователь %s запустил бота", message.from_user.username)

    # TODO: process None
    user_id = message.from_user.id
    username = message.from_user.username
    user_data = {"user_id": user_id, "username": username, "is_admin": False}
    admins = os.getenv("ADMINS", "").split(",")
    if str(user_id) in admins:
        user_data["is_admin"] = True

    user_data = await user_service.get_user_by_id(user_id)
    if user_data:
        logger.info("Пользователь %s уже зарегестрирован. Сброс клавиатуры", user_id)
        await message.reply("Перезапущен.", reply_markup=get_main_kb(bool(user_data["is_admin"])))
    else:
        response = await user_service.register_user(user_data)
        if response == httpx.codes.CREATED:
            await message.reply(
                "Привет! Это бот по отслеживанию симптомов. Если тебе нужна помощь по боту, нажми кнопку 'Помощь'",
                reply_markup=get_main_kb(bool(user_data["is_admin"])),
            )
        else:
            await message.reply("Не удалось подключиться к серверу. Попробуйте позже.")
