"""CRUD helpers for pipeline runs."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pipeline_run import PipelineRun
from app.schemas.pipeline_run import PipelineRunCreate


def create_pipeline_run(db: Session, payload: PipelineRunCreate) -> PipelineRun:
    run = PipelineRun(**payload.model_dump())
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def list_pipeline_runs(db: Session, skip: int = 0, limit: int = 100) -> list[PipelineRun]:
    statement = (
        select(PipelineRun).order_by(PipelineRun.created_at.desc()).offset(skip).limit(limit)
    )
    return list(db.scalars(statement).all())


def get_pipeline_run(db: Session, run_id: int) -> PipelineRun | None:
    return db.get(PipelineRun, run_id)
