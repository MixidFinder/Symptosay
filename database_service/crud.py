from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime

from symptoms_models import Symptom
from user_symptoms_models import UserSymptom

# Функции для справочника симптомов (db_symptoms)

async def create_symptom(db: AsyncSession, name: str, description: str = None):
    
    symptom = Symptom(name=name, description=description)
    db.add(symptom)
    await db.commit()
    await db.refresh(symptom)
    return symptom

async def get_symptoms(db: AsyncSession, skip: int = 0, limit: int = 100):
    
    result = await db.execute(select(Symptom).offset(skip).limit(limit))
    return result.scalars().all()

# Функции для записей симптомов пользователей (db_users_symptoms)

async def record_user_symptom(db: AsyncSession, user_id: int, symptom_id: int):

    user_symptom = UserSymptom(
        user_id=user_id,
        symptom_id=symptom_id,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(user_symptom)
    await db.commit()
    await db.refresh(user_symptom)
    return user_symptom

async def get_user_symptoms(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):

    stmt = select(UserSymptom).where(UserSymptom.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_user_symptom(db: AsyncSession, record_id: int, new_symptom_id: int):

    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if user_symptom is None:
        return None
    user_symptom.symptom_id = new_symptom_id
    await db.commit()
    await db.refresh(user_symptom)
    return user_symptom

async def delete_user_symptom(db: AsyncSession, record_id: int):
 
    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if user_symptom is None:
        return None
    await db.delete(user_symptom)
    await db.commit()
    return user_symptom
