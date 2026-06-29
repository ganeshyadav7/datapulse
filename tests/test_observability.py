"""Tests for observability endpoints."""

from fastapi.testclient import TestClient


def test_liveness_readiness_and_performance(client: TestClient) -> None:
    live = client.get("/api/v1/health/live")
    assert live.status_code == 200
    assert live.json()["status"] == "live"

    ready = client.get("/api/v1/health/ready")
    assert ready.status_code == 200
    assert ready.json()["database"] == "ok"

    performance = client.get("/api/v1/metrics/performance")
    assert performance.status_code == 200
    assert "request_count" in performance.json()


def test_prometheus_metrics(client: TestClient) -> None:
    response = client.get("/api/v1/metrics/prometheus")
    assert response.status_code == 200
    assert "datapulse_api_requests_total" in response.text
