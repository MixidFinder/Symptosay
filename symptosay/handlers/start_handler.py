import logging

import httpx
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

from keyboards.start_keyboard import get_start_keyboard

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

start_router = Router()

USER_SERVICE_URL = "http://user_service:8000"


@start_router.message(Command("start"))
async def send_welcome(message: Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота.")
    await message.reply(
        "Привет! Нажми кнопку 'Старт', чтобы зарегистрироваться.",
        reply_markup=get_start_keyboard(),
    )


@start_router.message(F.text == "Старт")
async def process_start_button(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_data = {"user_id": user_id, "username": username}

    logger.info(f"Пользователь {user_id} ({username}) нажал кнопку 'Старт'.")

    try:
        async with httpx.AsyncClient() as client:
            logger.info(
                f"Отправка запроса к {USER_SERVICE_URL}/auth для пользователя {user_id}."
            )
            response = await client.post(f"{USER_SERVICE_URL}/auth", json=user_data)

            if response.status_code == 200:
                logger.info(f"Пользователь {user_id} успешно зарегистрирован.")
                await message.reply("Вы успешно зарегистрированы!")
            else:
                logger.error(
                    f"Ошибка при регистрации пользователя {user_id}. "
                    f"Статус код: {response.status_code}, Ответ: {response.text}"
                )
                await message.reply(
                    "Произошла ошибка при регистрации. Попробуйте позже."
                )
    except httpx.RequestError as e:
        logger.error(
            f"Не удалось подключиться к серверу для пользователя {user_id}: {e}"
        )
        await message.reply("Не удалось подключиться к серверу. Попробуйте позже.")
