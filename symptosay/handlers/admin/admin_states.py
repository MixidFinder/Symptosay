from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    waiting_username_rmv = State()
    waiting_username_add = State()
    main_admin_keyboard = State()
    db_admin_keyboard = State()
    user_admin_keyboard = State()
