from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field, RootModel


ID = str


class AvailabilityMap(RootModel[Dict[str, bool]]):
    # Map like { "day_0_slot_13": true }
    root: Dict[str, bool] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    ok: bool = True
    message: Optional[str] = None


