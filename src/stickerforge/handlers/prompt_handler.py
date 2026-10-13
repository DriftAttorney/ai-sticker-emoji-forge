"""Text-prompt -> sticker. The default path."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from stickerforge.core.generator import GenSpec
from stickerforge.services.pipeline import ForgePipeline

log = logging.getLogger("stickerforge.handlers.prompt")


@dataclass(slots=True)
class StickerResult:
    path: Path
    prompt: str
    style: str
    seed: int


class PromptHandler:
    def __init__(self, *, pipeline: ForgePipeline) -> None:
        self._pipeline = pipeline

    def run(self, *, prompt: str, style: str = "sticker") -> StickerResult:
        spec = GenSpec(prompt=_style_prefix(style) + prompt)
        rgba, seed = self._pipeline.forge(spec)
        path = self._pipeline.save(rgba, tag=style)
        log.info("forged %s (seed=%d)", path.name, seed)
        return StickerResult(path=path, prompt=prompt, style=style, seed=seed)


def _style_prefix(style: str) -> str:
    return {
        "sticker": "die-cut sticker, thick white outline, ",
        "emoji": "twemoji-style flat emoji, ",
        "kawaii": "kawaii chibi, big eyes, ",
        "pixel": "16-bit pixel art, ",
        "flat": "flat vector illustration, ",
    }.get(style, "")