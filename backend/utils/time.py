"""
Time utilities.

Helpers for parsing ISO timestamps, converting to/from UTC, generating
time slots, and getting timezone offsets.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List
import hashlib

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


def parse_iso_datetime(dt_str: str) -> datetime:
    """Parse ISO-8601 string into timezone-aware datetime.

    Accepts trailing 'Z' for UTC.
    """

    if not isinstance(dt_str, str) or not dt_str:
        raise ValueError("datetime string required")
    value = dt_str
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def convert_to_utc(local_dt: datetime, timezone_name: str) -> datetime:
    """Convert a local datetime given a timezone name to UTC."""

    if ZoneInfo is None:
        raise ValueError("ZoneInfo is unavailable in this environment")
    if local_dt.tzinfo is None:
        local_dt = local_dt.replace(tzinfo=ZoneInfo(timezone_name))  # type: ignore[arg-type]
    else:
        local_dt = local_dt.astimezone(ZoneInfo(timezone_name))  # type: ignore[arg-type]
    return local_dt.astimezone(timezone.utc)


def convert_from_utc(utc_dt: datetime, timezone_name: str) -> datetime:
    """Convert a UTC datetime to local time in `timezone_name`."""

    if ZoneInfo is None:
        raise ValueError("ZoneInfo is unavailable in this environment")
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    else:
        utc_dt = utc_dt.astimezone(timezone.utc)
    return utc_dt.astimezone(ZoneInfo(timezone_name))  # type: ignore[arg-type]


def generate_time_slots(start: datetime, end: datetime, duration_minutes: int) -> List[datetime]:
    """Generate slot start times from `start` to before `end` every duration minutes.

    Both `start` and `end` should be timezone-aware datetimes.
    """

    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    if end <= start:
        return []
    if duration_minutes <= 0:
        raise ValueError("duration_minutes must be > 0")
    step = timedelta(minutes=duration_minutes)
    slots: List[datetime] = []
    cursor = start
    while cursor < end:
        slots.append(cursor)
        cursor = cursor + step
    return slots


def get_timezone_offset(timezone_name: str) -> timedelta:
    """Return offset for timezone now relative to UTC as timedelta."""

    if ZoneInfo is None:
        raise ValueError("ZoneInfo is unavailable in this environment")
    now_utc = datetime.now(timezone.utc)
    local_now = now_utc.astimezone(ZoneInfo(timezone_name))  # type: ignore[arg-type]
    return local_now.utcoffset() or timedelta(0)


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def generate_default_avatar(name: str) -> str:
    """Generate a default avatar URL based on user name.
    
    Uses a placeholder service that generates avatars based on initials.
    """
    # Clean the name and get initials
    initials = ''.join([word[0].upper() for word in name.split() if word])[:2]
    if not initials:
        initials = 'U'
    
    # Use a simple hash of the name for consistent colors
    name_hash = hashlib.md5(name.encode()).hexdigest()
    color = name_hash[:6]  # Use first 6 characters as hex color
    
    # Use a placeholder service (like UI Avatars or DiceBear)
    # For now, we'll use a simple placeholder that shows initials
    return f"https://ui-avatars.com/api/?name={initials}&background={color}&color=fff&size=128&bold=true"


def get_default_availability() -> dict:
    """Get default availability structure for new users.
    
    Returns a structure with all time slots set to False (unavailable).
    """
    availability = {}
    
    # Generate slots for 7 days (Monday to Sunday) and 24 hours each day
    for day in range(7):  # 0 = Monday, 6 = Sunday
        for hour in range(24):  # 0-23 hours
            slot_key = f"day_{day}_slot_{hour}"
            availability[slot_key] = False
    
    return availability

