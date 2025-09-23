"""
Error utilities.

Custom exception classes and FastAPI error response helpers.
"""

from __future__ import annotations

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ValidationError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


def handle_validation_error(exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc) or "Validation error"})


def handle_unauthorized_error(exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc) or "Unauthorized"})

