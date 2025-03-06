from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database import user_symptoms_session
from app.schemas.user_symptoms import (
    UserSymptomCreate,
    UserSymptomOut,
    UserSymptomUpdate
)
from app.crud import user_symptoms as crud_user_symptoms

router = APIRouter()

async def get_user_symptoms_db() -> AsyncSession:

    async with user_symptoms_session() as session:
        yield session

@router.post("/", response_model=UserSymptomOut)
async def record_user_symptom(
    record: UserSymptomCreate,
    db: Annotated[AsyncSession, Depends(get_user_symptoms_db)]
) -> UserSymptomOut:

    new_record = await crud_user_symptoms.record_user_symptom(db, record)
    return new_record

@router.get("/{user_id}", response_model=list[UserSymptomOut])
async def read_user_symptoms(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Annotated[AsyncSession, Depends(get_user_symptoms_db)] = None
) -> list[UserSymptomOut]:

    records = await crud_user_symptoms.get_user_symptoms(db, user_id, skip,
                                                         limit)
    return records

@router.put("/{record_id}", response_model=UserSymptomOut)
async def update_user_symptom(
    record_id: int,
    update: UserSymptomUpdate,
    db: Annotated[AsyncSession, Depends(get_user_symptoms_db)]
) -> UserSymptomOut:

    updated = await crud_user_symptoms.update_user_symptom(db, record_id,
                                                           update)
    if not updated:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return updated

@router.delete("/{record_id}", response_model=UserSymptomOut)
async def delete_user_symptom(
    record_id: int,
    db: Annotated[AsyncSession, Depends(get_user_symptoms_db)]
) -> UserSymptomOut:

    deleted = await crud_user_symptoms.delete_user_symptom(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return deleted
