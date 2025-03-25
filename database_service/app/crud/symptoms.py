from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomCreate, SymptomsBatchCreate
from fastapi import HTTPException

async def create_symptom(db: AsyncSession, symptom: SymptomCreate):
    new_symptom = Symptom(name=symptom.name, description=symptom.description)
    db.add(new_symptom)
    try:
        await db.commit()
        await db.refresh(new_symptom)
        return new_symptom
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Symptom already exists")

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
