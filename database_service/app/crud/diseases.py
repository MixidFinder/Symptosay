from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.diseases import Disease, disease_symptom
from app.models.symptoms import Symptom
from app.schemas.diseases import DiseaseCreate

async def create_disease(db: AsyncSession, disease: DiseaseCreate) -> Disease:
    new_disease = Disease(name=disease.name, description=disease.description)
    db.add(new_disease)
    await db.commit()
    await db.refresh(new_disease)
    return new_disease

async def get_diseases(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Disease).offset(skip).limit(limit))
    return result.scalars().all()

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
    stmt = select(Symptom).join(disease_symptom, Symptom.id == disease_symptom.c.symptom_id).where(disease_symptom.c.disease_id == disease_id)
    result = await db.execute(stmt)
    return result.scalars().all()
