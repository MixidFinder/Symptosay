import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

load_dotenv(find_dotenv())

DATABASE_SERVICE_DB = os.getenv("DATABASE_SERVICE_DB")

if not DATABASE_SERVICE_DB:
    raise ValueError("Missing database URLs")

symptoms_engine = create_async_engine(DATABASE_SERVICE_DB, echo=True)

session = sessionmaker(symptoms_engine, class_=AsyncSession, expire_on_commit=False)
