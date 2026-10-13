"""Preset — diffusion model + step/size/outline knobs."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Preset(BaseModel):
    name: str
    model_id: str = Field(description="Hugging Face repo id, e.g. stabilityai/sdxl-turbo")
    steps: int = Field(ge=1, le=50, default=8)
    guidance: float = Field(ge=0.0, le=20.0, default=1.5)
    size: int = Field(default=512, description="square output, px")
    outline_px: int = Field(ge=0, le=32, default=8)