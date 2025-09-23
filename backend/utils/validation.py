"""
Validation utilities.

Helpers for validating emails, timezones, availability arrays, password
strength, and light input sanitization.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, Mapping

try:
    from zoneinfo import available_timezones  # Python 3.9+
except Exception:  # pragma: no cover
    available_timezones = lambda: set()  # type: ignore


_EMAIL_REGEX = re.compile(
    r"^(?=.{3,254}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_email(email: str) -> bool:
    """Return True if the string looks like a valid email address.

    This is a pragmatic regex-based check and not a full RFC validation.
    """

    if not isinstance(email, str):
        return False
    return _EMAIL_REGEX.match(email.strip()) is not None


def validate_timezone(timezone_name: str) -> bool:
    """Return True if the timezone name is a valid IANA timezone.

    Uses `zoneinfo.available_timezones()` when available.
    """

    if not isinstance(timezone_name, str) or not timezone_name:
        return False
    try:
        return timezone_name in available_timezones()
    except Exception:
        return False


def validate_availability_array(values: Iterable[int]) -> bool:
    """Return True if `values` is a 24-length iterable of 0/1 integers."""

    try:
        items = list(values)
    except Exception:
        return False
    if len(items) != 24:
        return False
    try:
        normalized = [1 if int(v) else 0 for v in items]
    except Exception:
        return False
    return all(v in (0, 1) for v in normalized)


def validate_password_strength(password: str) -> bool:
    """Basic password strength policy.

    - At least 8 characters
    - Contains uppercase, lowercase, digit
    - Optional: special character improves strength, but not required
    """

    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit


def sanitize_input(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a shallow-sanitized copy of mapping `data`.

    - Trims whitespace around string values
    - Leaves other values unchanged
    """

    sanitized: Dict[str, Any] = {}
    for key, value in dict(data).items():
        if isinstance(value, str):
            sanitized[key] = value.strip()
        else:
            sanitized[key] = value
    return sanitized

