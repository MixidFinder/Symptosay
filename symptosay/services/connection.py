import logging
from typing import Any

from httpx import AsyncClient

logger = logging.getLogger(__name__)


async def request_service(method: str, url: str, data: list[dict] | dict[str, Any] | None = None):
    logger.info("Request to %s, method: %s", url, method.upper())
    async with AsyncClient() as session:
        if method.lower() in ["put", "post", "patch", "delete"]:
            response = await session.request(method=method.lower(), url=url, json=data, timeout=5)
        else:
            response = await session.request(method=method.lower(), url=url, timeout=5)

        response.raise_for_status()
        return response.json()
