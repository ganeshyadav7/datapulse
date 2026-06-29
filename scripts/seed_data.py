"""Seed the local DataPulse database with realistic demo records."""

import argparse
import random
import sys
from datetime import timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy.exc import IntegrityError  # noqa: E402

import app.models  # noqa: E402,F401
from app.db.base import Base  # noqa: E402
from app.db.compat import ensure_sqlite_compatibility  # noqa: E402
from app.db.database import engine  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.schemas.airflow_dag import AirflowDagRunCreate  # noqa: E402
from app.schemas.data_quality_check import DataQualityCheckCreate  # noqa: E402
from app.schemas.pipeline_run import PipelineRunCreate  # noqa: E402
from app.schemas.spark_job import SparkJobCreate  # noqa: E402
from app.services.airflow_service import create_airflow_dag_run  # noqa: E402
from app.services.data_quality_service import create_check  # noqa: E402
from app.services.pipeline_service import create_run  # noqa: E402
from app.services.spark_service import create_job  # noqa: E402
from app.utils.time import utc_now  # noqa: E402

PIPELINES = ["customer_load", "orders_ingest", "billing_export", "feature_build"]
DAGS = ["warehouse_refresh", "billing_export", "feature_store_sync", "fraud_signals"]
SPARK_JOBS = ["orders_compaction", "customer_features", "fraud_scoring", "session_rollups"]
DATASETS = ["orders", "customers", "payments", "events", "products"]


def generate_pipeline_runs(count: int) -> list[PipelineRunCreate]:
    now = utc_now()
    records = []
    for index in range(count):
        started = now - timedelta(minutes=index * 7)
        duration = random.randint(60, 3600)
        status = random.choices(["success", "failed", "running"], weights=[82, 14, 4])[0]
        ended = None if status == "running" else started + timedelta(seconds=duration)
        records.append(
            PipelineRunCreate(
                pipeline_name=f"{random.choice(PIPELINES)}_{index % 12}",
                pipeline_type=random.choice(["batch", "streaming", "dbt", "elt"]),
                status=status,
                started_at=started,
                ended_at=ended,
                duration_seconds=None if status == "running" else duration,
                records_processed=random.randint(1_000, 2_000_000),
                error_message="Source freshness threshold exceeded" if status == "failed" else None,
            )
        )
    return records


def generate_airflow_runs(count: int) -> list[AirflowDagRunCreate]:
    now = utc_now()
    records = []
    for index in range(count):
        started = now - timedelta(minutes=index * 15)
        duration = random.randint(120, 5400)
        failed_tasks = random.choice([0, 0, 0, 1, 2])
        status = "failed" if failed_tasks else random.choice(["success", "success", "running"])
        records.append(
            AirflowDagRunCreate(
                dag_id=random.choice(DAGS),
                run_id=f"scheduled__{now.date()}__{index}",
                status=status,
                execution_date=started,
                start_time=started,
                end_time=None if status == "running" else started + timedelta(seconds=duration),
                duration_seconds=None if status == "running" else duration,
                failed_tasks=failed_tasks,
                retry_count=random.randint(0, 3) if failed_tasks else random.choice([0, 0, 1]),
                sla_miss=duration > 3600 or failed_tasks > 0,
            )
        )
    return records


def generate_spark_jobs(count: int) -> list[SparkJobCreate]:
    now = utc_now()
    records = []
    for index in range(count):
        started = now - timedelta(minutes=index * 10)
        duration = random.randint(45, 4200)
        status = random.choices(["success", "failed", "running"], weights=[86, 10, 4])[0]
        input_records = random.randint(10_000, 10_000_000)
        output_records = 0 if status == "failed" else int(input_records * random.uniform(0.75, 1.0))
        records.append(
            SparkJobCreate(
                job_name=random.choice(SPARK_JOBS),
                app_id=f"application_datapulse_{index:05d}",
                status=status,
                start_time=started,
                end_time=None if status == "running" else started + timedelta(seconds=duration),
                duration_seconds=None if status == "running" else duration,
                input_records=input_records,
                output_records=output_records,
                executor_count=random.randint(2, 24),
                memory_used_mb=random.randint(1024, 65536),
                partitions=random.randint(4, 512),
                error_message="Executor lost" if status == "failed" else None,
            )
        )
    return records


def generate_quality_checks(count: int) -> list[DataQualityCheckCreate]:
    records = []
    for index in range(count):
        failed = random.choices([0, random.randint(1, 500)], weights=[80, 20])[0]
        total = random.randint(1_000, 1_000_000)
        records.append(
            DataQualityCheckCreate(
                dataset_name=random.choice(DATASETS),
                check_name=random.choice(
                    ["not_null", "unique_key", "schema_match", "accepted_values", "type_check"]
                ),
                check_type=random.choice(
                    [
                        "expect_column_values_to_not_be_null",
                        "expect_compound_columns_to_be_unique",
                        "expect_table_columns_to_match_set",
                        "expect_column_values_to_be_in_set",
                        "expect_column_values_to_be_of_type",
                    ]
                ),
                expected_value="validation passed",
                actual_value="validation passed" if failed == 0 else f"{failed} unexpected rows",
                failed_records=failed,
                total_records=total,
            )
        )
    return records


def insert_records(db, create_func, records) -> int:
    inserted = 0
    for record in records:
        try:
            create_func(db, record)
            inserted += 1
        except IntegrityError:
            db.rollback()
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed DataPulse demo data.")
    parser.add_argument("--pipeline-runs", type=int, default=500)
    parser.add_argument("--airflow-runs", type=int, default=100)
    parser.add_argument("--spark-jobs", type=int, default=200)
    parser.add_argument("--quality-checks", type=int, default=300)
    args = parser.parse_args()

    random.seed(42)
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_compatibility(engine)
    db = SessionLocal()
    try:
        inserted = {
            "pipeline_runs": insert_records(
                db, create_run, generate_pipeline_runs(args.pipeline_runs)
            ),
            "airflow_dag_runs": insert_records(
                db, create_airflow_dag_run, generate_airflow_runs(args.airflow_runs)
            ),
            "spark_jobs": insert_records(db, create_job, generate_spark_jobs(args.spark_jobs)),
            "data_quality_checks": insert_records(
                db, create_check, generate_quality_checks(args.quality_checks)
            ),
        }
    finally:
        db.close()
    print(f"Seeded DataPulse sample data: {inserted}")


if __name__ == "__main__":
    main()
