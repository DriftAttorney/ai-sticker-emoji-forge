"""Reference-art handler — palette + pose extraction for style transfer seeds."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from PIL import Image

log = logging.getLogger("stickerforge.handlers.reference")


class ReferenceHandler:
    def __init__(self, *, k_colors: int = 6) -> None:
        self._k = k_colors

    def extract_palette(self, ref: Path) -> list[tuple[int, int, int]]:
        img = Image.open(ref).convert("RGB").resize((128, 128))
        arr = np.asarray(img).reshape(-1, 3).astype(np.float32)
        centers = _kmeans(arr, k=self._k, iters=12)
        return [tuple(int(c) for c in row) for row in centers]


def _kmeans(x: np.ndarray, *, k: int, iters: int) -> np.ndarray:
    rng = np.random.default_rng(0)
    centers = x[rng.choice(len(x), size=k, replace=False)]
    for _ in range(iters):
        d = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(-1)
        labels = d.argmin(1)
        for i in range(k):
            if (labels == i).any():
                centers[i] = x[labels == i].mean(0)
    return centers