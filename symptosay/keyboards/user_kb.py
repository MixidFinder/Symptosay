from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_profile_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Ваши записи", callback_data="user_symptoms")
