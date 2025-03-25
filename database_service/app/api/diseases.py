from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import select

from app.database import get_db
from app.schemas.diseases import DiseaseCreate, DiseaseOut
from app.crud import diseases as crud_diseases
from app.models.diseases import Disease

router = APIRouter()


@router.post("", response_model=DiseaseOut)
async def create_disease(disease: DiseaseCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    new_disease = await crud_diseases.create_disease(db, disease)
    return new_disease


@router.get("", response_model=list[DiseaseOut])
async def read_diseases(skip: int = 0, limit: int = 100, db: Annotated[AsyncSession, Depends(get_db)] = None):
    items = await crud_diseases.get_diseases(db, skip, limit)
    return items


@router.post("/{disease_id}/symptoms/{symptom_id}")
async def add_symptom_to_disease(disease_id: int, symptom_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await crud_diseases.add_symptom(db, disease_id, symptom_id)
    return {"status": "ok"}


@router.get("/{disease_id}/symptoms")
async def get_disease_symptoms(disease_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_diseases.get_disease_symptoms(db, disease_id)


@router.delete("/{disease_id}", response_model=DiseaseOut)
async def delete_disease(disease_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Disease).where(Disease.id == disease_id)
    result = await db.execute(stmt)
    disease = result.scalar_one_or_none()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    await db.delete(disease)
    await db.commit()
    return disease


@router.patch("/{disease_id}", response_model=DiseaseOut)
async def patch_disease(disease_id: int, payload: DiseaseCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Disease).where(Disease.id == disease_id)
    result = await db.execute(stmt)
    disease = result.scalar_one_or_none()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    disease.name = payload.name
    disease.description = payload.description

    await db.commit()
    await db.refresh(disease)
    return disease
