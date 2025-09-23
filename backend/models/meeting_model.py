"""
Meeting model/data access.

MVP: read/write meeting records in backend/data/meetings.json.
Production: ORM model with meetings table.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from utils.storage import read_json, write_json, update_json


MEETINGS_FILE = 'meetings.json'


class MeetingModel:
    @staticmethod
    def _load_storage() -> List[Dict[str, Any]]:
        return list(read_json(MEETINGS_FILE, default_factory=list) or [])

    @staticmethod
    def _save_storage(records: List[Dict[str, Any]]) -> None:
        write_json(MEETINGS_FILE, records)

    @staticmethod
    def _to_api(rec: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': rec.get('id') or rec.get('_id') or None,
            'title': rec.get('title'),
            'description': rec.get('description'),
            'creatorId': rec.get('creatorId'),
            'teamId': rec.get('teamId'),
            'timeSlots': rec.get('timeSlots'),
            'scheduledTime': rec.get('scheduledTime'),
            'votingStart': rec.get('votingStart'),
            'votingEnd': rec.get('votingEnd'),
            'duration': rec.get('duration'),
            'timezone': rec.get('timezone'),
            'status': rec.get('status') or 'scheduled',
            'createdAt': rec.get('createdAt'),
        }

    @staticmethod
    def _from_api(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': payload.get('id') or payload.get('meetId'),
            'title': payload.get('title'),
            'description': payload.get('description'),
            'creatorId': payload.get('creatorId'),
            'teamId': payload.get('teamId'),
            'timeSlots': payload.get('timeSlots'),
            'scheduledTime': payload.get('scheduledTime'),
            'votingStart': payload.get('votingStart'),
            'votingEnd': payload.get('votingEnd'),
            'duration': payload.get('duration'),
            'timezone': payload.get('timezone'),
            'status': payload.get('status') or 'scheduled',
            'createdAt': payload.get('createdAt'),
        }

    @classmethod
    def list_meetings(cls) -> List[Dict[str, Any]]:
        return [cls._to_api(m) for m in cls._load_storage()]

    @classmethod
    def list_meetings_by_team(cls, team_id: str) -> List[Dict[str, Any]]:
        return [cls._to_api(m) for m in cls._load_storage() if m.get('teamId') == team_id]

    @classmethod
    def get_meeting(cls, meeting_id: str) -> Optional[Dict[str, Any]]:
        for m in cls._load_storage():
            if (m.get('id') or m.get('_id')) == meeting_id:
                return cls._to_api(m)
        return None

    @classmethod
    def create_meeting(cls, team_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        import uuid
        from datetime import datetime
        
        record = cls._from_api({**payload, 'teamId': team_id})
        if not record.get('id'):
            record['id'] = str(uuid.uuid4())
        
        # Set createdAt if not provided
        if not record.get('createdAt'):
            record['createdAt'] = datetime.utcnow().isoformat() + 'Z'
        
        with update_json(MEETINGS_FILE, default_factory=list) as data:
            data.append(record)
        return cls._to_api(record)

    @classmethod
    def update_meeting(cls, meeting_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        storage = cls._load_storage()
        for idx, rec in enumerate(storage):
            if (rec.get('id') or rec.get('_id')) != meeting_id:
                continue
            # Perform a partial update: only apply fields explicitly provided in updates
            # without overriding other existing fields.
            merged = dict(rec)
            # Allowed updatable fields in API naming
            allowed_keys = {
                'title', 'description', 'timeSlots', 'scheduledTime',
                'votingStart', 'votingEnd', 'duration', 'timezone', 'status'
            }
            for key, value in updates.items():
                if key in allowed_keys:
                    merged[key] = value
            storage[idx] = merged
            cls._save_storage(storage)
            return cls._to_api(merged)
        return None

    @classmethod
    def delete_meeting(cls, meeting_id: str) -> bool:
        storage = cls._load_storage()
        kept: List[Dict[str, Any]] = []
        removed = False
        for rec in storage:
            if (rec.get('id') or rec.get('_id')) == meeting_id:
                removed = True
                continue
            kept.append(rec)
        if removed:
            cls._save_storage(kept)
        return removed

