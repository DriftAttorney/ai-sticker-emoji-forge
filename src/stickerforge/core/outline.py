"""Sticker outline pass — thick white border, the thing that makes it read as a sticker."""
from __future__ import annotations

import numpy as np


def add_outline(rgba: np.ndarray, *, thickness: int = 8, color: tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    """Dilate the alpha mask and composite a colored ring behind the subject."""
    if thickness <= 0:
        return rgba
    alpha = rgba[:, :, 3]
    mask = alpha > 16
    grown = _dilate(mask, radius=thickness)
    ring = grown & ~mask

    out = rgba.copy()
    out[ring, 0] = color[0]
    out[ring, 1] = color[1]
    out[ring, 2] = color[2]
    out[ring, 3] = 255
    return out


def _dilate(mask: np.ndarray, *, radius: int) -> np.ndarray:
    from scipy.ndimage import binary_dilation

    struct = np.ones((radius * 2 + 1, radius * 2 + 1), dtype=bool)
    return binary_dilation(mask, structure=struct)