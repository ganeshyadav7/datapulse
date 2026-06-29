"""FastAPI application entrypoint for DataPulse."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.v1 import airflow, data_quality, health, metrics, pipeline_runs, spark
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.database import engine
import app.models  # noqa: F401


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        Base.metadata.create_all(bind=engine)
        yield

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Open-source observability for modern data pipelines.",
        lifespan=lifespan,
    )
    application.include_router(health.router)
    application.include_router(pipeline_runs.router)
    application.include_router(airflow.router)
    application.include_router(spark.router)
    application.include_router(data_quality.router)
    application.include_router(metrics.router)
    return application


app = create_app()
