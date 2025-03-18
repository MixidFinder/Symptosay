import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from filters.admin_filter import IsAdminFilter
from keyboards.admin_kb import get_admin_keyboard
from services.state import save_context

from . import user_adm

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.include_router(user_adm.user_adm_router)
admin_router.message.filter(IsAdminFilter())


@admin_router.message(F.text.lower() == "админ панель")
async def open_admin_panel(message: Message, state: FSMContext) -> None:
    logger.info("User %s opened admin panel", message.from_user.id)
    await message.reply("Админ панель открыта", reply_markup=get_admin_keyboard())
    await save_context(state, keyboard=get_admin_keyboard(), text="Админ панель открыта")
