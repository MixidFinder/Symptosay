import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

from handlers.start_handler import start_router

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
bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(start_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
