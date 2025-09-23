"""
Members service.

Implements member CRUD, availability get/update, and team membership queries.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from models.user_model import UserModel
from models.team_model import TeamModel
from utils.errors import ConflictError, NotFoundError, ValidationError
from utils.validation import validate_email, validate_timezone, sanitize_input


class MembersService:
    """Member management service."""

    def create_member(self, member_data: Dict) -> Dict:
        """Create a new member with validation."""
        data = sanitize_input(member_data)
        
        if not data.get('name'):
            raise ValidationError("Name is required")
        
        # Validate email if provided
        if 'email' in data and data['email']:
            if not validate_email(data['email']):
                raise ValidationError("Invalid email format")
        
        # Validate timezone
        timezone = data.get('timezone', 'UTC')
        if not validate_timezone(timezone):
            raise ValidationError("Invalid timezone")
        
        # Check if member already exists by name
        existing_member = UserModel.get_member_by_name(data['name'])
        if existing_member:
            raise ConflictError("Member with this name already exists")
        
        # Check if email already exists
        if 'email' in data and data['email']:
            all_members = UserModel.list_members()
            for member in all_members:
                if member.get('email') == data['email']:
                    raise ConflictError("Member with this email already exists")
        
        member_payload = {
            'name': data['name'],
            'email': data.get('email'),
            'timezone': timezone,
            'role': data.get('role', 'member'),
            'status': data.get('status', 'offline'),
            'availability': data.get('availability', {}),
            'teams': data.get('teams', []),
            'avatar': data.get('avatar')
        }
        
        return UserModel.create_member(member_payload)

    def get_member(self, member_id: str) -> Optional[Dict]:
        """Get member by ID."""
        return UserModel.get_member(member_id)

    def get_member_by_name(self, name: str) -> Optional[Dict]:
        """Get member by name."""
        return UserModel.get_member_by_name(name)

    def list_members(self) -> List[Dict]:
        """List all members."""
        # Base members from storage
        members = UserModel.list_members()

        # Build a mapping of member_id -> [team_ids] from teams.json
        teams = TeamModel.list_teams()
        member_to_team_ids: Dict[str, List[str]] = {}
        for team in teams:
            team_id = team.get('id')
            for mid in team.get('members', []) or []:
                if not isinstance(mid, str):
                    continue
                member_to_team_ids.setdefault(mid, []).append(team_id)

        # Enrich each member with computed team ids (union with any existing)
        enriched: List[Dict] = []
        for m in members:
            existing = m.get('teams') or []
            computed = member_to_team_ids.get(m.get('id'), [])
            # deduplicate while preserving order: existing first, then computed
            seen = set()
            merged: List[str] = []
            for tid in list(existing) + list(computed):
                if isinstance(tid, str) and tid not in seen:
                    seen.add(tid)
                    merged.append(tid)
            m_enriched = {**m, 'teams': merged}
            enriched.append(m_enriched)

        return enriched

    def update_member(self, member_id: str, updates: Dict) -> Optional[Dict]:
        """Update member with validation."""
        data = sanitize_input(updates)
        # Remove keys explicitly set to None to avoid nullifying fields
        data = {k: v for k, v in data.items() if v is not None}

        # Prevent sensitive/internal field updates through this path
        if 'password_hash' in data:
            del data['password_hash']
        
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        # Validate email if provided
        if 'email' in data and data['email']:
            if not validate_email(data['email']):
                raise ValidationError("Invalid email format")
            
            # Check if email is already used by another member
            all_members = UserModel.list_members()
            for m in all_members:
                if m['id'] != member_id and m.get('email') == data['email']:
                    raise ConflictError("Email already in use by another member")
        
        # Validate timezone if provided
        if 'timezone' in data and data['timezone']:
            if not validate_timezone(data['timezone']):
                raise ValidationError("Invalid timezone")
        
        return UserModel.update_member(member_id, data)

    def delete_member(self, member_id: str) -> bool:
        """Delete member by ID."""
        # Remove member from all teams first
        teams = TeamModel.list_teams()
        for team in teams:
            if member_id in team['members']:
                updated_members = [mid for mid in team['members'] if mid != member_id]
                TeamModel.update_team(team['id'], {'members': updated_members})
        
        return UserModel.delete_member(member_id)

    def update_availability(self, member_id: str, availability: Dict) -> Optional[Dict]:
        """Update member availability."""
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        return UserModel.update_availability(member_id, availability)

    def get_availability(self, member_id: str) -> Optional[Dict]:
        """Get member availability."""
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        return member.get('availability', {})

    def get_member_teams(self, member_id: str) -> List[Dict]:
        """Get all teams a member belongs to."""
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        all_teams = TeamModel.list_teams()
        member_teams = []
        
        for team in all_teams:
            if member_id in team['members']:
                member_teams.append(team)
        
        return member_teams

    def add_member_to_team(self, member_id: str, team_id: str) -> Dict:
        """Add member to team."""
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if member is already in team
        if member_id in team['members']:
            raise ConflictError("Member is already in this team")
        
        # Add member to team
        updated_members = team['members'] + [member_id]
        updated_team = TeamModel.update_team(team_id, {'members': updated_members})
        
        if not updated_team:
            raise NotFoundError("Failed to update team")
        
        return updated_team

    def remove_member_from_team(self, member_id: str, team_id: str) -> Dict:
        """Remove member from team."""
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if member is in team
        if member_id not in team['members']:
            raise NotFoundError("Member is not in this team")
        
        # Remove member from team
        updated_members = [mid for mid in team['members'] if mid != member_id]
        updated_team = TeamModel.update_team(team_id, {'members': updated_members})
        
        if not updated_team:
            raise NotFoundError("Failed to update team")
        
        return updated_team
