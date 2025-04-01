from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_kb import get_main_kb

start_router = Router()


@start_router.message(Command("start"))
async def send_welcome(message: Message, user_data: dict[str, Any]) -> None:
    username = message.from_user.username
    if not username:
        await message.reply(
            "У вас не настроен юзернейм в телеграме, установите его в настройках что бы иметь возможность пользоваться ботом"
        )
        return

    await message.reply(
        "Привет! Это бот по отслеживанию симптомов. Если тебе нужна помощь по боту, нажми кнопку 'Помощь'",
        reply_markup=get_main_kb(is_admin=user_data["is_admin"]),
    )
