"""
Members controller.

Handles member CRUD operations, availability management, and team membership.
"""

from __future__ import annotations

from typing import List

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services.members_service import MembersService
from schemas.members import CreateMemberRequest, UpdateMemberRequest, MemberResponse, ListMembersResponse, UpdateAvailabilityRequest
from utils.errors import ValidationError, NotFoundError, ConflictError


class MembersController:
    """Members controller handling HTTP requests."""

    def __init__(self):
        self.members_service = MembersService()

    async def list_members(self) -> JSONResponse:
        """List all members."""
        try:
            members = self.members_service.list_members()
            # Return raw array for frontend expectations
            return JSONResponse(status_code=200, content=members)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_member(self, member_id: str) -> JSONResponse:
        """Get member by ID."""
        try:
            member = self.members_service.get_member(member_id)
            if not member:
                raise HTTPException(status_code=404, detail="Member not found")
            
            response_data = MemberResponse(**member)
            return JSONResponse(status_code=200, content=response_data.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_member(self, request: CreateMemberRequest) -> JSONResponse:
        """Create a new member."""
        try:
            member_data = request.dict()
            member = self.members_service.create_member(member_data)
            
            response_data = MemberResponse(**member)
            return JSONResponse(status_code=201, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_member(self, member_id: str, request: UpdateMemberRequest) -> JSONResponse:
        """Update member."""
        try:
            updates = request.dict(exclude_unset=True)
            member = self.members_service.update_member(member_id, updates)
            
            if not member:
                raise HTTPException(status_code=404, detail="Member not found")
            
            response_data = MemberResponse(**member)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_member(self, member_id: str) -> JSONResponse:
        """Delete member."""
        try:
            success = self.members_service.delete_member(member_id)
            if not success:
                raise HTTPException(status_code=404, detail="Member not found")
            
            return JSONResponse(status_code=200, content={"message": "Member deleted successfully"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_availability(self, member_id: str, request: UpdateAvailabilityRequest) -> JSONResponse:
        """Update member availability."""
        try:
            availability = request.availability.dict()
            member = self.members_service.update_availability(member_id, availability)
            
            if not member:
                raise HTTPException(status_code=404, detail="Member not found")
            
            response_data = MemberResponse(**member)
            return JSONResponse(status_code=200, content=response_data.dict())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_availability(self, member_id: str) -> JSONResponse:
        """Get member availability."""
        try:
            availability = self.members_service.get_availability(member_id)
            if availability is None:
                raise HTTPException(status_code=404, detail="Member not found")
            # Return raw map
            return JSONResponse(status_code=200, content=availability)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_member_teams(self, member_id: str) -> JSONResponse:
        """Get teams a member belongs to."""
        try:
            teams = self.members_service.get_member_teams(member_id)
            return JSONResponse(status_code=200, content=teams)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
