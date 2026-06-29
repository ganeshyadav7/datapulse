"""Airflow monitoring simulation endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.db.session import get_db
from app.schemas.airflow_dag import AirflowDagRunCreate, AirflowDagRunRead, AirflowSummary
from app.services import airflow_service

router = APIRouter(prefix="/api/v1/airflow", tags=["airflow"])


@router.post("/dag-runs", response_model=AirflowDagRunRead, status_code=status.HTTP_201_CREATED)
def create_dag_run(payload: AirflowDagRunCreate, db: Session = Depends(get_db)):
    try:
        return airflow_service.create_airflow_dag_run(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Airflow run_id already exists",
        ) from exc


@router.get("/dag-runs", response_model=list[AirflowDagRunRead])
def list_dag_runs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return airflow_service.list_airflow_dag_runs(db, skip=skip, limit=limit)


@router.get("/summary", response_model=AirflowSummary)
def get_airflow_summary(db: Session = Depends(get_db)):
    return airflow_service.summarize_airflow(db)


@router.get("/dag-runs/{dag_run_id}", response_model=AirflowDagRunRead)
def get_dag_run(dag_run_id: int, db: Session = Depends(get_db)):
    dag_run = airflow_service.get_airflow_dag_run(db, dag_run_id)
    if dag_run is None:
        raise not_found("AirflowDagRun", dag_run_id)
    return dag_run
