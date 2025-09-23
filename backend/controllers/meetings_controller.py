"""
Meetings controller.

Handles meeting CRUD operations, voting system, and meeting participants.
"""

from __future__ import annotations

from typing import List

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services.meetings_service import MeetingsService
from schemas.meetings import CreateMeetingRequest, UpdateMeetingRequest, MeetingResponse, ListMeetingsResponse, SubmitVoteRequest, VoteResponse, VoteResultsResponse
from utils.errors import ValidationError, NotFoundError, ConflictError


class MeetingsController:
    """Meetings controller handling HTTP requests."""

    def __init__(self):
        self.meetings_service = MeetingsService()

    async def list_meetings(self) -> JSONResponse:
        """List all meetings."""
        try:
            meetings = self.meetings_service.list_meetings()
            # Return raw array for frontend expectations
            return JSONResponse(status_code=200, content=meetings)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def list_team_meetings(self, team_id: str) -> JSONResponse:
        """List meetings for a team."""
        try:
            meetings = self.meetings_service.list_team_meetings(team_id)
            return JSONResponse(status_code=200, content=meetings)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_meeting(self, meeting_id: str) -> JSONResponse:
        """Get meeting by ID."""
        try:
            meeting = self.meetings_service.get_meeting(meeting_id)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            
            response_data = MeetingResponse(**meeting)
            return JSONResponse(status_code=200, content=response_data.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_meeting(self, team_id: str, request: CreateMeetingRequest, creator_id: str | None = None) -> JSONResponse:
        """Create a new meeting."""
        try:
            meeting_data = request.dict()
            meeting = self.meetings_service.create_meeting(team_id, meeting_data, creator_id)
            
            response_data = MeetingResponse(**meeting)
            return JSONResponse(status_code=201, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_meeting(self, meeting_id: str, request: UpdateMeetingRequest) -> JSONResponse:
        """Update meeting."""
        try:
            updates = request.dict(exclude_unset=True)
            meeting = self.meetings_service.update_meeting(meeting_id, updates)
            
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            
            response_data = MeetingResponse(**meeting)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_meeting(self, meeting_id: str) -> JSONResponse:
        """Delete meeting."""
        try:
            success = self.meetings_service.delete_meeting(meeting_id)
            if not success:
                raise HTTPException(status_code=404, detail="Meeting not found")
            
            return JSONResponse(status_code=200, content={"deleted": True})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_meeting_members(self, meeting_id: str) -> JSONResponse:
        """Get meeting members."""
        try:
            members = self.meetings_service.get_meeting_members(meeting_id)
            return JSONResponse(status_code=200, content=members)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_meeting_votes(self, meeting_id: str) -> JSONResponse:
        """Get meeting votes."""
        try:
            votes = self.meetings_service.get_meeting_votes(meeting_id)
            response_data = [VoteResponse(**vote) for vote in votes]
            return JSONResponse(status_code=200, content=[v.dict() for v in response_data])
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def submit_vote(self, meeting_id: str, user_id: str, request: SubmitVoteRequest) -> JSONResponse:
        """Submit vote for meeting."""
        try:
            vote_data = request.dict()
            vote = self.meetings_service.submit_vote(meeting_id, user_id, vote_data)
            
            response_data = VoteResponse(**vote)
            return JSONResponse(status_code=201, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_vote_results(self, meeting_id: str) -> JSONResponse:
        """Get vote results for meeting."""
        try:
            results = self.meetings_service.get_vote_results(meeting_id)
            # Return raw dict (results)
            return JSONResponse(status_code=200, content=results.get('results') if isinstance(results, dict) else results)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_meeting_participants(self, meeting_id: str) -> JSONResponse:
        """Get meeting participants with vote status."""
        try:
            participants = self.meetings_service.get_meeting_participants(meeting_id)
            return JSONResponse(status_code=200, content={"participants": participants})
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
