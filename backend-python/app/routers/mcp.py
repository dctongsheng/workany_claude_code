"""MCP API router."""

import httpx
from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.node_client import get_node_client

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.get("/config")
async def get_mcp_config() -> dict[str, Any]:
    """Get MCP configuration."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/mcp/config")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/config")
async def update_mcp_config(body: dict[str, Any]) -> dict[str, Any]:
    """Update MCP configuration."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/mcp/config", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/path")
async def get_mcp_path() -> dict[str, Any]:
    """Get MCP configuration file path."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/mcp/path")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/all-configs")
async def get_all_mcp_configs() -> dict[str, Any]:
    """Get all MCP configurations."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/mcp/all-configs")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
