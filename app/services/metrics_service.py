"""Cross-domain metrics service."""

from sqlalchemy.orm import Session

from app.services.airflow_service import summarize_airflow
from app.services.data_quality_service import summarize_data_quality
from app.services.pipeline_service import summarize_runs
from app.services.spark_service import summarize_spark
from app.schemas.metrics import MetricsOverview


def get_metrics_overview(db: Session) -> MetricsOverview:
    pipeline = summarize_runs(db)
    airflow = summarize_airflow(db)
    spark = summarize_spark(db)
    data_quality = summarize_data_quality(db)
    return MetricsOverview(
        total_pipeline_runs=pipeline.total_runs,
        successful_runs=pipeline.successful_runs,
        failed_runs=pipeline.failed_runs,
        average_duration_seconds=pipeline.average_duration_seconds,
        total_records_processed=pipeline.total_records_processed,
        airflow_sla_misses=airflow.sla_misses,
        failed_spark_jobs=spark.failed_jobs,
        failed_data_quality_checks=data_quality.failed_checks,
    )
