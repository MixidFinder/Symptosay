from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database import get_db
from app.schemas.symptoms import SymptomCreate, SymptomOut, SymptomsBatchCreate
from app.models.symptoms import Symptom
from app.crud import symptoms as crud_symptoms
from sqlalchemy import select

router = APIRouter()

@router.post("", response_model=SymptomOut)
async def create_symptom(symptom: SymptomCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_symptoms.create_symptom(db, symptom)

@router.get("", response_model=list[SymptomOut])
async def read_symptoms(skip: int = 0, limit: int = 100, db: Annotated[AsyncSession, Depends(get_db)] = None):
    return await crud_symptoms.get_symptoms(db, skip, limit)

@router.get("/{symptom_name}", response_model=SymptomOut)
async def get_symptom_by_name(symptom_name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    symptom = await crud_symptoms.get_by_name(db, symptom_name)
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom

@router.post("/batch", response_model=list[SymptomOut])
async def create_symptoms_batch(batch: SymptomsBatchCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_symptoms.create_symptoms_batch(db, batch)

@router.delete("/{symptom_id}", response_model=SymptomOut)
async def delete_symptom(symptom_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Symptom).where(Symptom.id == symptom_id)
    result = await db.execute(stmt)
    symptom = result.scalar_one_or_none()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")

    await db.delete(symptom)
    await db.commit()
    return symptom

@router.patch("/{symptom_id}", response_model=SymptomOut)
async def patch_symptom(symptom_id: int, payload: SymptomCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Symptom).where(Symptom.id == symptom_id)
    result = await db.execute(stmt)
    symptom = result.scalar_one_or_none()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")

    symptom.name = payload.name
    symptom.description = payload.description

    await db.commit()
    await db.refresh(symptom)
    return symptom
