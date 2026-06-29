# DataPulse Architecture

DataPulse is organized as an enterprise-style observability control plane.

## Layers

- `app/api/v1`: FastAPI routers, auth, health checks, and metrics.
- `app/core`: settings, structured logging, JWT helpers, middleware, and metrics.
- `app/schemas`: Pydantic v2 request and response models.
- `app/services`: business logic, summaries, and validation decisions.
- `app/crud`: database persistence helpers.
- `app/models`: SQLAlchemy ORM table mappings.
- `app/db`: engine, session, and declarative base setup.
- `app/utils`: time and sample data helpers.
- `frontend`: React/Vite dashboard.
- `grafana` and `prometheus`: observability stack provisioning.

## Request Flow

1. A client calls a FastAPI endpoint.
2. The router validates input with Pydantic schemas.
3. FastAPI injects a SQLAlchemy session.
4. The router delegates to a service.
5. The service uses CRUD helpers and ORM models.
6. The response is serialized through a Pydantic response model.

## Database

SQLite is the default for local development:

```text
sqlite:///./datapulse.db
```

PostgreSQL can be enabled by setting `DATABASE_URL`:

```text
postgresql+psycopg2://datapulse:datapulse@localhost:5432/datapulse
```

## Observability Domains

DataPulse monitors four common data engineering surfaces:

- Pipeline run lifecycle and throughput.
- Airflow DAG run health, failed tasks, and SLA misses.
- Spark job status, records, executors, and memory use.
- Data quality checks with Great Expectations-style pass/fail semantics.

## Security and Observability

- JWT auth endpoints support Admin, Operator, and Viewer roles.
- Existing APIs remain backward compatible when `AUTH_ENABLED=false`.
- Request IDs and correlation IDs are emitted as response headers.
- Logs are JSON-formatted for aggregation.
- Security headers and CORS are configured centrally.
- Prometheus-style metrics are exposed for Grafana dashboards.
