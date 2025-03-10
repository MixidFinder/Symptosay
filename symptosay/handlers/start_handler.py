import logging
import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from keyboards.main_kb import get_main_kb
from services import user_service

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

start_router = Router()


@start_router.message(Command("start"))
async def send_welcome(message: Message) -> None:
    # TODO: process None
    user_id = message.from_user.id
    username = message.from_user.username
    new_user = {"user_id": user_id, "username": username, "is_admin": False}
    admins = os.getenv("ADMINS", "").split(",")

    if str(user_id) in admins:
        new_user["is_admin"] = True

    user_data = await user_service.get_user_by_id(user_id)

    if user_data:
        await message.reply("Перезапущен", reply_markup=await get_main_kb(new_user["user_id"]))
    else:
        response = await user_service.register_user(new_user)
        if response:
            await message.reply(
                "Привет! Это бот по отслеживанию симптомов. Если тебе нужна помощь по боту, нажми кнопку 'Помощь'",
                reply_markup=await get_main_kb(bool(new_user["is_admin"])),
            )
        else:
            await message.reply("Не удалось подключиться к серверу. Попробуйте позже.")
