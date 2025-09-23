"""
Auth utilities.

JWT encode/decode helpers and password hashing/verification.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import hashlib
import hmac
import os

import base64
import json


# Lightweight JWT (HS256) implementation to avoid extra dependencies.
# For production, consider using `pyjwt`.


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _json_dumps(obj: Any) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sign(message: bytes, secret: bytes) -> bytes:
    return hmac.new(secret, message, hashlib.sha256).digest()


def generate_jwt_token(user_id: str, expires_delta: timedelta) -> str:
    """Generate a compact JWT string signed with HS256.

    Payload includes `sub` and `exp` (as Unix timestamp seconds).
    Secret is read from `JWT_SECRET` env var, defaulting to a dev secret.
    """

    now = datetime.now(timezone.utc)
    exp = now + expires_delta
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "exp": int(exp.timestamp())}
    secret = os.environ.get("JWT_SECRET", "dev-secret").encode("utf-8")

    part1 = _b64url_encode(_json_dumps(header))
    part2 = _b64url_encode(_json_dumps(payload))
    signing_input = f"{part1}.{part2}".encode("ascii")
    signature = _b64url_encode(_sign(signing_input, secret))
    return f"{part1}.{part2}.{signature}"


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verify HS256-signed JWT and return payload.

    Raises ValueError on invalid signature or expiration.
    """

    if not isinstance(token, str) or token.count(".") != 2:
        raise ValueError("Invalid token format")
    part1, part2, signature = token.split(".")
    secret = os.environ.get("JWT_SECRET", "dev-secret").encode("utf-8")
    signing_input = f"{part1}.{part2}".encode("ascii")
    expected_sig = _b64url_encode(_sign(signing_input, secret))
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid token signature")

    payload_bytes = _b64url_decode(part2)
    payload = json.loads(payload_bytes.decode("utf-8"))
    exp = int(payload.get("exp", 0))
    now = int(datetime.now(timezone.utc).timestamp())
    if now >= exp:
        raise ValueError("Token expired")
    return payload


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256.

    Output format: iterations$salt_hex$hash_hex
    """

    if not isinstance(password, str) or not password:
        raise ValueError("password required")
    iterations = 100_000
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{iterations}${salt.hex()}${dk.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        iterations_str, salt_hex, hash_hex = hashed.split("$")
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def get_current_user(token: Optional[str]) -> Optional[str]:
    """Return user id (sub) from bearer token or None if invalid/missing.

    Dev bypass: if ALLOW_PUBLIC_MUTATIONS=true and no token, return a fixed dev user id.
    """

    if not token:
        # Development bypass to allow frontend without auth to mutate
        if os.environ.get("ALLOW_PUBLIC_MUTATIONS", "false").lower() == "true":
            return "dev-user"
        return None
    try:
        payload = verify_jwt_token(token)
        return str(payload.get("sub"))
    except Exception:
        return None

