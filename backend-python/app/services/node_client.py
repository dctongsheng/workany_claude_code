"""Node.js service client for proxying AI/Sandbox requests."""

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

import httpx
from httpx_sse import aconnect_sse

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class NodeClient:
    """Client for proxying requests to the Node.js service."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.node_service_url
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 minutes timeout for long operations

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def get(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make a GET request to the Node.js service."""
        url = f"{self.base_url}{path}"
        logger.debug(f"GET {url}")
        response = await self.client.get(url, **kwargs)
        return response

    async def post(self, path: str, **kwargs: Any) -> httpx.Response:
        """Make a POST request to the Node.js service."""
        url = f"{self.base_url}{path}"
        logger.debug(f"POST {url}")
        response = await self.client.post(url, **kwargs)
        return response

    async def proxy_json(self, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Proxy a JSON request and return the JSON response."""
        response = await self.post(path, json=data)
        response.raise_for_status()
        return response.json()

    async def proxy_sse(
        self, path: str, data: dict[str, Any] | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Proxy an SSE stream and yield parsed JSON events."""
        url = f"{self.base_url}{path}"
        logger.debug(f"SSE {url}")

        async with aconnect_sse(
            self.client, "POST", url, json=data or {}
        ) as event_source:
            async for sse in event_source.aiter_sse():
                if sse.data:
                    try:
                        yield json.loads(sse.data)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse SSE data: {e}")
                        yield {"type": "error", "content": f"JSON parse error: {e}"}


# Global client instance
_node_client: NodeClient | None = None


def get_node_client() -> NodeClient:
    """Get or create the global Node.js client instance."""
    global _node_client
    if _node_client is None:
        _node_client = NodeClient()
    return _node_client


async def close_node_client() -> None:
    """Close the global Node.js client."""
    global _node_client
    if _node_client is not None:
        await _node_client.close()
        _node_client = None
