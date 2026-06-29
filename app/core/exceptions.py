"""Shared API exception helpers."""

from fastapi import HTTPException, status


def not_found(resource: str, item_id: int) -> HTTPException:
    """Build a consistent 404 response for missing database records."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id {item_id} was not found",
    )
