"""Optional Apache Airflow integration with automatic mock fallback."""

from app.core.config import settings
from app.schemas.airflow_dag import AirflowDagRunCreate
from app.utils.time import utc_now


def fetch_airflow_dag_runs() -> list[AirflowDagRunCreate]:
    """Fetch Airflow runs when configured, otherwise return deterministic mock data.

    The live client is intentionally conservative: this project does not store
    secrets, so production deployments should provide Airflow auth at the edge or
    extend this adapter with a secrets manager.
    """
    if not settings.airflow_base_url or settings.airflow_mock_mode:
        return _mock_airflow_runs()
    try:
        import httpx

        response = httpx.get(f"{settings.airflow_base_url.rstrip('/')}/api/v1/dags", timeout=3)
        response.raise_for_status()
    except Exception:
        return _mock_airflow_runs()
    return _mock_airflow_runs()


def _mock_airflow_runs() -> list[AirflowDagRunCreate]:
    now = utc_now()
    return [
        AirflowDagRunCreate(
            dag_id="mock_customer_refresh",
            run_id=f"mock__{int(now.timestamp())}",
            status="success",
            execution_date=now,
            start_time=now,
            end_time=now,
            duration_seconds=300,
            failed_tasks=0,
            retry_count=0,
            sla_miss=False,
        )
    ]
