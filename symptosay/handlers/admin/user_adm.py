import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from services.user_service import toggle_admin

logger = logging.getLogger(__name__)

user_adm_router = Router()


class AddAdmin(StatesGroup):
    waiting_user_id = State()


class RemoveAdmin(StatesGroup):
    waiting_user_id = State()


@user_adm_router.message(F.text.lower() == "добавить админа")
async def add_admin(message: Message, state: FSMContext):
    await message.reply("Введите айди пользователя", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddAdmin.waiting_user_id)


@user_adm_router.message(AddAdmin.waiting_user_id)
async def process_add_admin(message: Message, state: FSMContext):
    target_id = int(message.text.strip())

    if await toggle_admin(target_id, True):
        await message.reply(f"Пользователь {message.text.strip()} стал админом")
        await state.clear()
    else:
        await message.reply(f"Пользователь {target_id} не найден, введите корректный айди")


@user_adm_router.message(F.text.lower() == "удалить админа")
async def remove_admin(message: Message, state: FSMContext):
    await message.reply("Введите айди пользователя", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RemoveAdmin.waiting_user_id)


@user_adm_router.message(RemoveAdmin.waiting_user_id)
async def process_remove_admin(message: Message, state: FSMContext):
    target_id = int(message.text.strip())

    if await toggle_admin(target_id, False):
        await message.reply(f"Пользователь {target_id} теперь не админ")
        await state.clear()
    else:
        await message.reply(f"Пользователь {target_id} не найден, введите корректный айди")
