"""
Meetings routes for /api/v1/meetings.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException

from controllers.meetings_controller import MeetingsController
from schemas.meetings import CreateMeetingRequest, UpdateMeetingRequest, SubmitVoteRequest
from utils.auth import get_current_user


router = APIRouter(prefix="/api/v1/meetings", tags=["Meetings"])
controller = MeetingsController()


def _require_user_id(authorization: str | None = Header(default=None)) -> str:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id


@router.get("")
async def list_meetings():
    return await controller.list_meetings()


# Deprecated in favor of /teams/{team_id}/meetings alias in teams routes


@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str):
    return await controller.get_meeting(meeting_id)


# Deprecated in favor of /teams/{team_id}/meetings alias in teams routes


@router.put("/{meeting_id}")
async def update_meeting(meeting_id: str, payload: UpdateMeetingRequest, user_id: str = Depends(_require_user_id)):
    return await controller.update_meeting(meeting_id, payload)


@router.delete("/{meeting_id}")
async def delete_meeting(meeting_id: str, user_id: str = Depends(_require_user_id)):
    return await controller.delete_meeting(meeting_id)


@router.get("/{meeting_id}/members")
async def get_meeting_members(meeting_id: str):
    return await controller.get_meeting_members(meeting_id)


@router.get("/{meeting_id}/votes")
async def get_meeting_votes(meeting_id: str):
    return await controller.get_meeting_votes(meeting_id)


@router.post("/{meeting_id}/votes")
async def submit_vote(meeting_id: str, user_id: str = Depends(_require_user_id), payload: SubmitVoteRequest | None = None):
    payload = payload or SubmitVoteRequest(userId=user_id, timeSlot="", preference="medium")
    data = payload.dict()
    data['userId'] = user_id
    return await controller.submit_vote(meeting_id, user_id, SubmitVoteRequest(**data))


@router.get("/{meeting_id}/results")
async def get_vote_results(meeting_id: str):
    return await controller.get_vote_results(meeting_id)

