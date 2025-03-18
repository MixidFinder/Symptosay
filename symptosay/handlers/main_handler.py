import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from keyboards.main_kb import get_main_kb
from services.state import load_context

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

main_router = Router()


@main_router.message(F.text.lower() == "назад")
async def back(message: Message, state: FSMContext):
    await load_context(message, state)


@main_router.message(F.text.lower() == "главная")
async def open_main_menu(message: Message, state: FSMContext) -> None:
    await message.reply("Главное меню", reply_markup=await get_main_kb(message.from_user.id))
    await state.clear()
