"""
Vote model/data access.

MVP: read/write vote records in backend/data/votes.json.
Production: ORM model with votes table.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from utils.storage import read_json, write_json, update_json


VOTES_FILE = 'votes.json'


class VoteModel:
    @staticmethod
    def _load_storage() -> List[Dict[str, Any]]:
        return list(read_json(VOTES_FILE, default_factory=list) or [])

    @staticmethod
    def _save_storage(records: List[Dict[str, Any]]) -> None:
        write_json(VOTES_FILE, records)

    @staticmethod
    def _to_api(rec: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': rec.get('id'),
            'meetingId': rec.get('meetingId'),
            'userId': rec.get('userId'),
            'timeSlot': rec.get('timeSlot'),
            'preference': rec.get('preference') or rec.get('Preference') or 'medium',
            'createdAt': rec.get('createdAt'),
        }

    @staticmethod
    def _from_api(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': payload.get('id'),
            'meetingId': payload.get('meetingId') or payload.get('meetId'),
            'userId': payload.get('userId'),
            'timeSlot': payload.get('timeSlot'),
            'preference': payload.get('preference') or payload.get('Preference') or 'medium',
            'createdAt': payload.get('createdAt'),
        }

    @classmethod
    def list_votes(cls, meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
        votes = [cls._to_api(v) for v in cls._load_storage()]
        if meeting_id is None:
            return votes
        return [v for v in votes if v.get('meetingId') == meeting_id]

    @classmethod
    def submit_vote(cls, meeting_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        import uuid
        from datetime import datetime
        
        record = cls._from_api({**payload, 'meetingId': meeting_id})
        if not record.get('id'):
            record['id'] = str(uuid.uuid4())
        
        if not record.get('createdAt'):
            record['createdAt'] = datetime.utcnow().isoformat() + 'Z'
        
        with update_json(VOTES_FILE, default_factory=list) as data:
            data[:] = [v for v in data if not (
                (v.get('meetingId') == record.get('meetingId')) and (v.get('userId') == record.get('userId'))
            )]
            data.append(record)
        return cls._to_api(record)

    @classmethod
    def aggregate_results(cls, meeting_id: str) -> Dict[str, Dict[str, Any]]:
        # Return { timeSlot: { votes: n, preference: highestPreference } }
        pref_rank = {'low': 1, 'medium': 2, 'high': 3}
        results: Dict[str, Dict[str, Any]] = {}
        for vote in cls._load_storage():
            if vote.get('meetingId') != meeting_id:
                continue
            slot = vote.get('timeSlot')
            pref = vote.get('preference') or 'medium'
            if not slot:
                continue
            bucket = results.setdefault(slot, {'votes': 0, 'preference': 'low'})
            bucket['votes'] += 1
            if pref_rank.get(pref, 0) > pref_rank.get(bucket['preference'], 0):
                bucket['preference'] = pref
        return results

