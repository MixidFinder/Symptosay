import logging

from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomBase

logger = logging.getLogger(__name__)


async def create_symptom(db: AsyncSession, request: list[SymptomBase]):
    logger.info("Get new symptoms: %s", request)
    try:
        symptoms = [Symptom(**symptom.model_dump()) for symptom in request]
        logger.info("DB symptoms: %s", symptoms)
        db.add_all(symptoms)
        await db.commit()

    except IntegrityError as ie:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Symptom already exists") from ie
    except Exception as e:
        logger.debug("Exception: %s", e)
        raise HTTPException(status_code=500, detail="Db error") from Exception
    else:
        return symptoms


async def get_symptoms(db: AsyncSession):
    return await paginate(db, select(Symptom))


async def get_symptoms_all(db: AsyncSession):
    result = await db.execute(select(Symptom))
    return result.scalars().all()


async def get_by_name(db: AsyncSession, name: str):
    stmt = select(Symptom).where(Symptom.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
