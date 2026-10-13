"""Thin adapter over diffusers. Returns HxWx4 uint8 RGBA."""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

import numpy as np

from stickerforge.models.preset import Preset

log = logging.getLogger("stickerforge.services.diffusion")


@lru_cache(maxsize=2)
def _load_pipe(model_id: str, allow_download: bool) -> Any:
    from diffusers import AutoPipelineForText2Image
    import torch

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id,
        torch_dtype=dtype,
        local_files_only=not allow_download,
    )
    pipe.set_progress_bar_config(disable=True)
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    return pipe


def build_backend(preset: Preset, *, allow_download: bool):
    def _run(prompt: str, *, steps: int, guidance: float, seed: int) -> np.ndarray:
        import torch

        pipe = _load_pipe(preset.model_id, allow_download)
        gen = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(seed)
        img = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            generator=gen,
            height=preset.size,
            width=preset.size,
        ).images[0]
        rgba = np.asarray(img.convert("RGBA"), dtype=np.uint8)
        return rgba

    return _run