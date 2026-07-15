"""Preview API router."""

import httpx
from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.node_client import get_node_client

router = APIRouter(prefix="/preview", tags=["preview"])


@router.get("/node-available")
async def check_node_available() -> dict[str, Any]:
    """Check if Node.js is available."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/preview/node-available")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/start")
async def start_preview(body: dict[str, Any]) -> dict[str, Any]:
    """Start a preview server."""
    if "taskId" not in body or "workDir" not in body:
        raise HTTPException(status_code=400, detail="taskId and workDir are required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/preview/start", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/stop")
async def stop_preview(body: dict[str, Any]) -> dict[str, Any]:
    """Stop a preview server."""
    if "taskId" not in body:
        raise HTTPException(status_code=400, detail="taskId is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/preview/stop", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/status/{task_id}")
async def get_preview_status(task_id: str) -> dict[str, Any]:
    """Get preview server status."""
    node_client = get_node_client()
    try:
        response = await node_client.get(f"/preview/status/{task_id}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/stop-all")
async def stop_all_previews() -> dict[str, Any]:
    """Stop all preview servers."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/preview/stop-all")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
