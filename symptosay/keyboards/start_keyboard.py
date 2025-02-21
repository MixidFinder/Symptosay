from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard():
    start_button = KeyboardButton(text="Старт")
    start_keyboard = ReplyKeyboardMarkup(
        keyboard=[[start_button]], resize_keyboard=True
    )

    return start_keyboard
