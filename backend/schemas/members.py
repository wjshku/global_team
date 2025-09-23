from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from schemas.common import AvailabilityMap


class CreateMemberRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = None
    timezone: str = Field('UTC')


class UpdateMemberRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = None
    timezone: Optional[str] = None


class UpdateAvailabilityRequest(BaseModel):
    availability: AvailabilityMap


class MemberResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    timezone: str
    role: str
    status: str
    availability: AvailabilityMap
    teams: List[str] = []
    avatar: Optional[str] = None
    createdAt: Optional[str] = None


class ListMembersResponse(BaseModel):
    items: List[MemberResponse]


