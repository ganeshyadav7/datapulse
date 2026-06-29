"""Tests for data quality endpoints."""

from fastapi.testclient import TestClient


def dq_payload() -> dict[str, object]:
    return {
        "dataset_name": "orders",
        "check_name": "order_id_not_null",
        "check_type": "expect_column_values_to_not_be_null",
        "expected_value": "0 nulls",
        "actual_value": "12 nulls",
        "failed_records": 12,
        "total_records": 1000,
    }


def test_data_quality_checks_and_summary(client: TestClient) -> None:
    created = client.post("/api/v1/data-quality/checks", json=dq_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "failed"

    assert client.get("/api/v1/data-quality/checks").status_code == 200

    fetched = client.get(f"/api/v1/data-quality/checks/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["dataset_name"] == "orders"

    summary = client.get("/api/v1/data-quality/summary")
    assert summary.status_code == 200
    assert summary.json()["failed_checks"] == 1
    assert summary.json()["failure_rate"] == 0.012
