"""Health endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}
