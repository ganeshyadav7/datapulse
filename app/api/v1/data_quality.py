"""Data quality monitoring endpoints."""

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.core.security import require_roles
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.data_quality_check import (
    DataQualityCheckCreate,
    DataQualityCheckRead,
    DataQualitySummary,
)
from app.services import data_quality_service
from app.services.great_expectations_service import validate_records

router = APIRouter(prefix="/api/v1/data-quality", tags=["data-quality"])


class ValidationRequest(BaseModel):
    dataset_name: str
    records: list[dict[str, object]]


@router.post("/checks", response_model=DataQualityCheckRead, status_code=status.HTTP_201_CREATED)
def create_data_quality_check(
    payload: DataQualityCheckCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
    return data_quality_service.create_check(db, payload)


@router.get("/checks", response_model=list[DataQualityCheckRead])
def list_data_quality_checks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return data_quality_service.list_checks(db, skip=skip, limit=limit)


@router.get("/summary", response_model=DataQualitySummary)
def get_data_quality_summary(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return data_quality_service.summarize_data_quality(db)


@router.post("/validate")
def validate_dataset(
    payload: ValidationRequest,
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
) -> dict[str, object]:
    inferred_schema: dict[str, type] = {}
    for record in payload.records:
        for key, value in record.items():
            if value is not None and key not in inferred_schema:
                inferred_schema[key] = type(value)
    report = validate_records(payload.records, inferred_schema)
    report["dataset_name"] = payload.dataset_name
    return report


@router.get("/checks/{check_id}", response_model=DataQualityCheckRead)
def get_data_quality_check(
    check_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    check = data_quality_service.get_check(db, check_id)
    if check is None:
        raise not_found("DataQualityCheck", check_id)
    return check
