"""Agent API router - proxies to Node.js service."""

import httpx
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.agent import AgentExecuteRequest, AgentPlanRequest, AgentRequest
from app.services.node_client import get_node_client
from app.utils.sse import create_sse_response

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/plan")
async def create_plan(request: AgentPlanRequest) -> StreamingResponse:
    """Create an execution plan (Phase 1).

    This endpoint creates a plan without executing it.
    Returns SSE stream with plan details.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    node_client = get_node_client()

    async def stream_plan() -> AsyncGenerator[dict[str, Any], None]:
        data = {"prompt": request.prompt}
        if request.model_config_data:
            data["modelConfig"] = request.model_config_data.model_dump(
                exclude_none=True, by_alias=True
            )
        async for event in node_client.proxy_sse("/agent/plan", data):
            yield event

    return create_sse_response(stream_plan())


@router.post("/execute")
async def execute_plan(request: AgentExecuteRequest) -> StreamingResponse:
    """Execute an approved plan (Phase 2).

    This endpoint executes a previously created plan.
    Returns SSE stream with execution progress.
    """
    if not request.plan_id:
        raise HTTPException(status_code=400, detail="planId is required")

    node_client = get_node_client()

    async def stream_execute() -> AsyncGenerator[dict[str, Any], None]:
        data: dict[str, Any] = {
            "planId": request.plan_id,
            "prompt": request.prompt,
        }
        if request.work_dir:
            data["workDir"] = request.work_dir
        if request.task_id:
            data["taskId"] = request.task_id
        if request.model_config_data:
            data["modelConfig"] = request.model_config_data.model_dump(
                exclude_none=True, by_alias=True
            )
        if request.sandbox_config:
            data["sandboxConfig"] = request.sandbox_config.model_dump(
                exclude_none=True, by_alias=True
            )
        if request.skills_config:
            data["skillsConfig"] = request.skills_config.model_dump(
                exclude_none=True, by_alias=True
            )
        if request.mcp_config:
            data["mcpConfig"] = request.mcp_config.model_dump(
                exclude_none=True, by_alias=True
            )
        async for event in node_client.proxy_sse("/agent/execute", data):
            yield event

    return create_sse_response(stream_execute())


@router.post("/")
async def run_agent(request: AgentRequest) -> StreamingResponse:
    """Direct agent execution (plan + execute in one call).

    This is the legacy endpoint that plans and executes in a single request.
    Returns SSE stream with execution progress.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    node_client = get_node_client()

    async def stream_agent() -> AsyncGenerator[dict[str, Any], None]:
        async for event in node_client.proxy_sse("/agent/", request.to_dict()):
            yield event

    return create_sse_response(stream_agent())


@router.post("/stop/{session_id}")
async def stop_agent(session_id: str) -> dict[str, str]:
    """Stop a running agent session."""
    node_client = get_node_client()

    try:
        response = await node_client.post(f"/agent/stop/{session_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Session not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> dict[str, Any]:
    """Get session status."""
    node_client = get_node_client()

    try:
        response = await node_client.get(f"/agent/session/{session_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Session not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/plan/{plan_id}")
async def get_plan(plan_id: str) -> dict[str, Any]:
    """Get plan details by ID."""
    node_client = get_node_client()

    try:
        response = await node_client.get(f"/agent/plan/{plan_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Plan not found")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
