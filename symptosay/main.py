import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from handlers.admin.admin import admin_router
from handlers.main_handler import main_router
from handlers.start_handler import start_router
from handlers.user_handler import user_router
from middlewares.user_middleware import UserDataMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("user_service.log", mode="w"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    msg = "BOT_TOKEN not set."
    raise ValueError(msg)
bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.message.outer_middleware(UserDataMiddleware())
dp.callback_query.outer_middleware(UserDataMiddleware())

dp.include_routers(start_router, main_router, admin_router, user_router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
