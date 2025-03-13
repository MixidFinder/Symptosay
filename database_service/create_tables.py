import asyncio
from app.database import symptoms_engine, user_symptoms_engine
from app.models.symptoms import SymptomsBase
from app.models.user_symptoms import UserSymptomsBase
from app.models.diseases import DiseasesBase

async def create_all_tables():
    async with symptoms_engine.begin() as conn:
        await conn.run_sync(SymptomsBase.metadata.create_all)
        await conn.run_sync(DiseasesBase.metadata.create_all)
    async with user_symptoms_engine.begin() as conn:
        await conn.run_sync(UserSymptomsBase.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_all_tables())
