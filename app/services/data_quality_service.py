"""Data quality service logic."""

from sqlalchemy.orm import Session

from app.crud.data_quality_check import (
    create_data_quality_check,
    get_data_quality_check,
    list_data_quality_checks,
)
from app.models.data_quality_check import DataQualityCheck
from app.schemas.data_quality_check import DataQualityCheckCreate, DataQualitySummary


def evaluate_check_status(payload: DataQualityCheckCreate) -> str:
    """Infer a validation status using Great Expectations-style semantics."""
    if payload.status:
        return payload.status
    if payload.failed_records > 0:
        return "failed"
    return "success" if payload.actual_value == payload.expected_value else "failed"


def create_check(db: Session, payload: DataQualityCheckCreate) -> DataQualityCheck:
    data = payload.model_copy(update={"status": evaluate_check_status(payload)})
    return create_data_quality_check(db, data)


def list_checks(db: Session, skip: int = 0, limit: int = 100) -> list[DataQualityCheck]:
    return list_data_quality_checks(db, skip=skip, limit=limit)


def get_check(db: Session, check_id: int) -> DataQualityCheck | None:
    return get_data_quality_check(db, check_id)


def summarize_data_quality(db: Session) -> DataQualitySummary:
    checks = list_data_quality_checks(db, limit=10_000)
    total_failed_records = sum(check.failed_records for check in checks)
    total_records_checked = sum(check.total_records for check in checks)
    return DataQualitySummary(
        total_checks=len(checks),
        passed_checks=sum(check.status.lower() == "success" for check in checks),
        failed_checks=sum(check.status.lower() == "failed" for check in checks),
        warning_checks=sum(check.status.lower() == "warning" for check in checks),
        total_failed_records=total_failed_records,
        total_records_checked=total_records_checked,
        failure_rate=(
            round(total_failed_records / total_records_checked, 4) if total_records_checked else 0.0
        ),
    )
