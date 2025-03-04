import logging
from http import HTTPStatus

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from keyboards.main_keyboard import get_main_kb

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

start_router = Router()

USER_SERVICE_URL = "http://user_service:8000"


@start_router.message(Command("start"))
async def send_welcome(message: Message) -> None:
    # TODO: process None
    logger.info("Пользователь %s запустил бота", message.from_user.username)

    # TODO: process None
    user_id = message.from_user.id
    username = message.from_user.username
    user_data = {"user_id": user_id, "username": username}

    try:
        async with httpx.AsyncClient() as session:
            # TODO: change endpoint
            logger.info("Отправка запроса к %s/auth для пользователя %s", USER_SERVICE_URL, user_id)
            response = await session.post(f"{USER_SERVICE_URL}/auth", json=user_data)

            is_admin = response.json().get("is_admin")

            if response.status_code == HTTPStatus.CREATED:
                logger.info("Пользователь %s успешно зарегистрирован", user_id)
                await message.reply(
                    "Привет! Это бот по отслеживанию симптомов. Если тебе нужна помощь по боту, нажми кнопку 'Помощь'",
                    reply_markup=get_main_kb(is_admin),
                )
            elif response.status_code == HTTPStatus.OK:
                logger.info("Пользователь %s уже зарегестрирован. Сброс клавиатуры", user_id)
                await message.reply("Перезапущен.", reply_markup=get_main_kb(is_admin))
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
