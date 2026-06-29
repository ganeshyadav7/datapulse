"""Airflow monitoring simulation service logic."""

from sqlalchemy.orm import Session

from app.crud.airflow_dag import create_dag_run, get_dag_run, list_dag_runs
from app.models.airflow_dag import AirflowDagRun
from app.schemas.airflow_dag import AirflowDagRunCreate, AirflowSummary


def create_airflow_dag_run(db: Session, payload: AirflowDagRunCreate) -> AirflowDagRun:
    return create_dag_run(db, payload)


def list_airflow_dag_runs(db: Session, skip: int = 0, limit: int = 100) -> list[AirflowDagRun]:
    return list_dag_runs(db, skip=skip, limit=limit)


def get_airflow_dag_run(db: Session, dag_run_id: int) -> AirflowDagRun | None:
    return get_dag_run(db, dag_run_id)


def summarize_airflow(db: Session) -> AirflowSummary:
    dag_runs = list_dag_runs(db, limit=10_000)
    durations = [run.duration_seconds for run in dag_runs if run.duration_seconds is not None]
    return AirflowSummary(
        total_dag_runs=len(dag_runs),
        successful_dag_runs=sum(run.status.lower() == "success" for run in dag_runs),
        failed_dag_runs=sum(run.status.lower() == "failed" for run in dag_runs),
        running_dag_runs=sum(run.status.lower() == "running" for run in dag_runs),
        sla_misses=sum(run.sla_miss for run in dag_runs),
        total_failed_tasks=sum(run.failed_tasks for run in dag_runs),
        total_retries=sum(run.retry_count for run in dag_runs),
        average_duration_seconds=round(sum(durations) / len(durations), 2) if durations else 0.0,
    )
