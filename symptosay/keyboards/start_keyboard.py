from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard() -> ReplyKeyboardMarkup:
    start_button = KeyboardButton(text="Старт")

    return ReplyKeyboardMarkup(keyboard=[[start_button]], resize_keyboard=True)
