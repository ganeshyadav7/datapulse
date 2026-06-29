"""CRUD helpers for data quality checks."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_quality_check import DataQualityCheck
from app.schemas.data_quality_check import DataQualityCheckCreate


def create_data_quality_check(db: Session, payload: DataQualityCheckCreate) -> DataQualityCheck:
    check = DataQualityCheck(**payload.model_dump())
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


def list_data_quality_checks(
    db: Session, skip: int = 0, limit: int = 100
) -> list[DataQualityCheck]:
    statement = (
        select(DataQualityCheck)
        .order_by(DataQualityCheck.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_data_quality_check(db: Session, check_id: int) -> DataQualityCheck | None:
    return db.get(DataQualityCheck, check_id)
