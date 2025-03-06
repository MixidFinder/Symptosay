import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_symptoms import UserSymptom
from app.schemas.user_symptoms import UserSymptomCreate, UserSymptomUpdate

async def record_user_symptom(db: AsyncSession,
                              record: UserSymptomCreate) -> UserSymptom:

    new_record = UserSymptom(
        user_id=record.user_id,
        symptom_id=record.symptom_id,
        timestamp=datetime.datetime.utcnow(),
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

async def get_user_symptoms(db: AsyncSession,
                            user_id: int,
                            skip: int = 0,
                            limit: int = 100
                            ) -> list[UserSymptom]:

    stmt = (
        select(UserSymptom)
        .where(UserSymptom.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_user_symptom(db: AsyncSession,
                              record_id: int,
                              update: UserSymptomUpdate
                              ) -> UserSymptom | None:

    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if not user_symptom:
        return None
    user_symptom.symptom_id = update.new_symptom_id
    await db.commit()
    await db.refresh(user_symptom)
    return user_symptom

async def delete_user_symptom(db: AsyncSession,
                              record_id: int
                              ) -> UserSymptom | None:

    stmt = select(UserSymptom).where(UserSymptom.id == record_id)
    result = await db.execute(stmt)
    user_symptom = result.scalar_one_or_none()
    if not user_symptom:
        return None
    await db.delete(user_symptom)
    await db.commit()
    return user_symptom
