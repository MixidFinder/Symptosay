from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

USERS_DATABASE_URL = os.getenv("USERS_DATABASE_URL")
SYMPTOMS_DATABASE_URL = os.getenv("SYMPTOMS_DATABASE_URL")
USER_SYMPTOMS_DATABASE_URL = os.getenv("USER_SYMPTOMS_DATABASE_URL")

if not (USERS_DATABASE_URL and SYMPTOMS_DATABASE_URL and USER_SYMPTOMS_DATABASE_URL):
    raise Exception("Не все переменные окружения для подключения к БД установлены.")

users_engine = create_async_engine(USERS_DATABASE_URL, echo=True)
symptoms_engine = create_async_engine(SYMPTOMS_DATABASE_URL, echo=True)
user_symptoms_engine = create_async_engine(USER_SYMPTOMS_DATABASE_URL, echo=True)

users_session = sessionmaker(users_engine, class_=AsyncSession, expire_on_commit=False)
symptoms_session = sessionmaker(symptoms_engine, class_=AsyncSession, expire_on_commit=False)
user_symptoms_session = sessionmaker(user_symptoms_engine, class_=AsyncSession, expire_on_commit=False)

class UsersBase(DeclarativeBase):
    pass

class SymptomsBase(DeclarativeBase):
    pass

class UserSymptomsBase(DeclarativeBase):
    pass
