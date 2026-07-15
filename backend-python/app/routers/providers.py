"""Providers API router."""

import httpx
from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.node_client import get_node_client

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/sandbox")
async def list_sandbox_providers() -> dict[str, Any]:
    """List all sandbox providers."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/providers/sandbox")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/sandbox/available")
async def list_available_sandbox() -> dict[str, Any]:
    """List available sandbox providers."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/providers/sandbox/available")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/sandbox/{provider_type}")
async def get_sandbox_provider(provider_type: str) -> dict[str, Any]:
    """Get sandbox provider details."""
    node_client = get_node_client()
    try:
        response = await node_client.get(f"/providers/sandbox/{provider_type}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Provider not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/sandbox/switch")
async def switch_sandbox_provider(body: dict[str, Any]) -> dict[str, Any]:
    """Switch sandbox provider."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/providers/sandbox/switch", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/agents")
async def list_agent_providers() -> dict[str, Any]:
    """List all agent providers."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/providers/agents")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/agents/available")
async def list_available_agents() -> dict[str, Any]:
    """List available agent providers."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/providers/agents/available")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/agents/{provider_type}")
async def get_agent_provider(provider_type: str) -> dict[str, Any]:
    """Get agent provider details."""
    node_client = get_node_client()
    try:
        response = await node_client.get(f"/providers/agents/{provider_type}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Provider not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/agents/switch")
async def switch_agent_provider(body: dict[str, Any]) -> dict[str, Any]:
    """Switch agent provider."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/providers/agents/switch", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/settings/sync")
async def sync_settings(body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Sync settings to backend."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/providers/settings/sync", json=body or {})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/config")
async def get_config() -> dict[str, Any]:
    """Get current provider configuration."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/providers/config")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
