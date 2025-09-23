"""
Team model/data access.

MVP: read/write team records in backend/data/teams.json including member IDs.
Production: ORM model with teams and team_members tables.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from utils.storage import read_json, write_json, update_json
from models.user_model import UserModel


TEAMS_FILE = 'teams.json'


def _slugify(value: str) -> str:
    return ''.join(ch.lower() if ch.isalnum() else '-' for ch in (value or '').strip()).strip('-') or 'team'


class TeamModel:
    """Team data model for CRUD operations on teams.json."""


    @classmethod
    def list_teams(cls) -> List[Dict[str, Any]]:
        storage = read_json(TEAMS_FILE, default_factory=dict)
        return list(storage.values())

    @classmethod
    def get_team(cls, team_id: str) -> Optional[Dict[str, Any]]:
        storage = read_json(TEAMS_FILE, default_factory=dict)
        return storage.get(team_id)

    @classmethod
    def get_team_members(cls, team_id: str) -> List[Dict[str, Any]]:
        team = cls.get_team(team_id)
        if not team:
            return []
        members: List[Dict[str, Any]] = []
        for mid in team.get('members', []):
            user = UserModel.get_member(mid)
            if user:
                members.append(user)
        return members

    @classmethod
    def create_team(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        import uuid
        from datetime import datetime
        
        name = (payload.get('name') or '').strip() or 'New Team'
        members_ids: List[str] = payload.get('members') or []
        description = payload.get('description')
        timezone = payload.get('timezone')
        
        # Generate unique team ID
        team_id = f"{_slugify(name)}-{str(uuid.uuid4())[:8]}"
        
        # Create team data in API format
        team_data = {
            'id': team_id,
            'name': name,
            'description': description,
            'timezone': timezone,
            'members': members_ids,
            'admin': members_ids[0] if members_ids else None,
            'memberCount': len(members_ids),
            'meetingCount': 0,
            'createdAt': datetime.now().isoformat()
        }
        
        # Load existing teams and add new team
        existing_teams = read_json(TEAMS_FILE, default_factory=dict)
        existing_teams[team_id] = team_data
        
        # Save updated teams
        write_json(TEAMS_FILE, existing_teams)
        
        return team_data

    @classmethod
    def update_team(cls, team_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        storage = read_json(TEAMS_FILE, default_factory=dict)
        
        if team_id not in storage:
            return None
            
        team = storage[team_id]
        
        # Update team data with provided updates
        for key, value in updates.items():
            if key in team:
                team[key] = value
        
        # Recalculate computed fields
        if 'members' in updates:
            team['memberCount'] = len(team['members'])
            team['admin'] = team['members'][0] if team['members'] else None
        
        # Save updated data
        write_json(TEAMS_FILE, storage)
        
        return team

    @classmethod
    def delete_team(cls, team_id: str) -> bool:
        storage = read_json(TEAMS_FILE, default_factory=dict)
        
        if team_id in storage:
            del storage[team_id]
            write_json(TEAMS_FILE, storage)
            return True
        return False

