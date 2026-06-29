"""Pipeline run API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PipelineRunBase(BaseModel):
    pipeline_name: str = Field(min_length=1, max_length=200)
    pipeline_type: str = Field(min_length=1, max_length=80)
    status: str = Field(min_length=1, max_length=40)
    started_at: datetime
    ended_at: datetime | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    records_processed: int = Field(default=0, ge=0)
    error_message: str | None = None


class PipelineRunCreate(PipelineRunBase):
    """Request body for creating a pipeline run."""


class PipelineRunRead(PipelineRunBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class PipelineRunSummary(BaseModel):
    total_runs: int
    successful_runs: int
    failed_runs: int
    running_runs: int
    average_duration_seconds: float
    total_records_processed: int
