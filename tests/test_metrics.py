"""Tests for metrics overview endpoint."""

from fastapi.testclient import TestClient


def test_metrics_overview(client: TestClient) -> None:
    client.post(
        "/api/v1/pipeline-runs",
        json={
            "pipeline_name": "daily_orders",
            "pipeline_type": "batch",
            "status": "success",
            "started_at": "2026-06-29T10:00:00Z",
            "duration_seconds": 60,
            "records_processed": 100,
        },
    )
    client.post(
        "/api/v1/airflow/dag-runs",
        json={
            "dag_id": "orders_dag",
            "run_id": "scheduled__2026-06-29",
            "status": "success",
            "execution_date": "2026-06-29T10:00:00Z",
            "start_time": "2026-06-29T10:00:00Z",
            "duration_seconds": 60,
            "failed_tasks": 0,
            "sla_miss": True,
        },
    )
    client.post(
        "/api/v1/spark/jobs",
        json={
            "job_name": "orders_transform",
            "app_id": "application_20260629_0002",
            "status": "failed",
            "start_time": "2026-06-29T10:00:00Z",
            "duration_seconds": 40,
            "input_records": 100,
            "output_records": 0,
            "executor_count": 2,
            "memory_used_mb": 1024,
            "error_message": "Executor lost",
        },
    )
    client.post(
        "/api/v1/data-quality/checks",
        json={
            "dataset_name": "orders",
            "check_name": "row_count",
            "check_type": "expect_table_row_count_to_equal",
            "expected_value": "100",
            "actual_value": "90",
            "failed_records": 10,
            "total_records": 100,
        },
    )

    response = client.get("/api/v1/metrics/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["total_pipeline_runs"] == 1
    assert body["airflow_sla_misses"] == 1
    assert body["failed_spark_jobs"] == 1
    assert body["failed_data_quality_checks"] == 1
