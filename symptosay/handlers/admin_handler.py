import logging

from aiogram import F, Router
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from filters.admin_filter import IsAdminFilter
from keyboards.admin_kb import get_admin_keyboard
from keyboards.main_kb import get_main_kb

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

admin_router = Router()
admin_router.message.filter(IsAdminFilter())


@admin_router.message(F.text.lower() == "админ панель")
async def open_admin_panel(message: Message) -> None:
    logger.info("User %s opened admin panel", message.from_user.id)
    await message.reply("Админ панель открыта", reply_markup=get_admin_keyboard())


@admin_router.message(F.text.lower() == "назад")
async def open_main_menu(message: Message) -> None:
    await message.reply("Главное меню", reply_markup=await get_main_kb(message.from_user.id))
