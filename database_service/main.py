# Импорт необходимых библиотек и модулей
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import AsyncGenerator, List
import uvicorn
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

# Импортируем фабрики сессий из файла database.py
from database import (
    users_session,        # Для подключения к базе db_users
    symptoms_session,     # Для подключения к базе db_symptoms
    user_symptoms_session # Для подключения к базе db_users_symptoms
)

# Импортируем модели из соответствующих файлов
# Если в этом файле нужно работать с User — берём user_models
from user_models import User
from symptoms_models import Symptom
from user_symptoms_models import UserSymptom

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Database Service")

# Добавляем CORS middleware (если требуется, для поддержки кросс-доменных запросов)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или укажите список разрешенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Зависимости для подключения к БД (FastAPI) ---
async def get_users_db() -> AsyncGenerator[AsyncSession, None]:
    async with users_session() as session:
        yield session

async def get_symptoms_db() -> AsyncGenerator[AsyncSession, None]:
    async with symptoms_session() as session:
        yield session

async def get_user_symptoms_db() -> AsyncGenerator[AsyncSession, None]:
    async with user_symptoms_session() as session:
        yield session

# --- Pydantic-модели для пользователей (db_users) ---
class UserCreate(BaseModel):
    username: str
    password: str  # В реальном проекте храните пароль в зашифрованном виде

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# --- Pydantic-модели для справочника симптомов (db_symptoms) ---
class SymptomCreate(BaseModel):
    name: str
    description: str | None = None

class SymptomOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True

# --- Pydantic-модели для пользовательских записей симптомов (db_users_symptoms) ---
class UserSymptomCreate(BaseModel):
    user_id: int
    symptom_id: int

class UserSymptomOut(BaseModel):
    id: int
    user_id: int
    symptom_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

class UserSymptomUpdate(BaseModel):
    new_symptom_id: int


# --- Эндпойнты для работы с пользователями (db_users) ---
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_users_db)):
    # Проверяем, существует ли уже пользователь с таким именем
    stmt = select(User).where(User.username == user.username)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_users_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# --- Эндпойнты для справочника симптомов (db_symptoms) ---
@app.post("/symptoms/", response_model=SymptomOut)
async def create_symptom(symptom: SymptomCreate, db: AsyncSession = Depends(get_symptoms_db)):
    new_symptom = Symptom(name=symptom.name, description=symptom.description)
    db.add(new_symptom)
    await db.commit()
    await db.refresh(new_symptom)
    return new_symptom

@app.get("/symptoms/", response_model=List[SymptomOut])
async def read_symptoms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_symptoms_db)):
    result = await db.execute(select(Symptom).offset(skip).limit(limit))
    return result.scalars().all()

# --- Эндпойнты для пользовательских записей симптомов (db_users_symptoms) ---
@app.post("/user-symptoms/", response_model=UserSymptomOut)
async def record_user_symptom(record: UserSymptomCreate, db: AsyncSession = Depends(get_user_symptoms_db)):
    new_record = UserSymptom(
        user_id=record.user_id,
        symptom_id=record.symptom_id,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

@app.get("/user-symptoms/{user_id}", response_model=List[UserSymptomOut])
async def read_user_symptoms(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_user_symptoms_db)
):
    stmt = select(UserSymptom).where(UserSymptom.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@app.put("/user-symptoms/{record_id}", response_model=UserSymptomOut)
async def update_user_symptom(
    record_id: int,
    update: UserSymptomUpdate,
    db: AsyncSession = Depends(get_user_symptoms_db)
):
    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if not user_symptom:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    user_symptom.symptom_id = update.new_symptom_id
    await db.commit()
    await db.refresh(user_symptom)
    return user_symptom

@app.delete("/user-symptoms/{record_id}", response_model=UserSymptomOut)
async def delete_user_symptom(record_id: int, db: AsyncSession = Depends(get_user_symptoms_db)):
    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if not user_symptom:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    await db.delete(user_symptom)
    await db.commit()
    return user_symptom

# --- Базовый эндпойнт для проверки работы сервиса ---
@app.get("/")
async def read_root():
    return {"message": "Database Service работает!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
