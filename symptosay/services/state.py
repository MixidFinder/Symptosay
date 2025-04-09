import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.main_kb import get_main_kb

HISTORY_LEN = 10
logger = logging.getLogger(__name__)


async def save_context(
    state: FSMContext,
    keyboard: ReplyKeyboardMarkup | ReplyKeyboardRemove | InlineKeyboardMarkup,
    text: str | None = None,
):
    data = await state.get_data()
    history = data.get("menu_history", [])

    current_context = {"text": text, "keyboard": keyboard, "state": await state.get_state()}
    logger.debug("Saved context: %s", current_context)
    logger.debug("History keyboards: %s", history)
    history.append(current_context)

    await state.update_data(menu_history=history)


async def load_context(event: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.debug("State data %s", data)
    history = data.get("menu_history", [])
    is_callback = isinstance(event, CallbackQuery)

    user_data = data.get("user_data")
    logger.debug("Load context with user data: %s", user_data)
    history.pop()

    if not history:
        await state.clear()
        if is_callback:
            await event.message.edit_text("Главное меню", reply_markup=get_main_kb(user_data["is_admin"]))
        else:
            await event.reply("Главное меню", reply_markup=get_main_kb(user_data["is_admin"]))
        return
    previous_context = history[-1]
    await state.update_data(menu_history=history)
    await state.set_state(previous_context["state"])

    logger.debug("Load context with context: %s", previous_context)

    if is_callback:
        await event.message.edit_text(text=previous_context["text"], reply_markup=previous_context["keyboard"])
    else:
        await event.reply(previous_context["text"], reply_markup=previous_context["keyboard"])
