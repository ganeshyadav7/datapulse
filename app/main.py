"""FastAPI application entrypoint for DataPulse."""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Lightweight data pipeline observability.",
    )
    application.include_router(health_router)
    return application


app = create_app()

