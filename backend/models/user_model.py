"""
User model/data access.

MVP: read/write user records in backend/data/members.json.
Production: ORM model with users table, password hashes, timezone, role.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from utils.storage import read_json, write_json, update_json


MEMBERS_FILE = 'members.json'


def _slugify(value: str) -> str:
    return ''.join(ch.lower() if ch.isalnum() else '-' for ch in (value or '').strip()).strip('-') or 'user'


def _normalize_timezone(tz: str) -> str:
    # Minimal normalization for known legacy values
    mapping = {
        'singapore': 'Asia/Singapore',
    }
    key = (tz or '').strip()
    mapped = mapping.get(key.lower())
    return mapped or key


def _availability_array_to_week_slots(arr: List[int]) -> Dict[str, bool]:
    # Legacy storage uses 24-length vector. Map to Monday (day_0) hourly slots 0..23
    if not isinstance(arr, list):
        return {}
    slots: Dict[str, bool] = {}
    for idx, v in enumerate(arr[:24]):
        if int(v) == 1:
            slots[f'day_0_slot_{idx}'] = True
    return slots


def _week_slots_to_availability_array(slots: Dict[str, Any]) -> Dict[str, bool]:
    # Store the full availability object instead of converting to legacy array
    if not isinstance(slots, dict):
        return {}
    return {k: bool(v) for k, v in slots.items()}


class UserModel:
    """Adapter between storage format and frontend API contract for members/users."""

    @staticmethod
    def _load_storage() -> List[Dict[str, Any]]:
        data = read_json(MEMBERS_FILE, default_factory=list)
        if isinstance(data, dict):  # if someone stored an object accidentally
            # Convert dict of name->record to list
            data = [{"name": k, **(v or {})} for k, v in data.items()]
        return list(data or [])

    @staticmethod
    def _save_storage(records: List[Dict[str, Any]]) -> None:
        write_json(MEMBERS_FILE, records)

    @staticmethod
    def _to_api(record: Dict[str, Any], idx: int) -> Dict[str, Any]:
        name = (record.get('name') or '').strip() or f'User {idx+1}'
        timezone = _normalize_timezone(record.get('timezone') or 'UTC')
        availability = record.get('availability')
        
        # Handle both legacy array format and new dict format
        if isinstance(availability, list):
            api_availability = _availability_array_to_week_slots(availability)
        else:
            api_availability = availability or {}
        
        # Generate deterministic id from name and index fallback
        generated_id = f"{_slugify(name)}-{idx+1}"
        return {
            'id': record.get('id') or generated_id,
            'name': name,
            'email': record.get('email') or None,
            'timezone': timezone,
            'role': record.get('role') or 'member',
            'status': record.get('status') or 'offline',
            'availability': api_availability,
            'teams': record.get('teams') or [],
            'avatar': record.get('avatar') or None,
            'createdAt': record.get('createdAt') or None,
        }

    @staticmethod
    def _from_api(payload: Dict[str, Any]) -> Dict[str, Any]:
        availability_slots = payload.get('availability') or {}
        # Store availability as-is instead of converting to legacy array
        return {
            'id': payload.get('id') or _slugify(payload.get('name') or 'user'),
            'name': payload.get('name'),
            'email': payload.get('email'),
            'timezone': _normalize_timezone(payload.get('timezone') or 'UTC'),
            'role': payload.get('role') or 'member',
            'status': payload.get('status') or 'offline',
            'availability': availability_slots,  # Store as dict, not array
            'teams': payload.get('teams') or [],
            'avatar': payload.get('avatar'),
            'createdAt': payload.get('createdAt'),
            'password_hash': payload.get('password_hash'),
        }

    # Read operations (API shapes)
    @classmethod
    def list_members(cls) -> List[Dict[str, Any]]:
        storage = cls._load_storage()
        return [cls._to_api(rec, i) for i, rec in enumerate(storage)]

    @classmethod
    def get_member(cls, member_id: str) -> Optional[Dict[str, Any]]:
        storage = cls._load_storage()
        for i, rec in enumerate(storage):
            api = cls._to_api(rec, i)
            if api['id'] == member_id:
                return api
        return None

    @classmethod
    def get_member_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        storage = cls._load_storage()
        for i, rec in enumerate(storage):
            if (rec.get('name') or '').strip() == (name or '').strip():
                return cls._to_api(rec, i)
        return None

    # Write operations (persist in storage format)
    @classmethod
    def create_member(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        with update_json(MEMBERS_FILE, default_factory=list) as data:
            record = cls._from_api(payload)
            data.append(record)
        # Return API view
        storage = cls._load_storage()
        return cls._to_api(storage[-1], len(storage) - 1)

    @classmethod
    def update_member(cls, member_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        storage = cls._load_storage()
        updated: Optional[Dict[str, Any]] = None
        for idx, rec in enumerate(storage):
            api = cls._to_api(rec, idx)
            if api['id'] == member_id:
                # merge updates (API level), then convert back to storage
                merged_api = {**api, **updates}
                new_storage_record = cls._from_api(merged_api)
                # Preserve sensitive/critical fields that are not part of API surface
                # Specifically ensure password_hash is never dropped unless explicitly provided
                if new_storage_record.get('password_hash') is None and rec.get('password_hash') is not None:
                    new_storage_record['password_hash'] = rec.get('password_hash')
                # Preserve createdAt if not provided
                if new_storage_record.get('createdAt') is None and rec.get('createdAt') is not None:
                    new_storage_record['createdAt'] = rec.get('createdAt')
                # Preserve avatar if not provided (profile updates may not send it)
                if new_storage_record.get('avatar') is None and rec.get('avatar') is not None:
                    new_storage_record['avatar'] = rec.get('avatar')

                storage[idx] = new_storage_record
                updated = cls._to_api(storage[idx], idx)
                break
        if updated is not None:
            cls._save_storage(storage)
        return updated

    @classmethod
    def update_availability(cls, member_id: str, availability: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return cls.update_member(member_id, {'availability': availability})

    @classmethod
    def delete_member(cls, member_id: str) -> bool:
        storage = cls._load_storage()
        kept: List[Dict[str, Any]] = []
        removed = False
        for idx, rec in enumerate(storage):
            api = cls._to_api(rec, idx)
            if api['id'] == member_id:
                removed = True
                continue
            kept.append(rec)
        if removed:
            cls._save_storage(kept)
        return removed

