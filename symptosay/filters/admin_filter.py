import logging
from typing import Any, override

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from services.adm_user_service import check_is_admin

logger = logging.getLogger(__name__)


class IsAdminFilter(BaseFilter):
    @override
    async def __call__(self, event: Message | CallbackQuery, user_data: dict[str, Any] | None = None) -> bool:
        user_id = event.from_user.id
        logger.info("Filtered user: %s with user_data: %s", user_id, user_data)

        if user_data:
            return user_data["is_admin"]

        return await check_is_admin(user_id)
