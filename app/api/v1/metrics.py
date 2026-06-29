"""Metrics endpoints."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.metrics import api_metrics
from app.core.security import require_roles
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.metrics import MetricsOverview
from app.services.metrics_service import get_metrics_overview

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/overview", response_model=MetricsOverview)
def metrics_overview(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
):
    return get_metrics_overview(db)


@router.get("/performance")
def performance_metrics(
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
) -> dict[str, float | int]:
    return {
        "request_count": api_metrics.request_count,
        "error_count": api_metrics.error_count,
        "average_duration_ms": api_metrics.average_duration_ms,
    }


@router.get("/prometheus")
def prometheus_metrics(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR, UserRole.VIEWER)),
) -> Response:
    overview = get_metrics_overview(db)
    lines = [
        "# HELP datapulse_api_requests_total Total API requests.",
        "# TYPE datapulse_api_requests_total counter",
        f"datapulse_api_requests_total {api_metrics.request_count}",
        "# HELP datapulse_pipeline_runs_total Total pipeline runs.",
        "# TYPE datapulse_pipeline_runs_total gauge",
        f"datapulse_pipeline_runs_total {overview.total_pipeline_runs}",
        "# HELP datapulse_pipeline_failures_total Failed pipeline runs.",
        "# TYPE datapulse_pipeline_failures_total gauge",
        f"datapulse_pipeline_failures_total {overview.failed_runs}",
        "# HELP datapulse_airflow_sla_misses_total Airflow SLA misses.",
        "# TYPE datapulse_airflow_sla_misses_total gauge",
        f"datapulse_airflow_sla_misses_total {overview.airflow_sla_misses}",
        "# HELP datapulse_spark_failures_total Failed Spark jobs.",
        "# TYPE datapulse_spark_failures_total gauge",
        f"datapulse_spark_failures_total {overview.failed_spark_jobs}",
        "# HELP datapulse_quality_failures_total Failed data quality checks.",
        "# TYPE datapulse_quality_failures_total gauge",
        f"datapulse_quality_failures_total {overview.failed_data_quality_checks}",
    ]
    return Response("\n".join(lines) + "\n", media_type="text/plain")
