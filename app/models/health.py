"""Health endpoint response models."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Basic health check response."""

    status: str

