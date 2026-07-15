"""Files API router."""

import httpx
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.node_client import get_node_client

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/readdir")
async def read_directory(body: dict[str, Any]) -> dict[str, Any]:
    """Recursively read directory contents."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/readdir", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/stat")
async def stat_path(body: dict[str, Any]) -> dict[str, Any]:
    """Check path status."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/stat", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/read")
async def read_file(body: dict[str, Any]) -> dict[str, Any]:
    """Read file contents."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/read", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/read-binary")
async def read_binary_file(body: dict[str, Any]) -> Response:
    """Read binary file contents."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/read-binary", json=body)
        response.raise_for_status()
        # Return raw bytes
        return Response(
            content=response.content,
            media_type=response.headers.get("content-type", "application/octet-stream"),
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/skills-dir")
async def get_skills_dir() -> dict[str, Any]:
    """Get skills directory path."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/files/skills-dir")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/detect-editor")
async def detect_editor() -> dict[str, Any]:
    """Detect code editor."""
    node_client = get_node_client()
    try:
        response = await node_client.get("/files/detect-editor")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/open-in-editor")
async def open_in_editor(body: dict[str, Any]) -> dict[str, Any]:
    """Open file in editor."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/open-in-editor", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/open")
async def open_file(body: dict[str, Any]) -> dict[str, Any]:
    """Open file with system default."""
    if "path" not in body:
        raise HTTPException(status_code=400, detail="path is required")

    node_client = get_node_client()
    try:
        response = await node_client.post("/files/open", json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
