import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./users.db"

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
