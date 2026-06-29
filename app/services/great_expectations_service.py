"""Great Expectations-compatible data quality validation and report generation."""

from collections import Counter
from pathlib import Path
from typing import Any


def validate_records(records: list[dict[str, Any]], schema: dict[str, type]) -> dict[str, Any]:
    """Validate records for nulls, duplicates, schema drift, types, and unexpected fields."""
    try:
        import great_expectations as ge  # noqa: F401

        engine = "great_expectations_available"
    except Exception:
        engine = "native_fallback"
    total_records = len(records)
    null_failures = sum(
        1 for record in records for field in schema if record.get(field) in (None, "")
    )
    fingerprints = [tuple(sorted(record.items())) for record in records]
    duplicate_rows = sum(count - 1 for count in Counter(fingerprints).values() if count > 1)
    unexpected_columns = sorted({key for record in records for key in record} - set(schema))
    type_failures = 0
    for record in records:
        for field, expected_type in schema.items():
            value = record.get(field)
            if value is not None and not isinstance(value, expected_type):
                type_failures += 1
    failed_records = null_failures + duplicate_rows + type_failures + len(unexpected_columns)
    return {
        "engine": engine,
        "status": "success" if failed_records == 0 else "failed",
        "total_records": total_records,
        "failed_records": failed_records,
        "null_failures": null_failures,
        "duplicate_rows": duplicate_rows,
        "unexpected_columns": unexpected_columns,
        "type_failures": type_failures,
    }


def write_validation_report(report: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# DataPulse Validation Report", ""]
    for key, value in report.items():
        lines.append(f"- **{key}**: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
