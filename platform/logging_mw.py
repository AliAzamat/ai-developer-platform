import json
import time
import sys
from starlette.middleware.base import BaseHTTPMiddleware


class StructuredLogMiddleware(BaseHTTPMiddleware):
    """Emit one structured JSON log line per request — method, path, status, ms."""

    async def dispatch(self, request, call_next):
        start = time.monotonic()
        response = await call_next(request)
        record = {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round((time.monotonic() - start) * 1000, 1),
        }
        print(json.dumps(record), file=sys.stdout, flush=True)
        return response
