"""HTTP middleware for production observability and security."""

import logging
import time
import uuid
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.metrics import api_metrics

logger = logging.getLogger("datapulse.request")
RequestHandler = Callable[[Request], Awaitable[Response]]


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request IDs, structured request logs, and security headers."""

    async def dispatch(self, request: Request, call_next: RequestHandler) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        correlation_id = request.headers.get("x-correlation-id", request_id)
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        api_metrics.request_count += 1
        api_metrics.total_duration_ms += duration_ms
        if response.status_code >= 500:
            api_metrics.error_count += 1

        response.headers["x-request-id"] = request_id
        response.headers["x-correlation-id"] = correlation_id
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["x-frame-options"] = "DENY"
        response.headers["referrer-policy"] = "no-referrer"
        response.headers["permissions-policy"] = "camera=(), microphone=(), geolocation=()"

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    """Small process-local rate limiter for local and single-node deployments."""

    def __init__(self, app):
        super().__init__(app)
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: RequestHandler) -> Response:
        client = request.client.host if request.client else "unknown"
        now = time.time()
        bucket = self._requests[client]
        while bucket and now - bucket[0] > settings.rate_limit_window_seconds:
            bucket.popleft()
        if len(bucket) >= settings.rate_limit_requests:
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json",
            )
        bucket.append(now)
        return await call_next(request)
