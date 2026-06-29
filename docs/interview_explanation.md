# DataPulse Interview Explanation

## Problem

Modern data teams run many pipelines across schedulers, compute engines, and
quality tools. When something fails, engineers need one place to answer:

- Which pipeline failed?
- Did an Airflow DAG miss its SLA?
- Did a Spark job fail or process fewer records than expected?
- Did a data quality check fail?
- What is the overall operational health of the platform?

## Solution

DataPulse is a FastAPI observability API that stores and summarizes operational
metadata for data pipelines. It accepts records for pipeline runs, Airflow DAG
runs, Spark jobs, and data quality checks, then exposes summary and overview
metrics for monitoring.

## Architecture

The project uses a layered backend design:

- Routers handle HTTP endpoints.
- Pydantic schemas validate input and shape responses.
- Services contain business logic and summary calculations.
- CRUD modules handle database reads and writes.
- SQLAlchemy models define the database tables.
- A central settings module controls environment configuration.

## Why FastAPI

FastAPI is a strong fit because it provides type-driven API development,
automatic OpenAPI documentation, high performance, dependency injection, and a
clean testing story with `TestClient`.

## Why SQLAlchemy

SQLAlchemy 2.x gives DataPulse a production-ready ORM while keeping the project
database-portable. SQLite works locally with zero setup, and PostgreSQL can be
used by changing `DATABASE_URL`.

## How Monitoring Works

DataPulse stores events and results from different data engineering systems:

- Pipeline runs track status, duration, records processed, and errors.
- Airflow DAG runs track DAG status, failed tasks, and SLA misses.
- Spark jobs track application status, records, executors, and memory use.
- Data quality checks compare expected values, actual values, failed records,
  and total records.

The summary endpoints aggregate those records into operational metrics.

## Data Engineering Relevance

This mirrors common data engineering work: monitoring batch and streaming jobs,
debugging orchestration failures, validating datasets, tracking SLAs, and
building reliable internal APIs around metadata. It shows backend engineering,
data platform awareness, database modeling, testing, Docker usage, and CI.
