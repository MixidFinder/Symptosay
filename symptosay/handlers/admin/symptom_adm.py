import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

logger = logging.getLogger(__name__)

symptom_router = Router()


class AddSymptoms(StatesGroup):
    waiting_symptoms = State()


@symptom_router.message(F.text.lower() == "добавить симптомы в бд")
async def add_db_symptoms(message: Message, state: FSMContext) -> None:
    await message.reply("Введите симтомы через замятую", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddSymptoms.waiting_symptoms)


@symptom_router.message(AddSymptoms.waiting_symptoms)
async def process_symptoms(message: Message, state: FSMContext) -> None:
    pass
