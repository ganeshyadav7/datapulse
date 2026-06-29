"""Cross-domain metrics schemas."""

from pydantic import BaseModel


class MetricsOverview(BaseModel):
    total_pipeline_runs: int
    successful_runs: int
    failed_runs: int
    average_duration_seconds: float
    total_records_processed: int
    airflow_sla_misses: int
    failed_spark_jobs: int
    failed_data_quality_checks: int
