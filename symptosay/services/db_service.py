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


async def get_diseases(pagination: dict[str, int]):
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases", data=pagination)


async def get_diseases_all():
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/all")


async def get_symptoms_all():
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/symptoms/all")


async def get_disease_by_name(disease: str):
    return await connection.request_service(method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease}")


async def del_symptoms(symptoms: list[dict]):
    await connection.request_service(method="delete", url=f"{DATABASE_SERVICE_URL}/api/symptoms", data=symptoms)


async def del_diseases(diseases: list[dict]):
    await connection.request_service(method="delete", url=f"{DATABASE_SERVICE_URL}/api/diseases", data=diseases)


async def get_disease_symptoms(disease_id: int, pagination: dict[str, int]):
    return await connection.request_service(
        method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease_id}/symptoms", data=pagination
    )


async def get_disease_symptoms_all(disease_id: int):
    return await connection.request_service(
        method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease_id}/symptoms/all"
    )


async def add_user_symptom(symptom_id: int, user_id: int, disease_id: int):
    await connection.request_service(
        method="post",
        url=f"{DATABASE_SERVICE_URL}/api/user-symptoms",
        data={"symptom_id": symptom_id, "user_id": user_id, "disease_id": disease_id},
    )


async def get_unlinked_symptom(disease_id: int, pagination: dict[str, int]):
    return await connection.request_service(
        method="get", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease_id}/symptoms/unlinked", data=pagination
    )


async def link_symptom(symptom_id: int, disease_id: int):
    await connection.request_service(
        method="post", url=f"{DATABASE_SERVICE_URL}/api/diseases/{disease_id}/symptoms/{symptom_id}"
    )
