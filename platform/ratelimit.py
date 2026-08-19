import time
from dataclasses import dataclass


@dataclass
class Bucket:
    """A token bucket: `tokens` refill at `rate` per second up to `capacity`."""
    capacity: float
    rate: float
    tokens: float
    updated: float


class RateLimiter:
    """One token bucket per key. Production: store buckets in Redis."""

    def __init__(self, capacity: float = 10, rate: float = 1.0) -> None:
        self.capacity = capacity
        self.rate = rate
        self.buckets: dict[str, Bucket] = {}

    def allow(self, key: str, now: float | None = None) -> bool:
        """Try to spend one token for `key`. True if allowed, False if throttled."""
        now = now if now is not None else time.monotonic()
        b = self.buckets.get(key)
        if b is None:
            b = Bucket(self.capacity, self.rate, self.capacity, now)
            self.buckets[key] = b
        # Refill based on elapsed time, capped at capacity.
        elapsed = now - b.updated
        b.tokens = min(b.capacity, b.tokens + elapsed * b.rate)
        b.updated = now
        if b.tokens >= 1:
            b.tokens -= 1
            return True
        return False
