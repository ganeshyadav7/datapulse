"""Data quality monitoring endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.db.session import get_db
from app.schemas.data_quality_check import (
    DataQualityCheckCreate,
    DataQualityCheckRead,
    DataQualitySummary,
)
from app.services import data_quality_service

router = APIRouter(prefix="/api/v1/data-quality", tags=["data-quality"])


@router.post("/checks", response_model=DataQualityCheckRead, status_code=status.HTTP_201_CREATED)
def create_data_quality_check(payload: DataQualityCheckCreate, db: Session = Depends(get_db)):
    return data_quality_service.create_check(db, payload)


@router.get("/checks", response_model=list[DataQualityCheckRead])
def list_data_quality_checks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return data_quality_service.list_checks(db, skip=skip, limit=limit)


@router.get("/summary", response_model=DataQualitySummary)
def get_data_quality_summary(db: Session = Depends(get_db)):
    return data_quality_service.summarize_data_quality(db)


@router.get("/checks/{check_id}", response_model=DataQualityCheckRead)
def get_data_quality_check(check_id: int, db: Session = Depends(get_db)):
    check = data_quality_service.get_check(db, check_id)
    if check is None:
        raise not_found("DataQualityCheck", check_id)
    return check
