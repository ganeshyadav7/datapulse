"""CRUD helpers for Spark jobs."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.spark_job import SparkJob
from app.schemas.spark_job import SparkJobCreate


def create_spark_job(db: Session, payload: SparkJobCreate) -> SparkJob:
    job = SparkJob(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def list_spark_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[SparkJob]:
    statement = select(SparkJob).order_by(SparkJob.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def get_spark_job(db: Session, job_id: int) -> SparkJob | None:
    return db.get(SparkJob, job_id)
