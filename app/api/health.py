"""Health check endpoints."""

from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=HealthResponse)
def root_health() -> HealthResponse:
    """Return application health from the root endpoint."""
    return HealthResponse(status="ok")


@router.get("/api/v1/health", response_model=HealthResponse)
def api_health() -> HealthResponse:
    """Return application health from the versioned API endpoint."""
    return HealthResponse(status="ok")

