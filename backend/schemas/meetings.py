from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class MeetingOption(BaseModel):
    timeSlot: str
    duration: Optional[int] = None


class CreateMeetingRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    timeSlots: Optional[List[str]] = None  # Array of ISO strings for voting
    scheduledTime: Optional[str] = None  # ISO string for final scheduled time
    votingStart: Optional[str] = None
    votingEnd: Optional[str] = None
    duration: Optional[int] = None  # Duration in minutes
    timezone: Optional[str] = None  # Timezone for the meeting
    # Frontend may submit detailed options instead of timeSlots
    options: Optional[List[MeetingOption]] = None


class UpdateMeetingRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    timeSlots: Optional[List[str]] = None
    scheduledTime: Optional[str] = None
    votingStart: Optional[str] = None
    votingEnd: Optional[str] = None
    duration: Optional[int] = None
    timezone: Optional[str] = None
    status: Optional[str] = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    creatorId: Optional[str] = None
    teamId: Optional[str] = None
    timeSlots: Optional[List[str]] = None
    scheduledTime: Optional[str] = None
    votingStart: Optional[str] = None
    votingEnd: Optional[str] = None
    duration: Optional[int] = None
    timezone: Optional[str] = None
    status: str
    createdAt: Optional[str] = None


class ListMeetingsResponse(BaseModel):
    items: List[MeetingResponse]


class SubmitVoteRequest(BaseModel):
    userId: str
    timeSlot: str
    preference: str = Field('medium')  # low, medium, high


class VoteResponse(BaseModel):
    id: str
    meetingId: str
    userId: str
    timeSlot: str
    preference: str
    createdAt: Optional[str] = None


class VoteResultsResponse(BaseModel):
    # { timeSlot: { votes: n, preference: highestPreference } }
    results: dict


