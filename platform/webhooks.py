import hashlib
import hmac
import json
import urllib.request


def sign(payload: bytes, secret: str) -> str:
    """HMAC-SHA256 signature of the raw payload bytes, hex-encoded."""
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def deliver(url: str, body: dict, secret: str) -> int:
    """POST a signed JSON webhook. Returns the HTTP status code."""
    raw = json.dumps(body, separators=(",", ":")).encode()
    signature = sign(raw, secret)
    req = urllib.request.Request(
        url, data=raw, method="POST",
        headers={"Content-Type": "application/json",
                 "X-Signature": f"sha256={signature}"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status


def verify(payload: bytes, secret: str, signature: str) -> bool:
    """A receiver uses this to confirm the webhook really came from us."""
    expected = "sha256=" + sign(payload, secret)
    return hmac.compare_digest(expected, signature)
