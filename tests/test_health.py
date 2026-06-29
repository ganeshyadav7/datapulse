"""Tests for health endpoints."""

from fastapi.testclient import TestClient


def test_root_health_endpoint(client: TestClient) -> None:
    """Root endpoint should report healthy status."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_health_endpoint(client: TestClient) -> None:
    """Versioned health endpoint should report healthy status."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
