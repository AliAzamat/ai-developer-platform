from collections import defaultdict


class UsageMeter:
    """Per-key usage counters for billing and quotas. Production: Redis/DB."""

    def __init__(self) -> None:
        self.requests: dict[str, int] = defaultdict(int)
        self.tokens: dict[str, int] = defaultdict(int)

    def record(self, owner: str, tokens: int = 0) -> None:
        """Count one request and any tokens it consumed, against an owner."""
        self.requests[owner] += 1
        self.tokens[owner] += tokens

    def usage(self, owner: str) -> dict:
        """The current billing-relevant usage for one owner."""
        return {"requests": self.requests[owner], "tokens": self.tokens[owner]}
