"""PackManifest — what lives inside every .sfpack."""
from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class PackManifest(BaseModel):
    name: str
    format: str
    count: int
    entries: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    forge_version: str = "0.4.2"