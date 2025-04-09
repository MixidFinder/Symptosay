import logging

from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diseases import Disease, disease_symptom
from app.models.symptoms import Symptom
from app.schemas.diseases import DiseaseBase

logger = logging.getLogger(__name__)


async def create_disease(db: AsyncSession, request: list[DiseaseBase]):
    logger.info("Get new diseases: %s", request)
    try:
        diseases = [Disease(**disease.model_dump()) for disease in request]
        logger.info("DB diseases: %s", diseases)
        db.add_all(diseases)
        await db.commit()

    except IntegrityError as ie:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Disease already exists") from ie
    except Exception as e:
        logger.debug("Exception: %s", e)
        raise HTTPException(status_code=500, detail="Db error") from Exception
    else:
        return diseases


async def get_diseases(db: AsyncSession):
    return await paginate(db, select(Disease))


async def add_symptom(db: AsyncSession, disease_id: int, symptom_id: int):
    stmt_d = select(Disease).where(Disease.id == disease_id)
    stmt_s = select(Symptom).where(Symptom.id == symptom_id)
    d_res = await db.execute(stmt_d)
    s_res = await db.execute(stmt_s)
    d = d_res.scalar_one_or_none()
    s = s_res.scalar_one_or_none()
    if not d or not s:
        return
    ds = disease_symptom.insert().values(disease_id=d.id, symptom_id=s.id)
    await db.execute(ds)
    await db.commit()


async def get_disease_symptoms(db: AsyncSession, disease_id: int):
    stmt = (
        select(Symptom)
        .join(disease_symptom, Symptom.id == disease_symptom.c.symptom_id)
        .where(disease_symptom.c.disease_id == disease_id)
    )
    return await paginate(db, stmt)
