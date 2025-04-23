import datetime

from fastapi import HTTPException
from sqlalchemy import and_, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diseases import disease_symptom
from app.models.user_symptoms import UserSymptom
from app.schemas.user_symptoms import UserSymptomCreate, UserSymptomUpdate


async def _symptom_belongs_to_disease(db: AsyncSession, disease_id: int, symptom_id: int) -> bool:
    stmt = select(
        exists().where(and_(disease_symptom.c.disease_id == disease_id, disease_symptom.c.symptom_id == symptom_id))
    )
    return await db.scalar(stmt)


async def record_user_symptom(db: AsyncSession, record: UserSymptomCreate):
    if record.disease_id is not None:
        ok = await _symptom_belongs_to_disease(db, record.disease_id, record.symptom_id)
        if not ok:
            raise HTTPException(status_code=400, detail="Symptom is not linked to the selected disease")
    new_record = UserSymptom(
        user_id=record.user_id,
        symptom_id=record.symptom_id,
        disease_id=record.disease_id,
        timestamp=datetime.datetime.utcnow(),
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record


async def get_user_symptoms(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    stmt = select(UserSymptom).where(UserSymptom.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_user_symptom(db: AsyncSession, record_id: int, update: UserSymptomUpdate):
    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    us = result.scalar_one_or_none()
    if not us:
        return None
    if update.new_disease_id is not None:
        ok = await _symptom_belongs_to_disease(db, update.new_disease_id, update.new_symptom_id)
        if not ok:
            raise HTTPException(status_code=400, detail="Symptom is not linked to the selected disease")
    us.symptom_id = update.new_symptom_id
    us.disease_id = update.new_disease_id
    await db.commit()
    await db.refresh(us)
    return us


async def delete_user_symptom(db: AsyncSession, record_id: int):
    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    us = result.scalar_one_or_none()
    if not us:
        return None
    await db.delete(us)
    await db.commit()
    return us
