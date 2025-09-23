"""
Blueprint routes for availability aggregation endpoints.

Provides /api/v1/teams/<id>/availability/heatmap that aggregates availability
into time buckets, with optional tz conversion.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/aggregation", tags=["Aggregation"])
