import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import diseases as crud_diseases
from app.database import get_db
from app.models.diseases import Disease
from app.schemas.diseases import DiseaseBase, DiseaseOut

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("", response_model=Page[DiseaseOut])
async def read_diseases(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_diseases.get_diseases(db)


@router.put("", response_model=list[DiseaseOut])
async def create_disease(disease: list[DiseaseBase], db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_diseases.create_disease(db, disease)


@router.get("/{disease_id}", response_model=DiseaseOut)
async def get_disease(disease_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Disease).where(Disease.id == disease_id)
    result = await db.execute(stmt)
    disease = result.scalar_one_or_none()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease


@router.patch("/{disease_id}", response_model=DiseaseOut)
async def patch_disease(disease_id: int, payload: DiseaseBase, db: Annotated[AsyncSession, Depends(get_db)]):
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


@router.post("/{disease_id}/symptoms/{symptom_id}")
async def add_symptom_to_disease(disease_id: int, symptom_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await crud_diseases.add_symptom(db, disease_id, symptom_id)
    return {"status": "ok"}


@router.get("/{disease_id}/symptoms")
async def get_disease_symptoms(disease_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_diseases.get_disease_symptoms(db, disease_id)


@router.delete("")
async def delete_diseases(request: list[DiseaseBase], db: Annotated[AsyncSession, Depends(get_db)]):
    diseases = [disease.name for disease in request]
    logger.debug("Diseases: %s", diseases)

    if not diseases:
        raise HTTPException(status_code=400, detail="List symptoms empty")
    try:
        await db.execute(delete(Disease).where(Disease.name.in_(diseases)))
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {e}") from Exception
