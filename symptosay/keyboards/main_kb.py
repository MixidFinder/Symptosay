from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_main_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="Записать симптом"))
    keyboard.add(KeyboardButton(text="Удалить симптом"))
    keyboard.add(KeyboardButton(text="Обновить симптом"))

    if is_admin:
        keyboard.row(KeyboardButton(text="Админ панель"))

    return keyboard.as_markup(resize_keyboard=True)


def get_nav_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Главная")
    builder.button(text="Назад")
    return builder.as_markup(resize_keyboard=True)
