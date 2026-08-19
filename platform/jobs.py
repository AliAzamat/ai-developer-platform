import uuid
from dataclasses import dataclass
from collections import deque


@dataclass
class Job:
    """A unit of async work and its lifecycle state."""
    job_id: str
    owner: str
    payload: dict
    status: str = "queued"
    result: str | None = None


_JOBS: dict[str, Job] = {}
_QUEUE: deque[str] = deque()
# (owner, idempotency_key) -> job_id, so a retried submit returns the first job.
_IDEMPOTENCY: dict[tuple[str, str], str] = {}


def submit(owner: str, payload: dict, idempotency_key: str | None = None) -> Job:
    """Create a queued job, deduplicating on (owner, idempotency_key)."""
    if idempotency_key is not None:
        existing_id = _IDEMPOTENCY.get((owner, idempotency_key))
        if existing_id is not None:
            return _JOBS[existing_id]        # the retry returns the ORIGINAL job
    job = Job(job_id=str(uuid.uuid4()), owner=owner, payload=payload)
    _JOBS[job.job_id] = job
    _QUEUE.append(job.job_id)
    if idempotency_key is not None:
        _IDEMPOTENCY[(owner, idempotency_key)] = job.job_id
    return job


def get(job_id: str) -> Job | None:
    return _JOBS.get(job_id)


def next_job() -> Job | None:
    if not _QUEUE:
        return None
    return _JOBS[_QUEUE.popleft()]
