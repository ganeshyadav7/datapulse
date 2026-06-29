"""Pipeline run service logic."""

from sqlalchemy.orm import Session

from app.crud.pipeline_run import create_pipeline_run, get_pipeline_run, list_pipeline_runs
from app.models.pipeline_run import PipelineRun
from app.schemas.pipeline_run import PipelineRunCreate, PipelineRunSummary


def create_run(db: Session, payload: PipelineRunCreate) -> PipelineRun:
    return create_pipeline_run(db, payload)


def list_runs(db: Session, skip: int = 0, limit: int = 100) -> list[PipelineRun]:
    return list_pipeline_runs(db, skip=skip, limit=limit)


def get_run(db: Session, run_id: int) -> PipelineRun | None:
    return get_pipeline_run(db, run_id)


def summarize_runs(db: Session) -> PipelineRunSummary:
    runs = list_pipeline_runs(db, limit=10_000)
    durations = [run.duration_seconds for run in runs if run.duration_seconds is not None]
    return PipelineRunSummary(
        total_runs=len(runs),
        successful_runs=sum(run.status.lower() == "success" for run in runs),
        failed_runs=sum(run.status.lower() == "failed" for run in runs),
        running_runs=sum(run.status.lower() == "running" for run in runs),
        average_duration_seconds=round(sum(durations) / len(durations), 2) if durations else 0.0,
        total_records_processed=sum(run.records_processed for run in runs),
    )
