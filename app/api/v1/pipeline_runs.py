"""Pipeline run endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.core.security import require_roles
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.pipeline_run import PipelineRunCreate, PipelineRunRead, PipelineRunSummary
from app.services import pipeline_service

router = APIRouter(prefix="/api/v1/pipeline-runs", tags=["pipeline-runs"])


@router.post("", response_model=PipelineRunRead, status_code=status.HTTP_201_CREATED)
def create_pipeline_run(
    payload: PipelineRunCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR)),
):
    return pipeline_service.create_run(db, payload)


@router.get("", response_model=list[PipelineRunRead])
def list_pipeline_runs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return pipeline_service.list_runs(db, skip=skip, limit=limit)


@router.get("/summary", response_model=PipelineRunSummary)
def get_pipeline_run_summary(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return pipeline_service.summarize_runs(db)


@router.get("/{run_id}", response_model=PipelineRunRead)
def get_pipeline_run(
    run_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    run = pipeline_service.get_run(db, run_id)
    if run is None:
        raise not_found("PipelineRun", run_id)
    return run
