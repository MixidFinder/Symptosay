import logging
import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


async def check_is_admin(user_id: int) -> bool:
    user_data = await get_user_by_id(user_id)
    if not user_data:
        return False
    logger.info("User %s is_admin: %s", user_id, user_data["is_admin"])
    return bool(user_data["is_admin"])


async def get_user_by_id(user_id: int):
    try:
        async with httpx.AsyncClient() as session:
            response = await session.get(f"{os.getenv('USER_SERVICE_URL')}/users/{user_id}", timeout=5)

            response.raise_for_status()

            return response.json()
    except Exception as e:
        logger.exception(msg=e)
        return None


async def register_user(user_data: dict[str, str]):
    try:
        async with httpx.AsyncClient() as session:
            response = await session.post(f"{os.getenv('USER_SERVICE_URL')}/users/register", json=user_data, timeout=5)
            response.raise_for_status()
            logger.info("User %s registered", user_data["user_id"])
            return response.json()
    except httpx.HTTPStatusError:
        logger.exception("User register error")
        return None


async def toggle_admin(username: str, is_admin: bool):
    try:
        async with httpx.AsyncClient() as session:
            response = await session.patch(
                f"{os.getenv('USER_SERVICE_URL')}/users/{username}/toggle-admin", json={"is_admin": is_admin}, timeout=5
            )
            response.raise_for_status()
            logger.info("User %s toggle-admin", username)
            return response.json()
    except httpx.HTTPStatusError:
        logger.exception("User toggle-admin error")
        return None
