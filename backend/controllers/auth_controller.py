"""
Auth controller.

Handles registration, login (password hashing, token issuance), logout, profile,
and token verification.
"""

from __future__ import annotations

from typing import Dict

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services.auth_service import AuthService
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, ProfileResponse, UpdateProfileRequest
from utils.errors import ValidationError, UnauthorizedError, ConflictError


class AuthController:
    """Authentication controller handling HTTP requests."""

    def __init__(self):
        self.auth_service = AuthService()

    async def login(self, request: LoginRequest) -> JSONResponse:
        """Handle user login."""
        try:
            user = self.auth_service.authenticate_user(email=request.email, name=request.name, password=request.password)
            token = self.auth_service.generate_token(user['id'])
            
            response_data = TokenResponse(
                accessToken=token,
                tokenType="bearer"
            )
            
            return JSONResponse(
                status_code=200,
                content=response_data.dict()
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except UnauthorizedError as e:
            raise HTTPException(status_code=401, detail=str(e))

    async def register(self, request: RegisterRequest) -> JSONResponse:
        """Handle user registration."""
        try:
            user_data = request.dict()
            user = self.auth_service.register_user(user_data)
            
            # Generate token for immediate login
            token = self.auth_service.generate_token(user['id'])
            
            response_data = {
                "user": ProfileResponse(
                    id=user['id'],
                    name=user['name'],
                    email=user['email'],
                    timezone=user['timezone'],
                    role=user['role'],
                    avatar=user.get('avatar'),
                    createdAt=user.get('createdAt')
                ).dict(),
                "token": TokenResponse(
                    accessToken=token,
                    tokenType="bearer"
                ).dict()
            }
            
            return JSONResponse(
                status_code=201,
                content=response_data
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    async def logout(self) -> JSONResponse:
        """Handle user logout."""
        # For JWT tokens, logout is handled client-side by removing the token
        # Server-side logout would require token blacklisting (not implemented)
        return JSONResponse(
            status_code=200,
            content={"message": "Logged out successfully"}
        )

    async def get_profile(self, user_id: str) -> JSONResponse:
        """Get user profile."""
        try:
            user = self.auth_service.get_user_profile(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            response_data = ProfileResponse(
                id=user['id'],
                name=user['name'],
                email=user['email'],
                timezone=user['timezone'],
                role=user['role'],
                avatar=user.get('avatar'),
                createdAt=user.get('createdAt')
            )
            
            return JSONResponse(
                status_code=200,
                content=response_data.dict()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_profile(self, user_id: str, request: UpdateProfileRequest) -> JSONResponse:
        """Update user profile."""
        try:
            updates = request.dict(exclude_unset=True)
            user = self.auth_service.update_user_profile(user_id, updates)
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            response_data = ProfileResponse(
                id=user['id'],
                name=user['name'],
                email=user['email'],
                timezone=user['timezone'],
                role=user['role'],
                avatar=user.get('avatar'),
                createdAt=user.get('createdAt')
            )
            
            return JSONResponse(
                status_code=200,
                content=response_data.dict()
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def verify_token(self, token: str) -> JSONResponse:
        """Verify JWT token."""
        try:
            payload = self.auth_service.verify_token(token)
            return JSONResponse(
                status_code=200,
                content={"valid": True, "payload": payload}
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")
