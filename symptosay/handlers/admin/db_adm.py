import json
import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError, codes
from keyboards.admin_kb import get_admin_nav_kb
from keyboards.main_kb import get_main_kb
from services import db_service
from services.state import save_context

logger = logging.getLogger(__name__)

db_adm_router = Router()


class SymptomsStates(StatesGroup):
    waiting_symptoms_add = State()
    waiting_symptoms_del = State()


@db_adm_router.callback_query(F.data == "add_symptoms_adm")
async def add_db_symptoms(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Введите симптомы через запятую"
    await state.set_state(SymptomsStates.waiting_symptoms_add)
    await save_context(state, get_admin_nav_kb(), text)
    await callback.message.edit_text(text, reply_markup=get_admin_nav_kb())


@db_adm_router.message(SymptomsStates.waiting_symptoms_add)
async def process_add_symptoms(message: Message, state: FSMContext, user_data: dict[str, Any]) -> None:
    input_text = message.text.strip().lower()

    symptoms = [{"name": symptom} for symptom in map(str.strip, input_text.split(",")) if symptom]
    logger.info("Get symptoms: %s", symptoms)

    if symptoms:
        try:
            await db_service.add_symptoms(symptoms)
            await message.reply(
                "Симптомы успешно добавлены", reply_markup=get_main_kb(user_data.get("is_admin", False))
            )
        except HTTPStatusError as e:
            if e.response.status_code == codes.CONFLICT:
                await message.reply("Симптомы уже есть в базе")
        except Exception as e:
            logger.debug("Exception: %s", e)
            await message.reply("Произошла непредвиденная ошибка, попробуйте позже")
        finally:
            await state.clear()
    else:
        await message.reply("Пожалуйста, введите симптомы через запятую, либо один симптом")


@db_adm_router.callback_query(F.data == "delete_symptoms_adm")
async def delete_db_symptoms(callback: CallbackQuery, state: FSMContext):
    text = "Введите симптомы через запятую"
    await state.set_state(SymptomsStates.waiting_symptoms_del)
    await save_context(state, get_admin_nav_kb(), text)
    await callback.message.edit_text(text, reply_markup=get_admin_nav_kb())


@db_adm_router.message(SymptomsStates.waiting_symptoms_del)
async def process_del_symptoms(message: Message, state: FSMContext, user_data: dict[str, Any]):
    input_text = message.text.strip().lower()
    symptoms = [{"name": symptom} for symptom in map(str.strip, input_text.split(",")) if symptom]
    logger.info("Get symptoms: %s", json.dumps(symptoms))
    if symptoms:
        try:
            await db_service.del_symptoms(symptoms)
            await message.reply("Симптомы успешно удалены", reply_markup=get_main_kb(user_data.get("is_admin", False)))
        except Exception as e:
            logger.info("Exception: %s", e)
            await message.reply("Произошла непредвиденная ошибка, попробуйте позже")
        finally:
            await state.clear()
    else:
        await message.reply("Пожалуйста, введите симптомы через запятую, либо один симптом")
