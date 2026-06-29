"""Tests for Airflow simulation endpoints."""

from fastapi.testclient import TestClient


def airflow_payload() -> dict[str, object]:
    return {
        "dag_id": "warehouse_refresh",
        "run_id": "manual__2026-06-29T10:00:00Z",
        "status": "failed",
        "execution_date": "2026-06-29T10:00:00Z",
        "start_time": "2026-06-29T10:01:00Z",
        "end_time": "2026-06-29T10:30:00Z",
        "duration_seconds": 1740,
        "failed_tasks": 2,
        "sla_miss": True,
    }


def test_airflow_dag_runs_and_summary(client: TestClient) -> None:
    created = client.post("/api/v1/airflow/dag-runs", json=airflow_payload())
    assert created.status_code == 201
    dag_run_id = created.json()["id"]

    assert client.get("/api/v1/airflow/dag-runs").status_code == 200

    fetched = client.get(f"/api/v1/airflow/dag-runs/{dag_run_id}")
    assert fetched.status_code == 200
    assert fetched.json()["dag_id"] == "warehouse_refresh"

    summary = client.get("/api/v1/airflow/summary")
    assert summary.status_code == 200
    assert summary.json()["failed_dag_runs"] == 1
    assert summary.json()["sla_misses"] == 1
