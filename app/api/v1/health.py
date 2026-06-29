"""Health endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/")
def root_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/health/live")
def liveness() -> dict[str, str]:
    return {"status": "live"}


@router.get("/api/v1/health/ready")
def readiness(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "ok"}
