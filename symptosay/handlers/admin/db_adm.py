import json
import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError, codes
from keyboards.admin_kb import get_admin_nav_kb
from keyboards.main_kb import build_pagination_db_kb, get_main_kb
from services import db_service
from services.state import save_context

from handlers.user_handler import PAGINATION_SIZE

logger = logging.getLogger(__name__)

db_adm_router = Router()


class SymptomsStates(StatesGroup):
    waiting_symptoms_add = State()
    waiting_symptoms_del = State()


class DiseaseStates(StatesGroup):
    waiting_diseases_add = State()
    waiting_diseases_del = State()


class LinkStates(StatesGroup):
    waiting_disease_choice = State()
    waiting_symptoms_choice = State()
    link_symptom = State()


@db_adm_router.callback_query(F.data == "add_symptoms_adm")
async def add_db_symptoms(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Введите симптомы через запятую"
    await state.set_state(SymptomsStates.waiting_symptoms_add)
    await save_context(state, get_admin_nav_kb(), text)
    await callback.message.edit_text(text, reply_markup=get_admin_nav_kb())


@db_adm_router.callback_query(F.data == "add_diseases_adm")
async def add_db_diseases(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Введите болезни через запятую"
    await state.set_state(DiseaseStates.waiting_diseases_add)
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


@db_adm_router.message(DiseaseStates.waiting_diseases_add)
async def process_add_diseases(message: Message, state: FSMContext, user_data: dict[str, Any]) -> None:
    input_text = message.text.strip().lower()

    diseases = [{"name": disease} for disease in map(str.strip, input_text.split(",")) if disease]
    logger.info("Get diseases: %s", diseases)

    if diseases:
        try:
            await db_service.add_diseases(diseases)
            await message.reply("Болезни успешно добавлены", reply_markup=get_main_kb(user_data.get("is_admin", False)))
        except HTTPStatusError as e:
            if e.response.status_code == codes.CONFLICT:
                await message.reply("Болезни уже есть в базе")
        except Exception as e:
            logger.debug("Exception: %s", e)
            await message.reply("Произошла непредвиденная ошибка, попробуйте позже")
        finally:
            await state.clear()
    else:
        await message.reply("Пожалуйста, введите болезни через запятую, либо одну болезнь")


@db_adm_router.callback_query(F.data == "delete_diseases_adm")
async def delete_db_diseases(callback: CallbackQuery, state: FSMContext):
    text = "Введите болезни через запятую"
    await state.set_state(DiseaseStates.waiting_diseases_del)
    await save_context(state, get_admin_nav_kb(), text)
    await callback.message.edit_text(text, reply_markup=get_admin_nav_kb())


@db_adm_router.message(DiseaseStates.waiting_diseases_del)
async def process_del_diseases(message: Message, state: FSMContext, user_data: dict[str, Any]):
    input_text = message.text.strip().lower()
    diseases = [{"name": disease} for disease in map(str.strip, input_text.split(",")) if disease]
    logger.info("Get diseases: %s", json.dumps(diseases))
    if diseases:
        try:
            await db_service.del_diseases(diseases)
            await message.reply("Болезни успешно удалены", reply_markup=get_main_kb(user_data.get("is_admin", False)))
        except Exception as e:
            logger.info("Exception: %s", e)
            await message.reply("Произошла непредвиденная ошибка, попробуйте позже")
        finally:
            await state.clear()
    else:
        await message.reply("Пожалуйста, введите болезни через запятую, либо одну болезнь")


@db_adm_router.callback_query(F.data == "link_disease_symptom")
async def link_choose_disease(callback: CallbackQuery, state: FSMContext):
    text = "Выберите болезнь с которой нужно связать симптомы"
    action = "choose"
    target = "symptom"

    response = await db_service.get_diseases({"size": PAGINATION_SIZE})

    await state.set_data({"action": action, "target": target})
    keyboard = build_pagination_db_kb(data=response, action=action, target=target)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await state.set_state(LinkStates.waiting_disease_choice)


@db_adm_router.callback_query(lambda c: c.data.startswith("choose_symptom_"))
async def link_choose_symptom(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    disease_id = data.get("disease_id")
    if disease_id is None:
        disease_id = int(callback.data.split("_")[2])
        await state.update_data({"disease_id": disease_id})

    text = "Выберите симптомы, те симптомы которые уже связаны с болезнью - пропадают"
    action = "link"
    target = "symptom"
    response = await db_service.get_unlinked_symptom(disease_id, pagination={"size": PAGINATION_SIZE})
    await state.update_data({"action": action, "target": target, "data": response})
    keyboard = build_pagination_db_kb(data=response, action=action, target=target)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await state.set_state(LinkStates.waiting_symptoms_choice)


@db_adm_router.callback_query(lambda c: c.data.startswith("link_symptom_"))
async def link_symptom(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    disease_id = data.get("disease_id")
    symptom_id = int(callback.data.split("_")[2])
    action = "link"
    target = "symptom"

    await db_service.link_symptom(symptom_id=symptom_id, disease_id=disease_id)
    response = await db_service.get_unlinked_symptom(disease_id, {"size": PAGINATION_SIZE})
    keyboard = build_pagination_db_kb(data=response, action=action, target=target)
    await state.update_data({"action": action, "target": target, "data": response})
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@db_adm_router.callback_query(LinkStates.waiting_symptoms_choice, lambda c: c.data.startswith("page_"))
async def symptom_page_handler(callback: CallbackQuery, state: FSMContext):
    logger.info("State: %s", await state.get_state())
    page = int(callback.data.split("_")[1])
    await state.update_data(page=page)
    state_data = await state.get_data()
    data = await db_service.get_unlinked_symptom(state_data["disease_id"], {"page": page, "size": PAGINATION_SIZE})

    keyboard = build_pagination_db_kb(data=data, action=state_data["action"], target=state_data["target"])

    await callback.message.edit_reply_markup(reply_markup=keyboard)


@db_adm_router.callback_query(LinkStates.waiting_disease_choice, lambda c: c.data.startswith("page_"))
async def disease_page_handler(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[1])
    await state.update_data(page=page)
    state_data = await state.get_data()
    data = await db_service.get_diseases({"page": page, "size": PAGINATION_SIZE})

    keyboard = build_pagination_db_kb(data=data, action=state_data["action"], target=state_data["target"])
    await callback.message.edit_reply_markup(reply_markup=keyboard)
