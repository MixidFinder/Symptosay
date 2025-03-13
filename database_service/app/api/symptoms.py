from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database import symptoms_session
from app.schemas.symptoms import SymptomCreate, SymptomOut, SymptomsBatchCreate
from app.crud import symptoms as crud_symptoms

router = APIRouter()

async def get_symptoms_db() -> AsyncSession:
    async with symptoms_session() as session:
        yield session

@router.post("", response_model=SymptomOut)
async def create_symptom(symptom: SymptomCreate, db: Annotated[AsyncSession, Depends(get_symptoms_db)]) -> SymptomOut:
    new_symptom = await crud_symptoms.create_symptom(db, symptom)
    return new_symptom

@router.get("", response_model=list[SymptomOut])
async def read_symptoms(skip: int = 0, limit: int = 100, db: Annotated[AsyncSession, Depends(get_symptoms_db)] = None) -> list[SymptomOut]:
    symptoms_list = await crud_symptoms.get_symptoms(db, skip, limit)
    return symptoms_list

@router.get("/{symptom_name}", response_model=SymptomOut)
async def get_symptom_by_name(symptom_name: str, db: Annotated[AsyncSession, Depends(get_symptoms_db)]) -> SymptomOut:
    symptom = await crud_symptoms.get_by_name(db, symptom_name)
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom

@router.post("/batch", response_model=list[SymptomOut])
async def create_symptoms_batch(batch: SymptomsBatchCreate, db: Annotated[AsyncSession, Depends(get_symptoms_db)]) -> list[SymptomOut]:
    created = await crud_symptoms.create_symptoms_batch(db, batch)
    return created
