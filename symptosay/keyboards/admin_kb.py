from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Работа с БД", callback_data="db_management")
    keyboard.button(text="Работа с пользователями", callback_data="user_management")
    return keyboard.as_markup()


def get_db_management_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Добавить симптомы", callback_data="add_symptoms_adm")
    keyboard.button(text="Добавить болезни", callback_data="add_diseases_adm")
    keyboard.button(text="Удалить симптомы", callback_data="delete_symptoms_adm")
    keyboard.button(text="Удалить болезни", callback_data="delete_diseases_adm")
    keyboard.button(text="Обновить симптом", callback_data="update_symptoms_adm")
    keyboard.button(text="Обновить болезнь", callback_data="update_diseases_adm")
    keyboard.button(text="Посмотреть все симптомы", callback_data="get_all_symptoms")
    keyboard.button(text="Посмотреть все болезни", callback_data="get_all_diseases")
    keyboard.button(text="Назад", callback_data="admin_back")
    keyboard.button(text="Отмена", callback_data="admin_cancel")
    keyboard.adjust(2)
    return keyboard.as_markup()


def get_user_management_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Добавить админа", callback_data="add_admin")
    keyboard.button(text="Удалить админа", callback_data="delete_admin")
    keyboard.button(text="Назад", callback_data="admin_back")
    keyboard.adjust(2)
    return keyboard.as_markup()


def get_admin_nav_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="admin_back")
    keyboard.button(text="Отмена", callback_data="admin_cancel")
    return keyboard.as_markup()
