from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database import symptoms_session
from app.schemas.diseases import DiseaseCreate, DiseaseOut
from app.crud import diseases as crud_diseases

router = APIRouter()

async def get_db() -> AsyncSession:
    async with symptoms_session() as session:
        yield session

@router.post("", response_model=DiseaseOut)
async def create_disease(disease: DiseaseCreate, db: Annotated[AsyncSession, Depends(get_db)]) -> DiseaseOut:
    new_disease = await crud_diseases.create_disease(db, disease)
    return new_disease

@router.get("", response_model=list[DiseaseOut])
async def read_diseases(skip: int = 0, limit: int = 100, db: Annotated[AsyncSession, Depends(get_db)] = None) -> list[DiseaseOut]:
    items = await crud_diseases.get_diseases(db, skip, limit)
    return items

@router.post("/{disease_id}/symptoms/{symptom_id}")
async def add_symptom_to_disease(disease_id: int, symptom_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await crud_diseases.add_symptom(db, disease_id, symptom_id)
    return {"status": "ok"}

@router.get("/{disease_id}/symptoms")
async def get_disease_symptoms(disease_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_diseases.get_disease_symptoms(db, disease_id)
