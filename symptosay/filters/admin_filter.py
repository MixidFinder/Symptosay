import logging
from typing import override

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.user_service import check_is_admin, get_user_by_id

logger = logging.getLogger(__name__)


class IsAdminFilter(BaseFilter):
    @override
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user_data = await get_user_by_id(user_id)
        logger.info("Filtered user: %s with user_data: %s", user_id, user_data)

        return await check_is_admin(user_data["user_id"])
