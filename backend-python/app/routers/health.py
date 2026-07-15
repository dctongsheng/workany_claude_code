"""Health check API router."""

import httpx
import time
from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.node_client import get_node_client

router = APIRouter(prefix="/health", tags=["health"])

# Track startup time
START_TIME = time.time()


@router.get("/")
async def health_check() -> dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "ok",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "uptime": time.time() - START_TIME,
    }


@router.get("/dependencies")
async def check_dependencies() -> dict[str, Any]:
    """Check all dependencies status."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/health/dependencies")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/dependencies/{dep_id}")
async def check_dependency(dep_id: str) -> dict[str, Any]:
    """Check a single dependency."""
    node_client = get_node_client()
    try:
        response = await node_client.get(f"/health/dependencies/{dep_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Dependency not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/dependencies/{dep_id}/install-commands")
async def get_install_commands(dep_id: str) -> dict[str, Any]:
    """Get install commands for a dependency."""
    node_client = get_node_client()
    try:
        response = await node_client.get(f"/health/dependencies/{dep_id}/install-commands")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Dependency not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/dependencies/{dep_id}/install")
async def install_dependency(dep_id: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Install a dependency."""
    node_client = get_node_client()
    try:
        response = await node_client.post(
            f"/health/dependencies/{dep_id}/install",
            json=body or {},
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Dependency not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
