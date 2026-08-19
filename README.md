# Developer API Platform for AI Workflows

An advanced project that builds the platform layer around AI workflows — the part between a model call and a paying developer. You build a FastAPI service that authenticates callers with hashed API keys, enforces per-key token-bucket rate limits, and exposes long-running AI jobs asynchronously through a queue with a background worker. You add webhook delivery with HMAC signatures so callers are notified when a job finishes, structured request logging and per-key usage metering for billing and observability, and idempotency keys so a retried request never runs a job twice. Everything runs locally under docker-compose with the API, a worker, and Redis. By the end you own the reusable platform scaffolding that turns any AI workflow into a metered, rate-limited, observable product.

## Stack
- Python
- FastAPI
- Redis
- Pydantic
- Docker
- docker-compose
