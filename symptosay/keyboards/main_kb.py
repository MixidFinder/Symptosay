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
    keyboard.row(KeyboardButton(text="Профиль"))

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


def build_pagination_db_kb(data: dict[str, Any] | list, action: str, target: str):
    builder = InlineKeyboardBuilder()
    logger.debug("Get pagination data: %s, action: %s, target: %s", data, action, target)

    if isinstance(data, dict):
        items = data.get("items", [])
        page = data.get("page", 1)
        size = data.get("size", len(items))
        total = data.get("total", len(items))
    elif isinstance(data, list):
        items = data
        page = 1
        size = len(items)
        total = len(items)

    for item in items:
        builder.button(text=item.get("name"), callback_data=f"{action}_{target}_{item.get('id')}")

    pagination_btns = []

    if page > 1:
        pagination_btns.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))

    if page * size < total:
        pagination_btns.append(InlineKeyboardButton(text="Далее ➡️", callback_data=f"page_{page + 1}"))

    builder.adjust(1)
    if pagination_btns:
        builder.row(*pagination_btns)

    builder.row(InlineKeyboardButton(text="Отмена", callback_data="home"))

    return builder.as_markup()
