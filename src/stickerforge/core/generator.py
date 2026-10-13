"""Prompt -> latent -> image. Pure functions over a diffusion callable."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

import numpy as np


class DiffusionBackend(Protocol):
    def __call__(self, prompt: str, *, steps: int, guidance: float, seed: int) -> np.ndarray: ...


@dataclass(frozen=True, slots=True)
class GenSpec:
    prompt: str
    negative_prompt: str = "blurry, lowres, extra fingers, watermark"
    steps: int = 8
    guidance: float = 1.5
    seed: int = -1
    size: int = 512


def generate(spec: GenSpec, backend: DiffusionBackend) -> np.ndarray:
    """Run one diffusion pass. Returns HxWx4 uint8 RGBA."""
    seed = spec.seed if spec.seed >= 0 else int(np.random.default_rng().integers(0, 2**31 - 1))
    img = backend(spec.prompt, steps=spec.steps, guidance=spec.guidance, seed=seed)
    if img.shape[:2] != (spec.size, spec.size):
        raise ValueError(f"backend returned {img.shape[:2]}, expected {(spec.size, spec.size)}")
    return img