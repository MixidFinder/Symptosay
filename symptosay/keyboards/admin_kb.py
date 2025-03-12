from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="Добавить симптомы в бд"))
    keyboard.add(KeyboardButton(text="Добавить болезни в бд"))
    keyboard.add(KeyboardButton(text="Удалить симптомы из бд"))
    keyboard.add(KeyboardButton(text="Удалить болезни из бд"))
    keyboard.add(KeyboardButton(text="Обновить симптом в бд"))
    keyboard.add(KeyboardButton(text="Обновить болезнь в бд"))
    keyboard.add(KeyboardButton(text="Добавить админа"))
    keyboard.add(KeyboardButton(text="Удалить админа"))
    keyboard.row(KeyboardButton(text="Назад"))

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)


def admin_toggle_keyboard():
    buttons = [
        InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin"),
        InlineKeyboardButton(text="Удалить администратора", callback_data="remove_admin"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
