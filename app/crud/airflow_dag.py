"""CRUD helpers for Airflow DAG runs."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.airflow_dag import AirflowDagRun
from app.schemas.airflow_dag import AirflowDagRunCreate


def create_dag_run(db: Session, payload: AirflowDagRunCreate) -> AirflowDagRun:
    dag_run = AirflowDagRun(**payload.model_dump())
    db.add(dag_run)
    db.commit()
    db.refresh(dag_run)
    return dag_run


def list_dag_runs(db: Session, skip: int = 0, limit: int = 100) -> list[AirflowDagRun]:
    statement = select(AirflowDagRun).order_by(AirflowDagRun.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def get_dag_run(db: Session, dag_run_id: int) -> AirflowDagRun | None:
    return db.get(AirflowDagRun, dag_run_id)
