"""FastAPI application entrypoint for DataPulse."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models as _models  # noqa: F401
from app.api.v1 import airflow, auth, data_quality, health, metrics, pipeline_runs, spark
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import InMemoryRateLimitMiddleware, RequestContextMiddleware
from app.db.base import Base
from app.db.compat import ensure_sqlite_compatibility
from app.db.database import engine

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        Base.metadata.create_all(bind=engine)
        ensure_sqlite_compatibility(engine)
        yield

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Open-source observability for modern data pipelines.",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(InMemoryRateLimitMiddleware)
    application.add_middleware(RequestContextMiddleware)

    @application.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled_exception",
            extra={"request_id": getattr(request.state, "request_id", None)},
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    application.include_router(health.router)
    application.include_router(auth.router)
    application.include_router(pipeline_runs.router)
    application.include_router(airflow.router)
    application.include_router(spark.router)
    application.include_router(data_quality.router)
    application.include_router(metrics.router)
    return application


app = create_app()
