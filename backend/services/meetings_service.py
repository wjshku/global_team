"""
Meetings service.

Implements meeting CRUD, votes, and meeting participants retrieval.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from models.meeting_model import MeetingModel
from models.vote_model import VoteModel
from models.team_model import TeamModel
from models.user_model import UserModel
from utils.errors import ConflictError, NotFoundError, ValidationError
from utils.validation import sanitize_input
from utils.time import parse_iso_datetime, convert_to_utc
from datetime import timezone


class MeetingsService:
    """Meeting management service."""

    def create_meeting(self, team_id: str, meeting_data: Dict, creator_id: str | None = None) -> Dict:
        """Create a new meeting for a team."""
        data = sanitize_input(meeting_data)
        
        if not data.get('title'):
            raise ValidationError("Meeting title is required")
        
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        # Validate scheduled time if provided
        if 'scheduledTime' in data and data['scheduledTime']:
            try:
                from utils.time import parse_iso_datetime
                parse_iso_datetime(data['scheduledTime'])
            except Exception:
                raise ValidationError("Invalid scheduledTime format. Use ISO 8601 format.")
        
        # Validate voting times if provided
        if 'votingStart' in data and data['votingStart']:
            try:
                from utils.time import parse_iso_datetime
                parse_iso_datetime(data['votingStart'])
            except Exception:
                raise ValidationError("Invalid votingStart format. Use ISO 8601 format.")
        
        if 'votingEnd' in data and data['votingEnd']:
            try:
                from utils.time import parse_iso_datetime
                parse_iso_datetime(data['votingEnd'])
            except Exception:
                raise ValidationError("Invalid votingEnd format. Use ISO 8601 format.")
        
        # Extract timeSlots from options if provided
        time_slots = data.get('timeSlots')
        if not time_slots and data.get('options'):
            # Convert options array to timeSlots array
            time_slots = [option.get('timeSlot') for option in data['options'] if option.get('timeSlot')]
        
        tz_name = data.get('timezone')

        # Normalize all times to UTC ISO strings
        def to_utc_iso(value: Optional[str]) -> Optional[str]:
            if not value:
                return value
            try:
                # If value lacks explicit offset and timezone provided, interpret in that timezone
                has_offset = isinstance(value, str) and ('+' in value or value.endswith('Z'))
                if tz_name and not has_offset:
                    # Parse naive as local date-time and convert using tz_name
                    from datetime import datetime
                    dt_naive = datetime.fromisoformat(value)
                    dt = convert_to_utc(dt_naive, tz_name)
                else:
                    dt = parse_iso_datetime(value)
                return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            except Exception:
                return value  # validation above will catch wrong formats
        
        time_slots_utc = [to_utc_iso(ts) for ts in (time_slots or [])]
        
        meeting_payload = {
            'title': data['title'],
            'description': data.get('description'),
            'creatorId': creator_id,
            'timeSlots': time_slots_utc or None,
            'scheduledTime': to_utc_iso(data.get('scheduledTime')),
            'votingStart': to_utc_iso(data.get('votingStart')),
            'votingEnd': to_utc_iso(data.get('votingEnd')),
            'duration': data.get('duration'),
            'timezone': data.get('timezone'),
            'status': data.get('status', 'scheduled')
        }
        
        return MeetingModel.create_meeting(team_id, meeting_payload)

    def get_meeting(self, meeting_id: str) -> Optional[Dict]:
        """Get meeting by ID."""
        return MeetingModel.get_meeting(meeting_id)

    def list_meetings(self) -> List[Dict]:
        """List all meetings."""
        return MeetingModel.list_meetings()

    def list_team_meetings(self, team_id: str) -> List[Dict]:
        """List meetings for a specific team."""
        # Validate team exists
        team = TeamModel.get_team(team_id)
        if not team:
            raise NotFoundError("Team not found")
        
        return MeetingModel.list_meetings_by_team(team_id)

    def update_meeting(self, meeting_id: str, updates: Dict) -> Optional[Dict]:
        """Update meeting with validation."""
        data = sanitize_input(updates)
        
        # Validate meeting exists
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        # Validate time formats if provided
        for time_field in ['scheduledTime', 'votingStart', 'votingEnd']:
            if time_field in data and data[time_field]:
                try:
                    from utils.time import parse_iso_datetime
                    parse_iso_datetime(data[time_field])
                except Exception:
                    raise ValidationError(f"Invalid {time_field} format. Use ISO 8601 format.")
        
        return MeetingModel.update_meeting(meeting_id, data)

    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete meeting by ID."""
        # Also delete all votes for this meeting
        votes = VoteModel.list_votes(meeting_id)
        for vote in votes:
            # Note: VoteModel doesn't have delete method, but we could add one
            pass
        
        return MeetingModel.delete_meeting(meeting_id)

    def get_meeting_members(self, meeting_id: str) -> List[Dict]:
        """Get all members who can participate in a meeting."""
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        team_id = meeting.get('teamId')
        if not team_id:
            return []
        
        return TeamModel.get_team_members(team_id)

    def submit_vote(self, meeting_id: str, user_id: str, vote_data: Dict) -> Dict:
        """Submit a vote for a meeting."""
        data = sanitize_input(vote_data)
        
        # Validate meeting exists
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        # Validate user exists
        user = UserModel.get_member(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Validate user is a member of the meeting's team
        team_id = meeting.get('teamId')
        if team_id:
            team = TeamModel.get_team(team_id)
            if not team or user_id not in team['members']:
                raise ValidationError("User is not a member of this team")
        
        # Validate required fields
        if not data.get('timeSlot'):
            raise ValidationError("timeSlot is required")
        
        # Validate preference
        preference = data.get('preference', 'medium')
        if preference not in ['low', 'medium', 'high']:
            raise ValidationError("preference must be 'low', 'medium', or 'high'")
        
        vote_payload = {
            'userId': user_id,
            'timeSlot': data['timeSlot'],
            'preference': preference
        }
        
        return VoteModel.submit_vote(meeting_id, vote_payload)

    def get_meeting_votes(self, meeting_id: str) -> List[Dict]:
        """Get all votes for a meeting."""
        # Validate meeting exists
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        return VoteModel.list_votes(meeting_id)

    def get_vote_results(self, meeting_id: str) -> Dict:
        """Get aggregated vote results for a meeting."""
        # Validate meeting exists
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        # Aggregate existing votes
        results = VoteModel.aggregate_results(meeting_id)
        
        # Ensure all proposed timeSlots are present with zero votes so UI can render options
        time_slots = meeting.get('timeSlots') or []
        for slot in time_slots:
            if slot not in results:
                results[slot] = {'votes': 0, 'preference': 'low', 'duration': meeting.get('duration')}
            else:
                # Enrich with duration if available
                if 'duration' not in results[slot]:
                    results[slot]['duration'] = meeting.get('duration')
        
        return {'results': results}

    def get_meeting_participants(self, meeting_id: str) -> List[Dict]:
        """Get meeting participants with their vote status."""
        meeting = MeetingModel.get_meeting(meeting_id)
        if not meeting:
            raise NotFoundError("Meeting not found")
        
        # Get team members
        team_id = meeting.get('teamId')
        if not team_id:
            return []
        
        members = TeamModel.get_team_members(team_id)
        
        # Get votes for this meeting
        votes = VoteModel.list_votes(meeting_id)
        vote_by_user = {vote['userId']: vote for vote in votes}
        
        # Add vote status to each member
        for member in members:
            member['hasVoted'] = member['id'] in vote_by_user
            if member['hasVoted']:
                member['vote'] = vote_by_user[member['id']]
        
        return members
