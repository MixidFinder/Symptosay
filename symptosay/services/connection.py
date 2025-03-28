import logging
from typing import Any

from httpx import AsyncClient, HTTPStatusError

logger = logging.getLogger(__name__)


async def get_service(url: str):
    logger.info("Get request to url: %s", url)
    try:
        async with AsyncClient() as session:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError:
        return None


async def post_service(url: str, data: dict[str, Any]):
    logger.info("Post request to url: %s", url)
    try:
        async with AsyncClient() as session:
            response = await session.post(url=url, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError:
        return None


async def patch_service(url: str, data: dict[str, Any]):
    logger.info("Patch request to url: %s", url)
    try:
        async with AsyncClient() as session:
            response = await session.patch(url=url, json=data, timeout=5)
            response.raise_for_status()
            return response.json()
    except HTTPStatusError:
        return None
