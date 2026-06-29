"""Tests for pipeline run endpoints."""

from fastapi.testclient import TestClient


def pipeline_payload(status: str = "success") -> dict[str, object]:
    return {
        "pipeline_name": "customer_daily_load",
        "pipeline_type": "batch",
        "status": status,
        "started_at": "2026-06-29T10:00:00Z",
        "ended_at": "2026-06-29T10:12:00Z",
        "duration_seconds": 720,
        "records_processed": 125000,
        "error_message": None,
    }


def test_pipeline_run_crud_and_summary(client: TestClient) -> None:
    created = client.post("/api/v1/pipeline-runs", json=pipeline_payload())
    assert created.status_code == 201
    run_id = created.json()["id"]

    listed = client.get("/api/v1/pipeline-runs")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/api/v1/pipeline-runs/{run_id}")
    assert fetched.status_code == 200
    assert fetched.json()["pipeline_name"] == "customer_daily_load"

    summary = client.get("/api/v1/pipeline-runs/summary")
    assert summary.status_code == 200
    assert summary.json()["total_runs"] == 1
    assert summary.json()["successful_runs"] == 1
    assert summary.json()["total_records_processed"] == 125000


def test_missing_pipeline_run_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/pipeline-runs/999")
    assert response.status_code == 404
