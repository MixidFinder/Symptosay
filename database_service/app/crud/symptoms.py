from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.symptoms import Symptom
from app.schemas.symptoms import SymptomCreate, SymptomsBatchCreate

async def create_symptom(db: AsyncSession, symptom: SymptomCreate) -> Symptom:

    new_symptom = Symptom(
        name=symptom.name,
        description=symptom.description,
    )
    db.add(new_symptom)
    await db.commit()
    await db.refresh(new_symptom)
    return new_symptom

async def get_symptoms(db: AsyncSession, skip: int = 0, limit: int = 100
                       ) -> list[Symptom]:

    result = await db.execute(
        select(Symptom).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_symptoms_batch(db: AsyncSession,
                                batch: SymptomsBatchCreate
                                ) -> list[Symptom]:

    names = [
        name.strip() for name in batch.names.split(",")
        if name.strip()
    ]
    created_symptoms = []
    for name in names:
        symptom = Symptom(name=name)
        db.add(symptom)
        created_symptoms.append(symptom)
    await db.commit()
    for symptom in created_symptoms:
        await db.refresh(symptom)
    return created_symptoms
