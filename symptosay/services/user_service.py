from __future__ import annotations

import logging

import httpx
from handlers.start_handler import USER_SERVICE_URL

logger = logging.getLogger(__name__)


async def check_is_admin(user_data: dict[str, str]) -> bool:
    logger.info("User %s is_admin: %s", user_data["user_id"], user_data["is_admin"])
    return bool(user_data.get("is_admin", False))


async def get_user_by_id(user_id: int) -> dict[str, str]:
    try:
        async with httpx.AsyncClient() as session:
            logger.info("Get request %s/users/%s", USER_SERVICE_URL, user_id)
            response = await session.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5)

            response.raise_for_status()

            return response.json()
    except httpx.RequestError as e:
        logger.exception(msg=e)
        return {}


async def register_user(user_data: dict[str, str]) -> int:
    try:
        async with httpx.AsyncClient() as session:
            logger.info("Post request to %s/users/register for user %s", USER_SERVICE_URL, user_data["user_id"])
            response = await session.post(f"{USER_SERVICE_URL}/users/register", json=user_data, timeout=5)
            response.raise_for_status()
            logger.info("User %s registered", user_data["user_id"])
            return response.status_code
    except httpx.HTTPStatusError as e:
        logger.exception("User register error")
        return e.response.status_code
