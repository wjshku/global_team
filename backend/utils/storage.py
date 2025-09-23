"""
Storage utilities.

File I/O helpers for JSON persistence with atomic writes and file locks.
"""

import json
import os
import tempfile
from contextlib import contextmanager
from typing import Any, Callable


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def _ensure_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _default_serializer(obj: Any) -> Any:
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def data_path(filename: str) -> str:
    """Return absolute path within backend/data for a given filename."""
    if os.path.isabs(filename):
        return filename
    _ensure_dir(os.path.join(DATA_DIR, 'x'))  # ensure data dir exists
    return os.path.join(DATA_DIR, filename)


def read_json(filename: str, default_factory: Callable[[], Any] | None = None) -> Any:
    """Read JSON from file. If not exists/empty, return default_factory() or {}."""
    path = data_path(filename)
    if not os.path.exists(path):
        return default_factory() if default_factory else {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return default_factory() if default_factory else {}
            return json.loads(content)
    except FileNotFoundError:
        return default_factory() if default_factory else {}


def write_json(filename: str, data: Any) -> None:
    """Atomically write JSON to file."""
    path = data_path(filename)
    _ensure_dir(path)
    dir_name = os.path.dirname(path)
    fd, tmp_path = tempfile.mkstemp(prefix='.tmp-', dir=dir_name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as tmp_file:
            json.dump(data, tmp_file, ensure_ascii=False, separators=(',', ':'), default=_default_serializer)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(tmp_path, path)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass


@contextmanager
def update_json(filename: str, default_factory: Callable[[], Any] | None = None):
    """Context manager to read-modify-write JSON safely.

    Usage:
        with update_json('members.json', list) as data:
            data.append({...})
    """
    data = read_json(filename, default_factory)
    yield data
    write_json(filename, data)
