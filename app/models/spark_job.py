"""Spark job ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.time import utc_now


class SparkJob(Base):
    """A simulated Spark application/job record."""

    __tablename__ = "spark_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_name: Mapped[str] = mapped_column(String(200), index=True)
    app_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(nullable=True)
    input_records: Mapped[int] = mapped_column(Integer, default=0)
    output_records: Mapped[int] = mapped_column(Integer, default=0)
    executor_count: Mapped[int] = mapped_column(Integer, default=1)
    memory_used_mb: Mapped[int] = mapped_column(Integer, default=0)
    partitions: Mapped[int] = mapped_column(Integer, default=1)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
