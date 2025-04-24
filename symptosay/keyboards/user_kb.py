from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_profile_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Ваши записи", callback_data="user_symptoms")
    return keyboard.as_markup()


def user_records_markup(data: dict, page: int, pages: int) -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()

    message_lines = []
    for idx, item in enumerate(data["items"], start=1):
        timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%d.%m.%Y %H:%M")
        message_lines.append(
            f"{idx}. Болезнь: <b>{item['disease_name']}</b>, симптом: <b>{item['symptom_name']}</b>\n   🕒 {timestamp}\n"
        )

    message = f"📋 <b>Ваши записи симптомов</b>\n\n{''.join(message_lines)}\nСтраница {page}/{pages}"

    pagination_btns = []
    if page > 1:
        pagination_btns.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))

    if page < pages:
        pagination_btns.append(InlineKeyboardButton(text="Далее ➡️", callback_data=f"page_{page + 1}"))

    if pagination_btns:
        builder.row(*pagination_btns)

    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="home"))

    return message, builder.as_markup()
