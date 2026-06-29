"""Spark monitoring simulation service logic."""

from sqlalchemy.orm import Session

from app.crud.spark_job import create_spark_job, get_spark_job, list_spark_jobs
from app.models.spark_job import SparkJob
from app.schemas.spark_job import SparkJobCreate, SparkSummary


def create_job(db: Session, payload: SparkJobCreate) -> SparkJob:
    return create_spark_job(db, payload)


def list_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[SparkJob]:
    return list_spark_jobs(db, skip=skip, limit=limit)


def get_job(db: Session, job_id: int) -> SparkJob | None:
    return get_spark_job(db, job_id)


def summarize_spark(db: Session) -> SparkSummary:
    jobs = list_spark_jobs(db, limit=10_000)
    durations = [job.duration_seconds for job in jobs if job.duration_seconds is not None]
    return SparkSummary(
        total_jobs=len(jobs),
        successful_jobs=sum(job.status.lower() == "success" for job in jobs),
        failed_jobs=sum(job.status.lower() == "failed" for job in jobs),
        running_jobs=sum(job.status.lower() == "running" for job in jobs),
        total_input_records=sum(job.input_records for job in jobs),
        total_output_records=sum(job.output_records for job in jobs),
        average_duration_seconds=round(sum(durations) / len(durations), 2) if durations else 0.0,
    )
