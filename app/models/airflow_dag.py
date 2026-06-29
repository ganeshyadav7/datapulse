"""Airflow DAG run ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.time import utc_now


class AirflowDagRun(Base):
    """A simulated Airflow DAG run record."""

    __tablename__ = "airflow_dag_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dag_id: Mapped[str] = mapped_column(String(200), index=True)
    run_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    execution_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(nullable=True)
    failed_tasks: Mapped[int] = mapped_column(Integer, default=0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    sla_miss: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
