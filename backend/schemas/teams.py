from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class CreateTeamRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    members: List[str] = []  # user IDs


class UpdateTeamRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    members: Optional[List[str]] = None


class TeamResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    timezone: Optional[str] = None
    members: List[str]
    admin: Optional[str] = None
    memberCount: int
    meetingCount: int
    createdAt: Optional[str] = None


class ListTeamsResponse(BaseModel):
    items: List[TeamResponse]


class TeamMembersResponse(BaseModel):
    teamId: str
    items: List[str]  # user IDs


