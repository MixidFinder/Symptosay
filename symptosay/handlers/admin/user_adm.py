import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.main_kb import get_main_kb, get_nav_kb

from services.user_service import toggle_admin

logger = logging.getLogger(__name__)

user_adm_router = Router()


class AddAdmin(StatesGroup):
    waiting_user_id = State()


class RemoveAdmin(StatesGroup):
    waiting_username = State()


@user_adm_router.message(F.text.lower() == "добавить админа")
async def add_admin(message: Message, state: FSMContext):
    await message.reply("Введите юзернейм пользователя", reply_markup=get_nav_kb())
    await state.set_state(AddAdmin.waiting_user_id)


@user_adm_router.message(AddAdmin.waiting_user_id)
async def process_add_admin(message: Message, state: FSMContext, user_data: dict[str, Any]):
    target_username = str(message.text.strip())

    if await toggle_admin(target_username, is_admin=True):
        await message.reply(
            f"Пользователь {message.text.strip()} стал админом",
            reply_markup=await get_main_kb(user_data["is_admin"]),
        )
        await state.clear()
    else:
        await message.reply(f"Пользователь {target_username} не найден, введите корректный айди")


@user_adm_router.message(F.text.lower() == "удалить админа")
async def remove_admin(message: Message, state: FSMContext):
    await message.reply("Введите юзернейм пользователя", reply_markup=get_nav_kb())
    await state.set_state(RemoveAdmin.waiting_username)


@user_adm_router.message(RemoveAdmin.waiting_username)
async def process_remove_admin(message: Message, state: FSMContext, user_data: dict[str, Any]):
    target_username = str(message.text.strip())

    if await toggle_admin(target_username, is_admin=False):
        await message.reply(
            f"Пользователь {target_username} потерял права админа",
            reply_markup=await get_main_kb(user_data["is_admin"]),
        )
        await state.clear()
    else:
        await message.reply(f"Пользователь {target_username} не найден, введите корректный айди")
