"""Sandbox API router - proxies to Node.js service."""

import httpx
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.services.node_client import get_node_client
from app.utils.sse import create_sse_response

router = APIRouter(prefix="/sandbox", tags=["sandbox"])


@router.get("/available")
async def check_available() -> dict[str, Any]:
    """Check if sandbox is available on this platform."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/sandbox/available")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/images")
async def get_images() -> dict[str, Any]:
    """Get available sandbox images."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/sandbox/images")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/exec")
async def exec_command(request: dict[str, Any]) -> dict[str, Any]:
    """Execute a command in sandbox."""
    if "command" not in request:
        raise HTTPException(status_code=400, detail="Command is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/sandbox/exec", json=request)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Return error response from Node.js service
        return e.response.json()


@router.post("/run/file")
async def run_file(request: dict[str, Any]) -> dict[str, Any]:
    """Run a script file in sandbox with auto-detected runtime."""
    if "filePath" not in request or "workDir" not in request:
        raise HTTPException(status_code=400, detail="filePath and workDir are required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/sandbox/run/file", json=request)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return e.response.json()


@router.post("/run/node")
async def run_node(request: dict[str, Any]) -> dict[str, Any]:
    """Run a Node.js script content in sandbox."""
    if "script" not in request:
        raise HTTPException(status_code=400, detail="Script content is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/sandbox/run/node", json=request)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return e.response.json()


@router.post("/exec/stream")
async def exec_stream(request: dict[str, Any]) -> StreamingResponse:
    """Stream execution output (for long-running commands)."""
    if "command" not in request:
        raise HTTPException(status_code=400, detail="Command is required")

    node_client = get_node_client()

    async def stream_exec() -> AsyncGenerator[dict[str, Any], None]:
        async for event in node_client.proxy_sse("/sandbox/exec/stream", request):
            yield event

    return create_sse_response(stream_exec())


@router.post("/stop-all")
async def stop_all() -> dict[str, Any]:
    """Stop all sandbox providers."""
    node_client = get_node_client()
    try:
        response = await node_client.post("/sandbox/stop-all")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/debug/codex-paths")
async def debug_codex_paths() -> dict[str, Any]:
    """Debug endpoint to check codex paths."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/sandbox/debug/codex-paths")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
