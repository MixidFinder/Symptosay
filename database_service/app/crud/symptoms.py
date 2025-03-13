from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomCreate, SymptomsBatchCreate

async def create_symptom(db: AsyncSession, symptom: SymptomCreate) -> Symptom:
    new_symptom = Symptom(name=symptom.name, description=symptom.description)
    db.add(new_symptom)
    await db.commit()
    await db.refresh(new_symptom)
    return new_symptom

async def get_symptoms(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Symptom]:
    result = await db.execute(select(Symptom).offset(skip).limit(limit))
    return result.scalars().all()

async def create_symptoms_batch(db: AsyncSession, batch: SymptomsBatchCreate) -> list[Symptom]:
    names = [x.strip() for x in batch.names.split(",") if x.strip()]
    created = []
    for name in names:
        s = Symptom(name=name)
        db.add(s)
        created.append(s)
    await db.commit()
    for i in created:
        await db.refresh(i)
    return created

async def get_by_name(db: AsyncSession, name: str) -> Symptom | None:
    stmt = select(Symptom).where(Symptom.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
