"""
Auth routes for /api/v1/auth.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException

from controllers.auth_controller import AuthController
from schemas.auth import LoginRequest, RegisterRequest, UpdateProfileRequest
from utils.auth import get_current_user


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
controller = AuthController()


@router.post("/login")
async def login(payload: LoginRequest):
    return await controller.login(payload)


@router.post("/register")
async def register(payload: RegisterRequest):
    return await controller.register(payload)


@router.post("/logout")
async def logout():
    return await controller.logout()


def _require_user_id(authorization: str | None = Header(default=None)) -> str:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id


@router.get("/profile")
async def get_profile(user_id: str = Depends(_require_user_id)):
    return await controller.get_profile(user_id)


@router.put("/profile")
async def update_profile(payload: UpdateProfileRequest, user_id: str = Depends(_require_user_id)):
    return await controller.update_profile(user_id, payload)


@router.post("/verify")
async def verify(authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    return await controller.verify_token(token or "")

