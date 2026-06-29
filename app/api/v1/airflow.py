"""Airflow monitoring simulation endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.core.security import require_roles
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.airflow_dag import AirflowDagRunCreate, AirflowDagRunRead, AirflowSummary
from app.services import airflow_service
from app.services.airflow_integration import fetch_airflow_dag_runs

router = APIRouter(prefix="/api/v1/airflow", tags=["airflow"])


@router.post("/dag-runs", response_model=AirflowDagRunRead, status_code=status.HTTP_201_CREATED)
def create_dag_run(
    payload: AirflowDagRunCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
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
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return airflow_service.list_airflow_dag_runs(db, skip=skip, limit=limit)


@router.get("/summary", response_model=AirflowSummary)
def get_airflow_summary(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return airflow_service.summarize_airflow(db)


@router.post("/sync", response_model=list[AirflowDagRunRead])
def sync_airflow_runs(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
    synced = []
    for payload in fetch_airflow_dag_runs():
        try:
            synced.append(airflow_service.create_airflow_dag_run(db, payload))
        except IntegrityError:
            db.rollback()
    return synced


@router.get("/dag-runs/{dag_run_id}", response_model=AirflowDagRunRead)
def get_dag_run(
    dag_run_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    dag_run = airflow_service.get_airflow_dag_run(db, dag_run_id)
    if dag_run is None:
        raise not_found("AirflowDagRun", dag_run_id)
    return dag_run
