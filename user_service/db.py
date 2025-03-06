import logging
import os
from collections.abc import AsyncGenerator

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

load_dotenv(find_dotenv())

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWD')}@user_service_db/users"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
            logger.info("Session success")
    except Exception as e:
        logger.error(f"Error session: {e}")


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("DB tables created successfully")
    except Exception as e:
        logger.error(f"Error creating db tables: {e}")
