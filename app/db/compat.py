"""Local SQLite compatibility helpers for existing development databases."""

from sqlalchemy import text
from sqlalchemy.engine import Engine

AIRFLOW_RETRY_COLUMN_SQL = (
    "ALTER TABLE airflow_dag_runs " "ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0"
)
SPARK_PARTITIONS_COLUMN_SQL = (
    "ALTER TABLE spark_jobs ADD COLUMN partitions INTEGER NOT NULL DEFAULT 1"
)


def ensure_sqlite_compatibility(engine: Engine) -> None:
    """Add newly introduced nullable/defaulted columns to old SQLite dev DBs."""
    if engine.url.get_backend_name() != "sqlite":
        return
    with engine.begin() as connection:
        tables = {
            row[0]
            for row in connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).all()
        }
        if "airflow_dag_runs" in tables:
            columns = {
                row[1] for row in connection.execute(text("PRAGMA table_info(airflow_dag_runs)"))
            }
            if "retry_count" not in columns:
                connection.execute(text(AIRFLOW_RETRY_COLUMN_SQL))
        if "spark_jobs" in tables:
            columns = {row[1] for row in connection.execute(text("PRAGMA table_info(spark_jobs)"))}
            if "partitions" not in columns:
                connection.execute(text(SPARK_PARTITIONS_COLUMN_SQL))
