# DataPulse

DataPulse is a lightweight, open-source observability tool for data pipelines.
This repository currently contains the initial FastAPI project foundation.

## Features

- FastAPI application metadata for `DataPulse` version `0.1.0`
- Root health endpoint at `GET /`
- Versioned health endpoint at `GET /api/v1/health`
- Basic pytest coverage for health checks

## Project Structure

```text
app/
  api/       API route modules
  core/      Configuration and shared utilities
  models/    Pydantic models
  services/  Business logic services
docs/        Project documentation
scripts/     Development and maintenance scripts
tests/       Test suite
```

## Getting Started

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

## Configuration

Copy `.env.example` to `.env` for local configuration overrides.

