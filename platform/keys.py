import hashlib
import secrets


def generate_key() -> tuple[str, str]:
    """Create a new API key. Returns (raw_key, key_hash).

    The raw key is shown to the developer ONCE; we persist only the hash.
    """
    raw = "sk_live_" + secrets.token_urlsafe(24)
    return raw, hash_key(raw)


def hash_key(raw: str) -> str:
    """A one-way hash of an API key, for storage and lookup."""
    return hashlib.sha256(raw.encode()).hexdigest()


# key_hash -> owner id. Production: a database table.
_KEYS: dict[str, str] = {}


def register_key(owner: str) -> str:
    """Issue a key to an owner; store the hash, return the raw key once."""
    raw, h = generate_key()
    _KEYS[h] = owner
    return raw


def owner_for(raw: str) -> str | None:
    """Resolve a raw key to its owner, or None if unknown."""
    return _KEYS.get(hash_key(raw))
