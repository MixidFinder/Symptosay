import logging
import os

from dotenv import find_dotenv, load_dotenv

from . import connection

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


async def check_is_admin(user_id: int) -> bool:
    user_data = await get_user_by_id(user_id)
    if not user_data:
        return False
    logger.info("User %s is_admin: %s", user_id, user_data["is_admin"])
    return bool(user_data["is_admin"])


async def get_user_by_id(user_id: int):
    return await connection.request_service("get", f"{USER_SERVICE_URL}/api/users/{user_id}")


async def register_user(user_data: dict[str, str]):
    return await connection.request_service("post", f"{USER_SERVICE_URL}/api/users/register", user_data)


async def toggle_admin(username: str, is_admin: bool):
    return await connection.request_service(
        "patch", f"{USER_SERVICE_URL}/api/users/{username}/toggle-admin", data={"is_admin": is_admin}
    )
