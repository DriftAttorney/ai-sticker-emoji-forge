"""ForgeJob — the unit of work the CLI consumes."""
from __future__ import annotations

from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class ForgeJob(BaseModel):
    job_id: str = Field(default_factory=lambda: uuid4().hex[:12])
    prompts: list[str] = Field(min_length=1)
    style: Literal["sticker", "emoji", "kawaii", "pixel", "flat"] = "sticker"
    pack_format: Literal["sfpack", "telegram", "whatsapp", "discord", "slack"] = "sfpack"
    seed: int = -1