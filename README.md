# DataPulse

DataPulse is a professional open-source FastAPI platform for observing modern
data pipelines. It tracks pipeline runs, simulated Airflow DAG runs, simulated
Spark jobs, data quality checks, SLA misses, failures, throughput, and summary
metrics using free and open-source tooling.

The project is designed to be useful as a portfolio project, interview talking
point, and clean foundation for a real internal data observability service.

## Architecture

```text
Client
  -> FastAPI routers in app/api/v1
  -> service layer in app/services
  -> CRUD helpers in app/crud
  -> SQLAlchemy ORM models in app/models
  -> SQLite by default, PostgreSQL-ready through DATABASE_URL
```

DataPulse keeps HTTP routing, business logic, persistence, schemas, and
configuration in separate modules so each part can evolve independently.

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- Alembic
- SQLite by default
- PostgreSQL-ready configuration
- Pytest
- Docker and Docker Compose
- GitHub Actions CI

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run locally:

```bash
uvicorn app.main:app --reload
```

Open:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Seed Demo Data

```bash
python scripts/seed_data.py
```

## Docker

Run the API with SQLite:

```bash
docker compose up --build datapulse-api
```

Run the optional PostgreSQL service:

```bash
docker compose --profile postgres up postgres
```

To point the API at PostgreSQL, set:

```bash
DATABASE_URL=postgresql+psycopg2://datapulse:datapulse@postgres:5432/datapulse
```

## API Endpoints

Health:

- `GET /`
- `GET /api/v1/health`

Pipeline runs:

- `POST /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs/{id}`
- `GET /api/v1/pipeline-runs/summary`

Airflow simulation:

- `POST /api/v1/airflow/dag-runs`
- `GET /api/v1/airflow/dag-runs`
- `GET /api/v1/airflow/dag-runs/{id}`
- `GET /api/v1/airflow/summary`

Spark simulation:

- `POST /api/v1/spark/jobs`
- `GET /api/v1/spark/jobs`
- `GET /api/v1/spark/jobs/{id}`
- `GET /api/v1/spark/summary`

Data quality:

- `POST /api/v1/data-quality/checks`
- `GET /api/v1/data-quality/checks`
- `GET /api/v1/data-quality/checks/{id}`
- `GET /api/v1/data-quality/summary`

Metrics:

- `GET /api/v1/metrics/overview`

## Sample Requests

Create a pipeline run:

```bash
curl -X POST http://localhost:8000/api/v1/pipeline-runs \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_name": "customer_daily_load",
    "pipeline_type": "batch",
    "status": "success",
    "started_at": "2026-06-29T08:00:00Z",
    "ended_at": "2026-06-29T08:12:00Z",
    "duration_seconds": 720,
    "records_processed": 125000
  }'
```

Create a data quality check:

```bash
curl -X POST http://localhost:8000/api/v1/data-quality/checks \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_name": "orders",
    "check_name": "order_id_not_null",
    "check_type": "expect_column_values_to_not_be_null",
    "expected_value": "0 nulls",
    "actual_value": "12 nulls",
    "failed_records": 12,
    "total_records": 1000
  }'
```

Get platform overview metrics:

```bash
curl http://localhost:8000/api/v1/metrics/overview
```

## Testing

```bash
python -m pytest
```

The test suite uses an isolated in-memory SQLite database and covers health,
pipeline run tracking, Airflow simulation, Spark simulation, data quality, and
overview metrics.

## Roadmap

- Add Alembic migration revisions for production schema evolution.
- Add filtering by status, name, and time window.
- Add Prometheus-compatible metrics output.
- Add dashboard frontend.
- Add real Airflow metadata database adapters.
- Add Spark History Server ingestion.
- Add notification integrations for SLA and quality failures.

## Resume and Interview Explanation

DataPulse demonstrates how to build a clean backend service for data engineering
operations. It models real observability concerns: pipeline status, DAG failures,
Spark resource usage, data quality validation, SLA misses, aggregate metrics, API
design, database modeling, testing, Docker, and CI.

In an interview, describe it as:

> I built DataPulse as a FastAPI-based observability API for data pipelines. It
> tracks pipeline runs, Airflow DAG runs, Spark jobs, data quality checks, and
> operational summaries. The architecture separates API routers, Pydantic
> schemas, services, CRUD logic, and SQLAlchemy models, with SQLite for local
> development and PostgreSQL-ready configuration for production.
