"""Centralized logging configuration."""

import logging

from app.core.config import settings


def configure_logging() -> None:
    """Configure application logging with a compact local-friendly format."""
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
