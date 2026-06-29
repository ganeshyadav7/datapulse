"""Spark job API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SparkJobBase(BaseModel):
    job_name: str = Field(min_length=1, max_length=200)
    app_id: str = Field(min_length=1, max_length=200)
    status: str = Field(min_length=1, max_length=40)
    start_time: datetime
    end_time: datetime | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    input_records: int = Field(default=0, ge=0)
    output_records: int = Field(default=0, ge=0)
    executor_count: int = Field(default=1, ge=1)
    memory_used_mb: int = Field(default=0, ge=0)
    error_message: str | None = None


class SparkJobCreate(SparkJobBase):
    """Request body for creating a Spark job."""


class SparkJobRead(SparkJobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class SparkSummary(BaseModel):
    total_jobs: int
    successful_jobs: int
    failed_jobs: int
    running_jobs: int
    total_input_records: int
    total_output_records: int
    average_duration_seconds: float
