"""Photo -> sticker. Background removal + optional img2img stylization."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from PIL import Image

from stickerforge.core.matting import cutout
from stickerforge.core.outline import add_outline
from stickerforge.services.matting_service import build_matte_fn

log = logging.getLogger("stickerforge.handlers.photo")


class PhotoHandler:
    def __init__(self, *, output_dir: Path) -> None:
        self._output_dir = output_dir
        self._matte = build_matte_fn()

    def run(self, *, photo: Path, outline_px: int = 8) -> Path:
        img = np.asarray(Image.open(photo).convert("RGB"))
        rgba = cutout(img, self._matte, feather_px=2)
        rgba = add_outline(rgba, thickness=outline_px)
        out = self._output_dir / f"{photo.stem}_sticker.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(rgba, mode="RGBA").save(out)
        log.info("photo -> sticker: %s", out.name)
        return out