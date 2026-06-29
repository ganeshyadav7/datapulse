"""Tests for Great Expectations-compatible validation helpers."""

from app.services.great_expectations_service import validate_records, write_validation_report


def test_validate_records_detects_quality_failures() -> None:
    report = validate_records(
        records=[
            {"id": 1, "name": "Ada", "tier": "gold"},
            {"id": 1, "name": "Ada", "tier": "gold"},
            {"id": 2, "name": None, "unexpected": "value"},
            {"id": "bad-type", "name": "Grace"},
        ],
        schema={"id": int, "name": str},
    )

    assert report["status"] == "failed"
    assert report["failed_records"] > 0
    assert report["duplicate_rows"] == 1
    assert report["null_failures"] == 1
    assert report["type_failures"] == 1
    assert report["unexpected_columns"] == ["tier", "unexpected"]


def test_write_validation_report(tmp_path) -> None:
    path = write_validation_report(
        {"status": "success", "total_records": 10},
        tmp_path / "validation.md",
    )

    assert path.exists()
    assert "DataPulse Validation Report" in path.read_text(encoding="utf-8")
