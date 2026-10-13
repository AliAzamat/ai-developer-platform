# AI Developer Platform

**The platform layer that turns an AI workflow into a developer-facing API: hashed API keys, per-key token-bucket rate limiting, async jobs with idempotency, HMAC-signed webhooks, usage metering, and structured request logs.**

A model call isn't a product until developers can authenticate, get throttled fairly, submit slow work without holding a connection open, retry safely, get notified when it's done, and be billed for what they used. This FastAPI project builds those layers around a deliberately simple workflow — two-sentence summarization — so the workflow can be swapped for any AI task without touching the platform code.

## Building blocks

| Concern | Module | Approach |
|---|---|---|
| API keys | `keys.py` | `sk_live_` + 24 random URL-safe bytes; only the SHA-256 hash is stored, and the raw key is shown once. |
| Rate limiting | `ratelimit.py` | One token bucket per key (default capacity 10, refill 1/s), with an injectable clock for deterministic tests. |
| Async jobs | `jobs.py`, `worker.py` | Submit returns a job ID immediately; a worker loop processes the queue and records `running` → `done`/`error`. |
| Idempotency | `jobs.py` | `(owner, idempotency_key)` maps to the first job, so a retried submit returns the original job instead of running twice. |
| Webhooks | `webhooks.py` | Compact JSON body signed with HMAC-SHA256 in an `X-Signature: sha256=…` header; receivers verify with constant-time comparison. Delivery is best-effort. |
| Metering | `metering.py` | Per-owner request and token counters for billing and quotas. |
| Logging | `logging_mw.py` | Starlette middleware that emits one JSON line per request: method, path, status, duration. |
| Workflow | `workflows.py` | `summarize(text)` via the OpenAI chat API — the swappable unit of work. |

## API (intended)

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/jobs/summarize` | `Authorization: Bearer <key>`, body `{"text": "…"}` → `{job_id, status}`; `429` when the bucket is empty |
| `GET` | `/v1/jobs/{job_id}` | Job status and result; owners can only see their own jobs |
| `GET` | `/health` | Liveness |

## Verifying a webhook

Receivers check the signature with `verify` from `platform/webhooks.py`:

```python
ok = verify(raw_request_body, secret="your-shared-secret",
            signature=request.headers["X-Signature"])
```
