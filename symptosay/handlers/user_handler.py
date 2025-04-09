from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError
from keyboards.main_kb import build_pagination_db_kb
from services.db_service import get_symptoms

user_router = Router()
PAGINATION_SIZE = 5


class UserState(StatesGroup):
    waiting_symptom_record = State()
    waiting_disease_add = State()


@user_router.message(F.text.lower() == "записать симптом")
async def add_user_symptom(message: Message, state: FSMContext):
    try:
        action = "add"
        target = "symptom"
        response = await get_symptoms({"size": PAGINATION_SIZE})
        await state.set_data({"action": action, "target": target})
        await message.answer(
            "Пожалуйста ввыберите симптом", reply_markup=build_pagination_db_kb(response, action, target)
        )
        await state.set_state(UserState.waiting_symptom_record)
    except HTTPStatusError:
        await message.reply("Ошибка сервера, попробуйте позже")


@user_router.message(UserState.waiting_symptom_record, lambda c: c.data.startwith("add_symptom_"))
async def record_user_symptom(callback: CallbackQuery, state: FSMContext, user_data: dict[str, Any]):
    symptom_id = int(callback.data.split("_")[2])


@user_router.callback_query(UserState.waiting_symptom_record, lambda c: c.data.startswith("page_"))
async def page_handler(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[1])
    await state.update_data(page=page)
    state_data = await state.get_data()
    data = await get_symptoms({"page": page, "size": PAGINATION_SIZE})

    keyboard = build_pagination_db_kb(data=data, action=state_data["action"], target=state_data["target"])

    await callback.message.edit_reply_markup(reply_markup=keyboard)
