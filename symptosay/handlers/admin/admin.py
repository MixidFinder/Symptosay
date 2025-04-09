import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from filters.admin_filter import IsAdminFilter
from keyboards.admin_kb import get_admin_main_keyboard, get_db_management_keyboard, get_user_management_keyboard
from services.state import save_context

from .db_adm import db_adm_router
from .user_adm import user_adm_router

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(IsAdminFilter())
admin_router.callback_query.filter(IsAdminFilter())
admin_router.include_router(user_adm_router)
admin_router.include_router(db_adm_router)


@admin_router.message(F.text.lower() == "админ панель")
async def open_admin_panel(message: Message, state: FSMContext) -> None:
    logger.info("User %s opened admin panel", message.from_user.id)
    text = "Админ панель"
    await save_context(state=state, keyboard=get_admin_main_keyboard(), text=text)
    await message.answer(text, reply_markup=get_admin_main_keyboard())


@admin_router.callback_query(F.data == "user_management")
async def user_admin_actions(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Управление пользователями"
    await save_context(state, text=text, keyboard=get_user_management_keyboard())
    await callback.message.edit_text(text=text, reply_markup=get_user_management_keyboard())


@admin_router.callback_query(F.data == "db_management")
async def db_admin_actions(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Управление базой данных"
    await save_context(state, text=text, keyboard=get_db_management_keyboard())
    await callback.message.edit_text(text=text, reply_markup=get_db_management_keyboard())
