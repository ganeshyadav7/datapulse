"""Reusable realistic sample records for local demos and tests."""

SAMPLE_PIPELINE_RUNS = [
    {
        "pipeline_name": "customer_daily_load",
        "pipeline_type": "batch",
        "status": "success",
        "started_at": "2026-06-29T08:00:00Z",
        "ended_at": "2026-06-29T08:12:00Z",
        "duration_seconds": 720,
        "records_processed": 125000,
        "error_message": None,
    },
    {
        "pipeline_name": "orders_stream_ingest",
        "pipeline_type": "streaming",
        "status": "failed",
        "started_at": "2026-06-29T09:00:00Z",
        "ended_at": "2026-06-29T09:04:00Z",
        "duration_seconds": 240,
        "records_processed": 18400,
        "error_message": "Kafka offset lag exceeded alert threshold",
    },
]

SAMPLE_AIRFLOW_DAG_RUNS = [
    {
        "dag_id": "warehouse_refresh",
        "run_id": "scheduled__2026-06-29T08:00:00Z",
        "status": "success",
        "execution_date": "2026-06-29T08:00:00Z",
        "start_time": "2026-06-29T08:01:00Z",
        "end_time": "2026-06-29T08:28:00Z",
        "duration_seconds": 1620,
        "failed_tasks": 0,
        "sla_miss": False,
    },
    {
        "dag_id": "billing_export",
        "run_id": "scheduled__2026-06-29T09:00:00Z",
        "status": "failed",
        "execution_date": "2026-06-29T09:00:00Z",
        "start_time": "2026-06-29T09:02:00Z",
        "end_time": "2026-06-29T09:45:00Z",
        "duration_seconds": 2580,
        "failed_tasks": 1,
        "sla_miss": True,
    },
]

SAMPLE_SPARK_JOBS = [
    {
        "job_name": "silver_orders_compaction",
        "app_id": "application_20260629_0001",
        "status": "success",
        "start_time": "2026-06-29T10:00:00Z",
        "end_time": "2026-06-29T10:08:00Z",
        "duration_seconds": 480,
        "input_records": 500000,
        "output_records": 499900,
        "executor_count": 6,
        "memory_used_mb": 12288,
        "error_message": None,
    },
    {
        "job_name": "customer_feature_build",
        "app_id": "application_20260629_0002",
        "status": "failed",
        "start_time": "2026-06-29T10:30:00Z",
        "end_time": "2026-06-29T10:36:00Z",
        "duration_seconds": 360,
        "input_records": 82000,
        "output_records": 0,
        "executor_count": 4,
        "memory_used_mb": 8192,
        "error_message": "Executor memory exceeded",
    },
]

SAMPLE_DATA_QUALITY_CHECKS = [
    {
        "dataset_name": "orders",
        "check_name": "order_id_not_null",
        "check_type": "expect_column_values_to_not_be_null",
        "expected_value": "0 nulls",
        "actual_value": "0 nulls",
        "failed_records": 0,
        "total_records": 100000,
    },
    {
        "dataset_name": "customers",
        "check_name": "email_format",
        "check_type": "expect_column_values_to_match_regex",
        "expected_value": "valid email format",
        "actual_value": "132 invalid emails",
        "failed_records": 132,
        "total_records": 50000,
    },
]
