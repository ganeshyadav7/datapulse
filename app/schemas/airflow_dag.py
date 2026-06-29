"""Airflow DAG run API schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AirflowDagRunBase(BaseModel):
    dag_id: str = Field(min_length=1, max_length=200)
    run_id: str = Field(min_length=1, max_length=200)
    status: str = Field(min_length=1, max_length=40)
    execution_date: datetime
    start_time: datetime
    end_time: datetime | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    failed_tasks: int = Field(default=0, ge=0)
    retry_count: int = Field(default=0, ge=0)
    sla_miss: bool = False


class AirflowDagRunCreate(AirflowDagRunBase):
    """Request body for creating an Airflow DAG run."""


class AirflowDagRunRead(AirflowDagRunBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class AirflowSummary(BaseModel):
    total_dag_runs: int
    successful_dag_runs: int
    failed_dag_runs: int
    running_dag_runs: int
    sla_misses: int
    total_failed_tasks: int
    total_retries: int
    average_duration_seconds: float
