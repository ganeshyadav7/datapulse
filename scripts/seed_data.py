"""Seed the local DataPulse database with realistic demo records."""

from app.db.base import Base
from app.db.database import engine
from app.db.session import SessionLocal
import app.models  # noqa: F401
from sqlalchemy.exc import IntegrityError
from app.schemas.airflow_dag import AirflowDagRunCreate
from app.schemas.data_quality_check import DataQualityCheckCreate
from app.schemas.pipeline_run import PipelineRunCreate
from app.schemas.spark_job import SparkJobCreate
from app.services.airflow_service import create_airflow_dag_run
from app.services.data_quality_service import create_check
from app.services.pipeline_service import create_run
from app.services.spark_service import create_job
from app.utils.sample_data import (
    SAMPLE_AIRFLOW_DAG_RUNS,
    SAMPLE_DATA_QUALITY_CHECKS,
    SAMPLE_PIPELINE_RUNS,
    SAMPLE_SPARK_JOBS,
)


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for create_func, schema, records in (
            (create_run, PipelineRunCreate, SAMPLE_PIPELINE_RUNS),
            (create_airflow_dag_run, AirflowDagRunCreate, SAMPLE_AIRFLOW_DAG_RUNS),
            (create_job, SparkJobCreate, SAMPLE_SPARK_JOBS),
            (create_check, DataQualityCheckCreate, SAMPLE_DATA_QUALITY_CHECKS),
        ):
            for item in records:
                try:
                    create_func(db, schema(**item))
                except IntegrityError:
                    db.rollback()
    finally:
        db.close()
    print("Seeded DataPulse sample data.")


if __name__ == "__main__":
    main()
