import os
from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from services.user_service import get_user_by_id, register_user


class UserDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Awaitable[Any]:
        user_id = event.from_user.id
        username = event.from_user.username

        user_data = await get_user_by_id(user_id)

        admins = os.getenv("ADMINS", "").split(",")
        is_admin = str(user_id) in admins

        if not user_data:
            new_user = {"user_id": user_id, "username": username, "is_admin": is_admin}
            user_data = await register_user(new_user)
            if user_data is None:
                user_data = {"user_id": user_id, "username": username, "is_admin": is_admin}

        if "is_admin" not in user_data:
            user_data["is_admin"] = is_admin

        data["user_data"] = user_data
        return await handler(event, data)
