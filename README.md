# DataPulse

DataPulse is an open-source data observability platform for monitoring pipeline
runs, Airflow DAGs, Spark jobs, data quality checks, SLA breaches, failures, and
operational metrics.

It now includes a FastAPI backend, JWT authentication, role-based access control,
a React/Vite dashboard, optional Airflow/PySpark/Great Expectations-style
integrations, SQLite/PostgreSQL support, Alembic migrations, structured logging,
Prometheus metrics, Grafana dashboards, Docker Compose, and CI quality gates.

## Architecture

```text
React/Vite Dashboard
  -> FastAPI API
      -> routers: app/api/v1
      -> auth/RBAC: app/core/security.py
      -> services: app/services
      -> CRUD: app/crud
      -> ORM models: app/models
      -> SQLite or PostgreSQL
  -> Prometheus scrape endpoint
  -> Grafana provisioned dashboard
```

## Folder Structure

```text
app/
  api/v1/          API routes, auth, health, metrics
  core/            settings, logging, security, middleware, metrics
  crud/            persistence helpers
  db/              engine, session, base, SQLite compatibility
  models/          SQLAlchemy ORM models
  schemas/         Pydantic request/response models
  services/        business logic and integration adapters
  utils/           sample data and time utilities
frontend/          React/Vite dashboard
grafana/           provisioned Grafana datasource and dashboard
prometheus/        Prometheus scrape config
alembic/           migration environment and revisions
tests/             API, auth, and observability tests
scripts/           database seed scripts
```

## Tech Stack

- Python 3.11+
- FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic
- SQLite by default, PostgreSQL-ready through `DATABASE_URL`
- JWT-style HMAC tokens and PBKDF2 password hashing
- React, Vite, Recharts, lucide-react
- Pytest, Black, isort, Flake8
- Docker Compose, Prometheus, Grafana

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run the dashboard:

```bash
cd frontend
npm install
npm run dev
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Dashboard: http://127.0.0.1:5173

## Docker

Run API and frontend:

```bash
docker compose up --build datapulse-api datapulse-frontend
```

Run optional PostgreSQL:

```bash
docker compose --profile postgres up postgres
```

Run optional Airflow:

```bash
docker compose --profile airflow up airflow
```

Run optional Prometheus and Grafana:

```bash
docker compose --profile observability up prometheus grafana
```

Grafana runs at http://localhost:3000 with `admin/admin`.

## Authentication

Auth routes:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

Roles:

- `Admin`
- `Operator`
- `Viewer`

By default, `AUTH_ENABLED=false` preserves backward compatibility for local
development and existing clients. Set `AUTH_ENABLED=true` to enforce bearer-token
RBAC on protected APIs.

Example:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@datapulse.local","password":"password123","role":"Admin"}'
```

## API

Existing endpoints remain supported:

- `GET /`
- `GET /api/v1/health`
- `POST /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs/{id}`
- `GET /api/v1/pipeline-runs/summary`
- `POST /api/v1/airflow/dag-runs`
- `GET /api/v1/airflow/dag-runs`
- `GET /api/v1/airflow/dag-runs/{id}`
- `GET /api/v1/airflow/summary`
- `POST /api/v1/spark/jobs`
- `GET /api/v1/spark/jobs`
- `GET /api/v1/spark/jobs/{id}`
- `GET /api/v1/spark/summary`
- `POST /api/v1/data-quality/checks`
- `GET /api/v1/data-quality/checks`
- `GET /api/v1/data-quality/checks/{id}`
- `GET /api/v1/data-quality/summary`
- `GET /api/v1/metrics/overview`

New endpoints:

- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`
- `GET /api/v1/metrics/performance`
- `GET /api/v1/metrics/prometheus`
- `POST /api/v1/airflow/sync`
- `POST /api/v1/spark/sample-job`
- `POST /api/v1/data-quality/validate`

## Airflow

DataPulse includes an Airflow integration adapter and Docker service. If
`AIRFLOW_BASE_URL` is unset or Airflow is unavailable, the service automatically
uses mock mode so local development keeps working.

## Spark

The Spark integration runs a tiny PySpark job when PySpark is installed. If
PySpark is unavailable, it records mock metrics with a clear message.

## Data Quality

The validation service checks null values, duplicate rows, schema drift, column
types, and unexpected fields, then can generate Markdown validation reports.

## Seed Data

Create realistic demo data:

```bash
python scripts/seed_data.py
```

Defaults:

- 500 pipeline runs
- 100 Airflow DAG runs
- 200 Spark jobs
- 300 data quality checks

Counts can be changed:

```bash
python scripts/seed_data.py --pipeline-runs 50 --airflow-runs 20
```

## Testing and CI

Local checks:

```bash
black --check app tests scripts
isort --check-only app tests scripts
flake8 app tests scripts --max-line-length=100 --extend-ignore=E203,W503
python -m pytest
cd frontend && npm run build
```

GitHub Actions runs formatting checks, import-order checks, Flake8, tests, import
verification, and Docker image build.

## Database Schema

Core tables:

- `users`: email, hashed password, role, active flag
- `pipeline_runs`: pipeline status, timing, records, errors
- `airflow_dag_runs`: DAG/run IDs, status, failed tasks, retries, SLA misses
- `spark_jobs`: app/job IDs, records, executors, memory, partitions, errors
- `data_quality_checks`: dataset, check type, expected/actual values, failures

SQLite is the default; PostgreSQL is selected by changing `DATABASE_URL`.

## Interview Explanation

DataPulse demonstrates a production-style data platform service. It combines API
design, database modeling, observability, auth, CI, Docker, dashboard UI, and
data engineering domain concepts such as Airflow orchestration, Spark execution,
SLA monitoring, and data quality validation.

## Roadmap

- Replace in-process rate limiting with Redis for multi-node deployments.
- Add OpenTelemetry traces.
- Add native Airflow auth and DAG run ingestion.
- Add a persistent Spark history-server collector.
- Add row-level tenancy and organization workspaces.
- Add automated frontend tests.
