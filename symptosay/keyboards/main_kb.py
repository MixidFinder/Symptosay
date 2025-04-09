import logging
from typing import Any

from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

logger = logging.getLogger(__name__)


def get_main_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
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


def get_inline_nav_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="back")
    keyboard.button(text="Главная", callback_data="home")
    return keyboard.as_markup()


def build_pagination_db_kb(data: dict[str, Any], action: str, target: str):
    builder = InlineKeyboardBuilder()
    logger.debug("Get pagination data: %s, action: %s, target: %s", data, action, target)

    for item in data["items"]:
        builder.button(text=item["name"], callback_data=f"{action}_{target}_{item['id']}")

    pagination_btns = []

    if data["page"] > 1:
        pagination_btns.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{data['page'] - 1}"))

    if data["page"] * data["size"] < data["total"]:
        pagination_btns.append(InlineKeyboardButton(text="Далее ➡️", callback_data=f"page_{data['page'] + 1}"))

    builder.adjust(1)
    if pagination_btns:
        builder.row(*pagination_btns)

    builder.row(InlineKeyboardButton(text="Отмена", callback_data="home"))

    return builder.as_markup()
