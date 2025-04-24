import logging
from typing import Any

from httpx import AsyncClient

logger = logging.getLogger(__name__)


async def request_service(method: str, url: str, data: list[dict] | dict[str, Any] | None = None):
    logger.info("Request to %s, method: %s, data: %s", url, method.upper(), data)
    async with AsyncClient() as session:
        if method.lower() == "get" and data:
            response = await session.request(method="get", url=url, params=data)
        elif method.lower() in ["put", "post", "patch", "delete"]:
            response = await session.request(method=method.lower(), url=url, json=data, timeout=5)
        else:
            response = await session.request(method=method.lower(), url=url, timeout=5)

        response.raise_for_status()
        return response.json()
