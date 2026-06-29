"""Data quality check API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DataQualityCheckBase(BaseModel):
    dataset_name: str = Field(min_length=1, max_length=200)
    check_name: str = Field(min_length=1, max_length=200)
    check_type: str = Field(min_length=1, max_length=120)
    status: str | None = Field(default=None, max_length=40)
    expected_value: str = Field(min_length=1, max_length=200)
    actual_value: str = Field(min_length=1, max_length=200)
    failed_records: int = Field(default=0, ge=0)
    total_records: int = Field(default=0, ge=0)


class DataQualityCheckCreate(DataQualityCheckBase):
    """Request body for creating a data quality check."""


class DataQualityCheckRead(DataQualityCheckBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime


class DataQualitySummary(BaseModel):
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    total_failed_records: int
    total_records_checked: int
    failure_rate: float
