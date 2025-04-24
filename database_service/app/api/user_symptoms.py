from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user_symptoms as crud_user_symptoms
from app.database import get_db
from app.schemas.user_symptoms import UserSymptomCreate, UserSymptomOut, UserSymptomOutStr, UserSymptomUpdate

router = APIRouter()


@router.post("", response_model=UserSymptomOut)
async def record_user_symptom(record: UserSymptomCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_user_symptoms.record_user_symptom(db, record)


@router.get("/{user_id}", response_model=Page[UserSymptomOutStr])
async def read_user_symptoms(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_user_symptoms.get_user_symptoms(db, user_id)


@router.patch("/{record_id}", response_model=UserSymptomOut)
async def update_user_symptom(record_id: int, update: UserSymptomUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    updated = await crud_user_symptoms.update_user_symptom(db, record_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated


@router.delete("/{record_id}", response_model=UserSymptomOut)
async def delete_user_symptom(record_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    deleted = await crud_user_symptoms.delete_user_symptom(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return deleted
