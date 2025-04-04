import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomBase, SymptomsBatchCreate

logger = logging.getLogger(__name__)


async def create_symptom(db: AsyncSession, request: list[SymptomBase]):
    logger.info("Get new symptoms: %s", request)
    try:
        symptoms = [Symptom(**symptom.model_dump()) for symptom in request]
        logger.info("DB symptoms: %s", symptoms)
        db.add_all(symptoms)
        await db.commit()
        for symptom in symptoms:
            await db.refresh(symptom)
    except IntegrityError as ie:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Symptom already exists") from ie
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from Exception
    else:
        return symptoms


async def get_symptoms(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Symptom).offset(skip).limit(limit))
    return result.scalars().all()


async def create_symptoms_batch(db: AsyncSession, batch: SymptomsBatchCreate):
    created = []
    for name in batch.names:
        s = Symptom(name=name)
        db.add(s)
        created.append(s)
    try:
        await db.commit()
        for i in created:
            await db.refresh(i)
        return created
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="One or more symptoms already exist")


async def get_by_name(db: AsyncSession, name: str):
    stmt = select(Symptom).where(Symptom.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
