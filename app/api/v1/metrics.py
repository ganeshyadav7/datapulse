"""Metrics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.metrics import MetricsOverview
from app.services.metrics_service import get_metrics_overview

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/overview", response_model=MetricsOverview)
def metrics_overview(db: Session = Depends(get_db)):
    return get_metrics_overview(db)
