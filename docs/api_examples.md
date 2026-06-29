# API Examples

## Health

```bash
curl http://localhost:8000/api/v1/health
```

## Pipeline Run

```bash
curl -X POST http://localhost:8000/api/v1/pipeline-runs \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_name": "daily_orders",
    "pipeline_type": "batch",
    "status": "success",
    "started_at": "2026-06-29T08:00:00Z",
    "ended_at": "2026-06-29T08:09:00Z",
    "duration_seconds": 540,
    "records_processed": 200000
  }'
```

## Airflow DAG Run

```bash
curl -X POST http://localhost:8000/api/v1/airflow/dag-runs \
  -H "Content-Type: application/json" \
  -d '{
    "dag_id": "warehouse_refresh",
    "run_id": "scheduled__2026-06-29T08:00:00Z",
    "status": "success",
    "execution_date": "2026-06-29T08:00:00Z",
    "start_time": "2026-06-29T08:01:00Z",
    "end_time": "2026-06-29T08:28:00Z",
    "duration_seconds": 1620,
    "failed_tasks": 0,
    "sla_miss": false
  }'
```

## Spark Job

```bash
curl -X POST http://localhost:8000/api/v1/spark/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "silver_orders_compaction",
    "app_id": "application_20260629_0001",
    "status": "success",
    "start_time": "2026-06-29T10:00:00Z",
    "end_time": "2026-06-29T10:08:00Z",
    "duration_seconds": 480,
    "input_records": 500000,
    "output_records": 499900,
    "executor_count": 6,
    "memory_used_mb": 12288
  }'
```

## Data Quality Check

```bash
curl -X POST http://localhost:8000/api/v1/data-quality/checks \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_name": "customers",
    "check_name": "email_format",
    "check_type": "expect_column_values_to_match_regex",
    "expected_value": "valid email format",
    "actual_value": "132 invalid emails",
    "failed_records": 132,
    "total_records": 50000
  }'
```

## Metrics

```bash
curl http://localhost:8000/api/v1/metrics/overview
```
