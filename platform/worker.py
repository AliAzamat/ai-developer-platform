import time
from platform.jobs import next_job
from platform.workflows import summarize
from platform.webhooks import deliver


def process_one() -> bool:
    """Run one job, then fire its webhook if the payload requested one."""
    job = next_job()
    if job is None:
        return False
    job.status = "running"
    try:
        job.result = summarize(job.payload["text"])
        job.status = "done"
    except Exception as exc:
        job.status = "error"
        job.result = f"ERROR: {exc!r}"
    callback = job.payload.get("callback_url")
    if callback:
        body = {"job_id": job.job_id, "status": job.status, "result": job.result}
        try:
            deliver(callback, body, secret=job.payload.get("secret", ""))
        except Exception:
            pass            # webhook delivery is best-effort; the job already ran
    return True


def run_forever(idle_sleep: float = 0.5) -> None:
    while True:
        if not process_one():
            time.sleep(idle_sleep)
