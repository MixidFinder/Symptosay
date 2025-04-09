import logging
import os

from dotenv import find_dotenv, load_dotenv

from . import connection

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

DATABASE_SERVICE_URL = os.getenv("DATABASE_SERVICE_URL")


async def get_symptom_by_name(symptom: str):
    await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/symptoms/{symptom}")


async def get_symptoms(pagination: dict[str, int]):
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/symptoms", data=pagination)


async def add_symptoms(symptoms: list[dict]):
    await connection.request_service(method="put", url=f"{DATABASE_SERVICE_URL}/api/symptoms", data=symptoms)


async def add_diseases(diseases: list[dict]):
    await connection.request_service(method="put", url=f"{DATABASE_SERVICE_URL}/api/diseases", data=diseases)


async def get_diseases():
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases")


async def get_disease_by_name(disease: str):
    await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease}")


async def del_symptoms(symptoms: list[dict]):
    await connection.request_service(method="delete", url=f"{DATABASE_SERVICE_URL}/api/symptoms", data=symptoms)


async def del_diseases(diseases: list[dict]):
    await connection.request_service(method="delete", url=f"{DATABASE_SERVICE_URL}/api/diseases", data=diseases)
