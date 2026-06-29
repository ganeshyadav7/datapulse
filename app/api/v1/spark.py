"""Spark monitoring simulation endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.core.security import require_roles
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.spark_job import SparkJobCreate, SparkJobRead, SparkSummary
from app.services import spark_service
from app.services.spark_integration import run_sample_spark_job

router = APIRouter(prefix="/api/v1/spark", tags=["spark"])


@router.post("/jobs", response_model=SparkJobRead, status_code=status.HTTP_201_CREATED)
def create_spark_job(
    payload: SparkJobCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
    try:
        return spark_service.create_job(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Spark app_id already exists",
        ) from exc


@router.get("/jobs", response_model=list[SparkJobRead])
def list_spark_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return spark_service.list_jobs(db, skip=skip, limit=limit)


@router.get("/summary", response_model=SparkSummary)
def get_spark_summary(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return spark_service.summarize_spark(db)


@router.post("/sample-job", response_model=SparkJobRead, status_code=status.HTTP_201_CREATED)
def run_sample_job(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
    payload = run_sample_spark_job()
    try:
        return spark_service.create_job(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Spark sample app_id already exists",
        ) from exc


@router.get("/jobs/{job_id}", response_model=SparkJobRead)
def get_spark_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    job = spark_service.get_job(db, job_id)
    if job is None:
        raise not_found("SparkJob", job_id)
    return job
