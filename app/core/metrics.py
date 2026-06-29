"""In-process API performance metrics."""

from dataclasses import dataclass


@dataclass
class ApiMetrics:
    request_count: int = 0
    error_count: int = 0
    total_duration_ms: float = 0.0

    @property
    def average_duration_ms(self) -> float:
        if self.request_count == 0:
            return 0.0
        return round(self.total_duration_ms / self.request_count, 2)


api_metrics = ApiMetrics()
