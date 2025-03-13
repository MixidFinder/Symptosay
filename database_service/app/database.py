import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

SYMPTOMS_DATABASE_URL = os.getenv("SYMPTOMS_DATABASE_URL")
USER_SYMPTOMS_DATABASE_URL = os.getenv("USER_SYMPTOMS_DATABASE_URL")

if not SYMPTOMS_DATABASE_URL or not USER_SYMPTOMS_DATABASE_URL:
    raise ValueError("Missing database URLs")

symptoms_engine = create_async_engine(SYMPTOMS_DATABASE_URL, echo=True)
user_symptoms_engine = create_async_engine(USER_SYMPTOMS_DATABASE_URL, echo=True)

symptoms_session = sessionmaker(symptoms_engine, class_=AsyncSession, expire_on_commit=False)
user_symptoms_session = sessionmaker(user_symptoms_engine, class_=AsyncSession, expire_on_commit=False)
