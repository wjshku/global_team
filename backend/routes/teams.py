"""
Teams routes for /api/v1/teams.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Body

from controllers.teams_controller import TeamsController
from controllers.meetings_controller import MeetingsController
from schemas.meetings import CreateMeetingRequest
from schemas.teams import CreateTeamRequest, UpdateTeamRequest
from utils.auth import get_current_user


router = APIRouter(prefix="/api/v1/teams", tags=["Teams"])
controller = TeamsController()
meetings_controller = MeetingsController()


def _require_user_id(authorization: str | None = Header(default=None)) -> str:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id


@router.get("")
async def list_teams():
    return await controller.list_teams()


@router.get("/{team_id}")
async def get_team(team_id: str):
    return await controller.get_team(team_id)


@router.post("")
async def create_team(payload: CreateTeamRequest, user_id: str = Depends(_require_user_id)):
    return await controller.create_team(payload, user_id)


@router.put("/{team_id}")
async def update_team(team_id: str, payload: UpdateTeamRequest, user_id: str = Depends(_require_user_id)):
    return await controller.update_team(team_id, payload, user_id)


@router.delete("/{team_id}")
async def delete_team(team_id: str, user_id: str = Depends(_require_user_id)):
    return await controller.delete_team(team_id, user_id)


@router.get("/{team_id}/members")
async def get_team_members(team_id: str):
    return await controller.get_team_members(team_id)


@router.post("/{team_id}/members/{member_id}")
async def add_member(team_id: str, member_id: str, user_id: str = Depends(_require_user_id)):
    return await controller.add_member(team_id, member_id, user_id)


@router.delete("/{team_id}/members/{member_id}")
async def remove_member(team_id: str, member_id: str, user_id: str = Depends(_require_user_id)):
    return await controller.remove_member(team_id, member_id, user_id)


# Aliases expected by frontend
@router.post("/{team_id}/members")
async def add_member_body(team_id: str, payload: dict = Body(...), user_id: str = Depends(_require_user_id)):
    member_id = payload.get("memberId")
    if not member_id:
        raise HTTPException(status_code=400, detail="memberId is required")
    return await controller.add_member(team_id, member_id, user_id)


@router.get("/{team_id}/meetings")
async def list_team_meetings_alias(team_id: str):
    return await meetings_controller.list_team_meetings(team_id)


@router.post("/{team_id}/meetings")
async def create_team_meeting_alias(team_id: str, payload: CreateMeetingRequest, user_id: str = Depends(_require_user_id)):
    return await meetings_controller.create_meeting(team_id, payload, user_id)

