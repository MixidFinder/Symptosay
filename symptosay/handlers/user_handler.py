import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError
from keyboards.main_kb import build_pagination_db_kb
from keyboards.user_kb import user_profile_kb, user_records_markup
from services import db_service

logger = logging.getLogger(__name__)

user_router = Router()
PAGINATION_SIZE = 5


class UserState(StatesGroup):
    waiting_symptom_choice = State()
    waiting_disease_choice = State()
    see_records = State()


@user_router.message(F.text.lower() == "записать симптом")
async def process_add_user_symptom(message: Message, state: FSMContext):
    try:
        action = "choose"
        target = "disease"
        text = "Пожалуйста выберите болезнь"
        response = await db_service.get_diseases({"size": PAGINATION_SIZE})
        await state.set_data({"action": action, "target": target})
        await message.answer(
            text=text,
            reply_markup=build_pagination_db_kb(response, action, target),
        )
        await state.set_state(UserState.waiting_disease_choice)
    except HTTPStatusError:
        await message.reply("Ошибка сервера, попробуйте позже")


@user_router.callback_query(UserState.waiting_disease_choice, lambda c: c.data.startswith("choose_disease_"))
async def record_user_disease_choice(callback: CallbackQuery, state: FSMContext):
    disease_id = int(callback.data.split("_")[2])
    action = "add"
    target = "symptom"

    response = await db_service.get_disease_symptoms(disease_id=disease_id, pagination={"size": PAGINATION_SIZE})
    logger.info("Get disease_symptoms: %s", response)

    await state.set_data({"action": action, "target": target, "disease_id": disease_id})
    await callback.message.edit_text(
        "Пожалуйста выберите симптом который хотите записать",
        reply_markup=build_pagination_db_kb(
            data=response,
            action=action,
            target=target,
        ),
    )
    await state.set_state(UserState.waiting_symptom_choice)


@user_router.callback_query(UserState.waiting_symptom_choice, lambda c: c.data.startswith("add_symptom_"))
async def record_user_symptom(callback: CallbackQuery, state: FSMContext, user_data: dict[str, Any]):
    symptom_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    try:
        await db_service.add_user_symptom(
            symptom_id=symptom_id, user_id=user_data["user_id"], disease_id=data["disease_id"]
        )
        await callback.message.edit_text("Симптом успешно записан")
        await state.clear()
    except HTTPStatusError:
        await callback.message.edit_text("Возникла ошибка, попробуйте позже")
        await state.clear()


@user_router.callback_query(UserState.waiting_disease_choice, lambda c: c.data.startswith("page_"))
async def disease_page_handler(callback: CallbackQuery, state: FSMContext):
    if isinstance(callback, CallbackQuery):
        page = int(callback.data.split("_")[1])
        await state.update_data(page=page)
        state_data = await state.get_data()
        data = await db_service.get_diseases({"page": page, "size": PAGINATION_SIZE})

        keyboard = build_pagination_db_kb(data=data, action=state_data["action"], target=state_data["target"])
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@user_router.callback_query(UserState.waiting_symptom_choice, lambda c: c.data.startswith("page_"))
async def symptom_page_handler(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[1])
    await state.update_data(page=page)
    state_data = await state.get_data()
    data = await db_service.get_disease_symptoms(state_data["disease_id"], {"page": page, "size": PAGINATION_SIZE})

    keyboard = build_pagination_db_kb(data=data, action=state_data["action"], target=state_data["target"])

    await callback.message.edit_reply_markup(reply_markup=keyboard)


@user_router.message(F.text.lower() == "профиль")
async def user_profile_handler(message: Message, state: FSMContext):
    text = "Профиль"
    await message.answer(text=text, reply_markup=user_profile_kb())
    await state.set_state(UserState.see_records)


@user_router.callback_query(F.data == "user_symptoms")
async def user_records(callback: CallbackQuery, state: FSMContext, user_data: dict[str, Any]):
    action = "get"
    target = "records"
    data = await db_service.get_user_records(user_data["user_id"], pagination={"size": PAGINATION_SIZE})
    message, keyboard = user_records_markup(data, 1, data["pages"])
    await state.set_data({"action": action, "target": target})
    await callback.message.edit_text(text=message, reply_markup=keyboard, parse_mode="HTML")


@user_router.callback_query(UserState.see_records, lambda c: c.data.startswith("page_"))
async def records_page_handler(callback: CallbackQuery, state: FSMContext, user_data: dict[str, Any]):
    page = int(callback.data.split("_")[1])
    await state.update_data(page=page)
    state_data = await state.get_data()
    data = await db_service.get_user_records(
        user_id=user_data["user_id"], pagination={"page": page, "size": PAGINATION_SIZE}
    )

    message, keyboard = user_records_markup(data, page, data["pages"])

    await callback.message.edit_text(text=message, reply_markup=keyboard, parse_mode="HTML")
