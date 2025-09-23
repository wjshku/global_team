"""
Members routes for /api/v1/members.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException

from controllers.members_controller import MembersController
from schemas.members import CreateMemberRequest, UpdateMemberRequest, UpdateAvailabilityRequest
from utils.auth import get_current_user


router = APIRouter(prefix="/api/v1/members", tags=["Members"])
controller = MembersController()


def _require_user_id(authorization: str | None = Header(default=None)) -> str:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id


@router.get("")
async def list_members():
    return await controller.list_members()


@router.get("/{member_id}")
async def get_member(member_id: str):
    return await controller.get_member(member_id)


@router.post("")
async def create_member(payload: CreateMemberRequest, user_id: str = Depends(_require_user_id)):
    return await controller.create_member(payload)


@router.put("/{member_id}")
async def update_member(member_id: str, payload: UpdateMemberRequest, user_id: str = Depends(_require_user_id)):
    return await controller.update_member(member_id, payload)


@router.delete("/{member_id}")
async def delete_member(member_id: str, user_id: str = Depends(_require_user_id)):
    return await controller.delete_member(member_id)


@router.get("/{member_id}/availability")
async def get_availability(member_id: str):
    return await controller.get_availability(member_id)


@router.put("/{member_id}/availability")
async def update_availability(member_id: str, payload: UpdateAvailabilityRequest, user_id: str = Depends(_require_user_id)):
    return await controller.update_availability(member_id, payload)


@router.get("/{member_id}/teams")
async def get_member_teams(member_id: str):
    return await controller.get_member_teams(member_id)

