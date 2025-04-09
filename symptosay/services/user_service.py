import os

from dotenv import find_dotenv, load_dotenv

from services import connection

load_dotenv(find_dotenv())

DATABASE_SERVICE_URL = os.getenv("DATABASE_SERVICE_URL")


async def record_user_symptom(symptom: dict[str, str]):
    await connection.request_service(method="post", url=f"{DATABASE_SERVICE_URL}/api/user-symptoms", data=symptom)


async def delete_user_symptom(symptom: str):
    await connection.request_service(method="delete", url=f"{DATABASE_SERVICE_URL}/api/user-service/{symptom}")


async def change_user_symptom(symptom: str, data: dict[str, str]):
    await connection.request_service(
        method="patch", url=f"{DATABASE_SERVICE_URL}/api/user-symptoms/{symptom}", data=data
    )
