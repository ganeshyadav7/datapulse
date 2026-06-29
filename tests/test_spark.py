"""Tests for Spark simulation endpoints."""

from fastapi.testclient import TestClient


def spark_payload() -> dict[str, object]:
    return {
        "job_name": "silver_orders_compaction",
        "app_id": "application_20260629_0001",
        "status": "success",
        "start_time": "2026-06-29T11:00:00Z",
        "end_time": "2026-06-29T11:08:00Z",
        "duration_seconds": 480,
        "input_records": 500000,
        "output_records": 499900,
        "executor_count": 6,
        "memory_used_mb": 12288,
        "error_message": None,
    }


def test_spark_jobs_and_summary(client: TestClient) -> None:
    created = client.post("/api/v1/spark/jobs", json=spark_payload())
    assert created.status_code == 201
    job_id = created.json()["id"]

    assert client.get("/api/v1/spark/jobs").status_code == 200

    fetched = client.get(f"/api/v1/spark/jobs/{job_id}")
    assert fetched.status_code == 200
    assert fetched.json()["job_name"] == "silver_orders_compaction"

    summary = client.get("/api/v1/spark/summary")
    assert summary.status_code == 200
    assert summary.json()["successful_jobs"] == 1
    assert summary.json()["total_input_records"] == 500000
