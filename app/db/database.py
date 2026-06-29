"""Database engine setup."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings


def make_engine(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine for SQLite or PostgreSQL-compatible URLs."""
    url = database_url or settings.database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine_kwargs = {"connect_args": connect_args}
    if url == "sqlite://":
        engine_kwargs["poolclass"] = StaticPool
    return create_engine(url, **engine_kwargs)


engine = make_engine()
