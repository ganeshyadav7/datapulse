"""Tests for authentication and RBAC-compatible defaults."""

from fastapi.testclient import TestClient


def test_register_login_and_refresh(client: TestClient) -> None:
    register = client.post(
        "/auth/register",
        json={
            "email": "admin@datapulse.local",
            "password": "password123",
            "full_name": "Admin User",
            "role": "Admin",
        },
    )
    assert register.status_code == 201
    assert register.json()["role"] == "Admin"

    login = client.post(
        "/auth/login",
        json={"email": "admin@datapulse.local", "password": "password123"},
    )
    assert login.status_code == 200
    tokens = login.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    refresh = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh.status_code == 200
    assert refresh.json()["access_token"]


def test_duplicate_register_returns_409(client: TestClient) -> None:
    payload = {
        "email": "viewer@datapulse.local",
        "password": "password123",
        "role": "Viewer",
    }
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409
