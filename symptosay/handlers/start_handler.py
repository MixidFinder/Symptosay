import logging
from http import HTTPStatus

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
async def send_welcome(message: Message) -> None:
    logger.info("Пользователь %s запустил бота.", message.from_user.username)
    await message.reply(
        "Привет! Нажми кнопку 'Старт', чтобы зарегистрироваться.",
        reply_markup=get_start_keyboard(),
    )


@start_router.message(F.text == "Старт")
async def process_start_button(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    user_data = {"user_id": user_id, "username": username}

    logger.info("Пользователь %s нажал кнопку 'Старт'.", user_id)

    try:
        async with httpx.AsyncClient() as client:
            logger.info("Отправка запроса к %s/auth для пользователя %s.", USER_SERVICE_URL, user_id)
            response = await client.post(f"{USER_SERVICE_URL}/auth", json=user_data)

            if response.status_code == HTTPStatus.OK:
                logger.info("Пользователь %s успешно зарегистрирован.", user_id)
                await message.reply("Вы успешно зарегистрированы!")
            else:
                logger.error(
                    "Ошибка при регистрации пользователя %s. Статус код: %s, Ответ: %s",
                    user_id,
                    response.status_code,
                    response.text,
                )
                await message.reply("Произошла ошибка при регистрации. Попробуйте позже.")
    except httpx.RequestError:
        logger.exception("Не удалось подключиться к серверу для пользователя %s", user_id)
        await message.reply("Не удалось подключиться к серверу. Попробуйте позже.")
