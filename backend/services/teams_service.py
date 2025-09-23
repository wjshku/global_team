"""
Teams service.

Implements team CRUD, membership management, and listing team meetings.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from models.team_model import TeamModel
from models.user_model import UserModel
from models.meeting_model import MeetingModel
from utils.errors import ConflictError, NotFoundError, ValidationError
from utils.validation import sanitize_input


class TeamsService:
    """Team management service."""

    def create_team(self, team_data: Dict, creator_id: str) -> Dict:
        """Create a new team with validation."""
        data = sanitize_input(team_data)
        
        if not data.get('name'):
            raise ValidationError("Team name is required")
        
        # Check if team already exists
        existing_teams = TeamModel.list_teams()
        for team in existing_teams:
            if team['name'].lower() == data['name'].lower():
                raise ConflictError("Team with this name already exists")
        
        # Validate creator exists
        creator = UserModel.get_member(creator_id)
        if not creator:
            raise NotFoundError("Creator not found")
        
        # Add creator to members list if not already included
        members = data.get('members', [])
        if creator_id not in members:
            members.append(creator_id)
        
        # Validate all member IDs exist
        for member_id in members:
            if not UserModel.get_member(member_id):
                raise NotFoundError(f"Member {member_id} not found")
        
        team_payload = {
            'name': data['name'],
            'description': data.get('description'),
            'timezone': data.get('timezone'),
            'members': members
        }
        
        return TeamModel.create_team(team_payload)

    def get_team(self, team_id: str) -> Optional[Dict]:
        """Get team by ID."""
        return TeamModel.get_team(team_id)

    def list_teams(self) -> List[Dict]:
        """List all teams."""
        return TeamModel.list_teams()

    def update_team(self, team_id: str, updates: Dict, user_id: str) -> Optional[Dict]:
        """Update team with validation."""
        data = sanitize_input(updates)
        
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if user is team admin
        if team.get('admin') != user_id:
            raise PermissionError("Only team admin can update team")
        
        # Validate timezone if provided
        if 'timezone' in data and data['timezone']:
            from utils.validation import validate_timezone
            if not validate_timezone(data['timezone']):
                raise ValidationError("Invalid timezone")
        
        # Validate all member IDs exist if provided
        if 'members' in data:
            for member_id in data['members']:
                if not UserModel.get_member(member_id):
                    raise NotFoundError(f"Member {member_id} not found")
        
        return TeamModel.update_team(team_id, data)

    def delete_team(self, team_id: str, user_id: str) -> bool:
        """Delete team by ID."""
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if user is team admin
        if team.get('admin') != user_id:
            raise PermissionError("Only team admin can delete team")
        
        return TeamModel.delete_team(team_id)

    def add_member_to_team(self, team_id: str, member_id: str, user_id: str) -> Dict:
        """Add member to team."""
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if user is team admin
        if team.get('admin') != user_id:
            raise PermissionError("Only team admin can add members")
        
        # Validate member exists
        member = UserModel.get_member(member_id)
        if not member:
            raise NotFoundError("Member not found")
        
        # Check if member is already in team
        if member_id in team['members']:
            raise ConflictError("Member is already in this team")
        
        # Add member to team
        updated_members = team['members'] + [member_id]
        updated_team = TeamModel.update_team(team_id, {'members': updated_members})
        
        if not updated_team:
            raise NotFoundError("Failed to update team")
        
        return updated_team

    def remove_member_from_team(self, team_id: str, member_id: str, user_id: str) -> Dict:
        """Remove member from team."""
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Check if user is team admin
        if team.get('admin') != user_id:
            raise PermissionError("Only team admin can remove members")
        
        # Check if member is in team
        if member_id not in team['members']:
            raise NotFoundError("Member is not in this team")
        
        # Remove member from team
        updated_members = [mid for mid in team['members'] if mid != member_id]
        updated_team = TeamModel.update_team(team_id, {'members': updated_members})
        
        if not updated_team:
            raise NotFoundError("Failed to update team")
        
        return updated_team

    def get_team_members(self, team_id: str) -> List[Dict]:
        """Get all members of a team."""
        return TeamModel.get_team_members(team_id)

    def get_team_with_members(self, team_id: str) -> Optional[Dict]:
        """Get team with full member details."""
        team = TeamModel.get_team(team_id)
        if not team:
            return None
        
        # Get full member details
        members = TeamModel.get_team_members(team_id)
        team['members'] = members
        
        return team

    def get_team_meetings(self, team_id: str) -> List[Dict]:
        """Get all meetings for a team."""
        return MeetingModel.list_meetings_by_team(team_id)
