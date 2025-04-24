import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import symptoms as crud_symptoms
from app.database import get_db
from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomBase, SymptomOut

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("", response_model=Page[SymptomOut])
async def read_symptoms(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_symptoms.get_symptoms(db)


@router.get("/all", response_model=list[SymptomOut])
async def get_symptoms_all(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud_symptoms.get_symptoms_all(db)


@router.put("", response_model=list[SymptomOut])
async def create_symptom(symptom: list[SymptomBase], db: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Create symptoms %s", symptom)
    return await crud_symptoms.create_symptom(db, symptom)


@router.get("/{symptom_id}", response_model=SymptomOut)
async def get_symptom(symptom_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(Symptom).where(Symptom.id == symptom_id)
    result = await db.execute(stmt)
    symptom = result.scalar_one_or_none()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom


@router.patch("/{symptom_id}", response_model=SymptomOut)
async def patch_symptom(symptom_id: int, payload: SymptomBase, db: Annotated[AsyncSession, Depends(get_db)]):
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


@router.delete("")
async def delete_symptoms(request: list[SymptomBase], db: Annotated[AsyncSession, Depends(get_db)]):
    symptoms = [symptom.name for symptom in request]
    logger.debug("Symptoms: %s", symptoms)

    if not symptoms:
        raise HTTPException(status_code=400, detail="List symptoms empty")
    try:
        await db.execute(delete(Symptom).where(Symptom.name.in_(symptoms)))
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {e}") from Exception
