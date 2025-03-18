from __future__ import annotations

from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.main_kb import get_main_kb

HISTORY_LEN = 10


async def save_context(
    state: FSMContext,
    keyboard: ReplyKeyboardMarkup | ReplyKeyboardRemove,
    text: str,
    additional_data: dict[str, Any] | None = None,
):
    data = await state.get_data()
    history = data.get("menu_history", [])

    current_context = {"text": text, "keyboard": keyboard, "state": await state.get_state(), "data": additional_data}
    history.append(current_context)

    await state.update_data(menu_history=history)


async def load_context(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("menu_history", [])

    if not history:
        await state.clear()
        await message.reply("Главное меню", reply_markup=await get_main_kb(message.from_user.id))
        return

    previous_context = history.pop()
    await state.update_data(menu_history=history)
    await state.set_state(previous_context["state"])

    await message.reply(previous_context["text"], reply_markup=previous_context["keyboard"])
