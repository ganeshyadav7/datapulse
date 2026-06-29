"""Centralized logging configuration."""

import json
import logging

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    """Format logs as JSON for production log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in (
            "request_id",
            "correlation_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
        ):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging() -> None:
    """Configure application logging with a compact local-friendly format."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(settings.log_level.upper())
