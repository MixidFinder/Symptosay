import logging
import os
from collections.abc import AsyncGenerator

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("USER_SERVICE_DB")

if not DATABASE_URL:
    msg = "Missing database URL"
    raise ValueError(msg)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
            logger.info("Session success")
    except Exception:
        logger.exception("Session error")
        raise
