"""ForgePipeline — the one object the UI and CLI both talk to."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

from stickerforge.config.loader import ForgeConfig
from stickerforge.core.generator import GenSpec, generate
from stickerforge.core.outline import add_outline
from stickerforge.services.diffusion_service import build_backend

log = logging.getLogger("stickerforge.services.pipeline")


class ForgePipeline:
    def __init__(self, *, cfg: ForgeConfig, preset_name: str) -> None:
        self._cfg = cfg
        self._preset = cfg.presets[preset_name]
        self._backend = build_backend(self._preset, allow_download=cfg.runtime.allow_download)

    def forge(self, spec: GenSpec) -> tuple[np.ndarray, int]:
        seed = spec.seed if spec.seed >= 0 else int(np.random.default_rng().integers(0, 2**31 - 1))
        spec = GenSpec(**{**spec.__dict__, "seed": seed, "steps": self._preset.steps, "size": self._preset.size})
        rgba = generate(spec, self._backend)
        rgba = add_outline(rgba, thickness=self._preset.outline_px)
        return rgba, seed

    def save(self, rgba: np.ndarray, *, tag: str) -> Path:
        out_dir = self._cfg.runtime.output_dir / datetime.now(timezone.utc).strftime("%Y%m%d")
        out_dir.mkdir(parents=True, exist_ok=True)
        name = f"{tag}_{datetime.now(timezone.utc).strftime('%H%M%S_%f')}.png"
        path = out_dir / name
        Image.fromarray(rgba, mode="RGBA").save(path)
        return path