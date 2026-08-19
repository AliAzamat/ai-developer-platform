from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from platform.keys import owner_for
from platform.ratelimit import RateLimiter
from platform import jobs

app = FastAPI(title="AI Workflow Platform")
limiter = RateLimiter(capacity=10, rate=1.0)


class SummarizeRequest(BaseModel):
    text: str


def require_key(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    owner = owner_for(authorization.removeprefix("Bearer "))
    if owner is None:
        raise HTTPException(401, "invalid API key")
    return owner


@app.post("/v1/jobs/summarize")
def submit_summarize(body: SummarizeRequest, owner: str = require_key) -> dict:
    """Enqueue the workflow and return a job id immediately (202 Accepted)."""
    if not limiter.allow(owner):
        raise HTTPException(429, "rate limit exceeded")
    job = jobs.submit(owner, {"text": body.text})
    return {"job_id": job.job_id, "status": job.status}


@app.get("/v1/jobs/{job_id}")
def job_status(job_id: str, owner: str = require_key) -> dict:
    """Poll a job's status and result; owners see only their own jobs."""
    job = jobs.get(job_id)
    if job is None or job.owner != owner:
        raise HTTPException(404, "job not found")
    return {"job_id": job.job_id, "status": job.status, "result": job.result}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
