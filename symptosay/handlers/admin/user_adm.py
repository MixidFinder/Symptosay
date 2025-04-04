import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError, codes
from keyboards.admin_kb import get_admin_main_keyboard, get_admin_nav_kb, get_user_management_keyboard
from keyboards.main_kb import get_main_kb
from services.state import load_context, save_context
from services.user_service import toggle_admin

from .admin_states import AdminState

logger = logging.getLogger(__name__)

user_adm_router = Router()


@user_adm_router.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.waiting_username_add)
    await save_context(state, text="Введите юзернейм пользовтателя", keyboard=get_user_management_keyboard())
    await callback.message.edit_text("Введите юзернейм пользователя", reply_markup=get_admin_nav_kb())


@user_adm_router.callback_query(F.data == "delete_admin")
async def remove_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.waiting_username_rmv)
    await save_context(state, text="Введите юзернейм пользователя", keyboard=get_user_management_keyboard())
    await callback.message.edit_text("Введите юзернейм пользователя", reply_markup=get_admin_nav_kb())


@user_adm_router.message(AdminState.waiting_username_rmv)
async def process_remove_admin(message: Message, state: FSMContext, user_data: dict[str, Any]):
    target_username = str(message.text.strip())

    try:
        await toggle_admin(user_data={"username": target_username, "is_admin": False})
        await message.reply(
            f"Пользователь {target_username} потерял права админа",
            reply_markup=get_main_kb(user_data["is_admin"]),
        )
        await state.clear()
    except HTTPStatusError as e:
        if e.response.status_code == codes.NOT_FOUND:
            await message.reply(f"Пользователь {target_username} не найден, введите корректный айди")
        else:
            await message.reply(
                "Ошибка сервера, попробуйте позже", reply_markup=get_main_kb(user_data.get("is_admin", False))
            )
            await state.clear()


@user_adm_router.message(AdminState.waiting_username_add)
async def process_add_admin(message: Message, state: FSMContext, user_data: dict[str, Any]):
    target_username = str(message.text.strip())

    try:
        await toggle_admin(user_data={"username": target_username, "is_admin": True})
        await message.reply(
            f"Пользователь {target_username} получил права админа",
            reply_markup=get_main_kb(user_data["is_admin"]),
        )
        await state.clear()
    except HTTPStatusError as e:
        if e.response.status_code == codes.NOT_FOUND:
            await message.reply(f"Пользователь {target_username} не найден, введите корректный айди")
        else:
            await message.reply(
                "Ошибка сервера, попробуйте позже", reply_markup=get_main_kb(user_data.get("is_admin", False))
            )
            await state.clear()


@user_adm_router.callback_query(F.data == "admin_cancel")
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Админ панель", reply_markup=get_admin_main_keyboard())
    await state.clear()


@user_adm_router.callback_query(F.data == "admin_back")
async def process_back(callback: CallbackQuery, state: FSMContext):
    await load_context(callback, state)
