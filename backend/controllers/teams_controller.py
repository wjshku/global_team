"""
Teams controller.

Handles team CRUD operations, membership management, and team-related queries.
"""

from __future__ import annotations

from typing import List

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services.teams_service import TeamsService
from schemas.teams import CreateTeamRequest, UpdateTeamRequest, TeamResponse, ListTeamsResponse, TeamMembersResponse
from utils.errors import ValidationError, NotFoundError, ConflictError


class TeamsController:
    """Teams controller handling HTTP requests."""

    def __init__(self):
        self.teams_service = TeamsService()

    async def list_teams(self) -> JSONResponse:
        """List all teams."""
        try:
            teams = self.teams_service.list_teams()
            # Return raw array
            return JSONResponse(status_code=200, content=teams)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_team(self, team_id: str) -> JSONResponse:
        """Get team by ID."""
        try:
            team = self.teams_service.get_team(team_id)
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            
            response_data = TeamResponse(**team)
            return JSONResponse(status_code=200, content=response_data.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_team(self, request: CreateTeamRequest, creator_id: str) -> JSONResponse:
        """Create a new team."""
        try:
            team_data = request.dict()
            team = self.teams_service.create_team(team_data, creator_id)
            
            response_data = TeamResponse(**team)
            return JSONResponse(status_code=201, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_team(self, team_id: str, request: UpdateTeamRequest, user_id: str) -> JSONResponse:
        """Update team."""
        try:
            updates = request.dict(exclude_unset=True)
            team = self.teams_service.update_team(team_id, updates, user_id)
            
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            
            response_data = TeamResponse(**team)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_team(self, team_id: str, user_id: str) -> JSONResponse:
        """Delete team."""
        try:
            success = self.teams_service.delete_team(team_id, user_id)
            if not success:
                raise HTTPException(status_code=404, detail="Team not found")
            
            return JSONResponse(status_code=200, content={"deleted": True})
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_team_members(self, team_id: str) -> JSONResponse:
        """Get team members."""
        try:
            members = self.teams_service.get_team_members(team_id)
            # Return full member objects array
            return JSONResponse(status_code=200, content=members)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def add_member(self, team_id: str, member_id: str, user_id: str) -> JSONResponse:
        """Add member to team."""
        try:
            team = self.teams_service.add_member_to_team(team_id, member_id, user_id)
            response_data = TeamResponse(**team)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def remove_member(self, team_id: str, member_id: str, user_id: str) -> JSONResponse:
        """Remove member from team."""
        try:
            team = self.teams_service.remove_member_from_team(team_id, member_id, user_id)
            response_data = TeamResponse(**team)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
