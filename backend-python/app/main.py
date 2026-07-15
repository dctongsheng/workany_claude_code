"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import agent, files, health, mcp, preview, providers, sandbox
from app.services.node_client import close_node_client

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_node_client()


app = FastAPI(
    title=settings.app_name,
    description="WorkAny AI Agent Backend API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(agent.router)
app.include_router(sandbox.router)
app.include_router(providers.router)
app.include_router(files.router)
app.include_router(preview.router)
app.include_router(mcp.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"name": settings.app_name, "version": "0.1.0"}
