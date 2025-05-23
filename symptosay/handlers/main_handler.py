import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.main_kb import get_main_kb
from services.state import load_context

logger = logging.getLogger(__name__)

main_router = Router()


@main_router.message(F.text.lower() == "назад")
async def back(message: Message, state: FSMContext, user_data: dict[str, Any]):
    await state.set_data(user_data)
    await load_context(message, state)


@main_router.message(F.text.lower() == "главная")
async def open_main_menu(message: Message, state: FSMContext, user_data: dict[str, Any]) -> None:
    await message.answer("Главное меню", reply_markup=get_main_kb(user_data["is_admin"]))
    await state.clear()


@main_router.callback_query(F.data == "home")
async def open_main_menu_inline(callback: CallbackQuery, state: FSMContext, user_data: dict[str, Any]):
    await callback.message.edit_text("Главное меню")
