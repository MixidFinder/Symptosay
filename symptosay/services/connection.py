import logging
from typing import Any

from httpx import AsyncClient, HTTPStatusError

logger = logging.getLogger(__name__)


async def request_service(method: str, url: str, data: dict[str, Any] | None = None):
    logger.info("Request to %s, method: %s", url, method.upper())
    try:
        async with AsyncClient() as session:
            client_method = getattr(session, method.lower())

            if method.lower() in ["put", "post", "patch"]:
                response = await client_method(url=url, json=data, timeout=5)
            else:
                response = await client_method(url=url, timeout=5)

            response.raise_for_status()
            return response.json()
    except HTTPStatusError:
        return None
    except AttributeError:
        logger.exception("Invalid HTTP method: %s", method.upper())
        return None
