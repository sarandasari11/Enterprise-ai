"""Application entry point for the enterprise AI backend."""

from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.routes.auth import router as auth_router


def create_app() -> FastAPI:
    """Create the FastAPI application instance and include the auth routes."""
    app = FastAPI(title="Enterprise AI Agent")
    app.include_router(auth_router)
    return app
