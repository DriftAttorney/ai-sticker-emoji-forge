"""Alpha-cutout stage. Wraps rembg, exposes a pure `cutout(rgba) -> rgba`."""
from __future__ import annotations

import logging
from typing import Callable

import numpy as np

log = logging.getLogger("stickerforge.core.matting")

MatteFn = Callable[[np.ndarray], np.ndarray]


def cutout(image: np.ndarray, matte_fn: MatteFn, *, feather_px: int = 2) -> np.ndarray:
    """Apply matte_fn to an RGB(A) array, return RGBA with feathered alpha."""
    if image.ndim != 3 or image.shape[2] not in (3, 4):
        raise ValueError(f"expected HxWx3 or HxWx4, got {image.shape}")
    rgb = image[:, :, :3]
    alpha = matte_fn(rgb).astype(np.uint8)
    if feather_px > 0:
        alpha = _feather(alpha, radius=feather_px)
    out = np.dstack([rgb, alpha])
    return out


def _feather(alpha: np.ndarray, *, radius: int) -> np.ndarray:
    from scipy.ndimage import gaussian_filter

    return gaussian_filter(alpha.astype(np.float32), sigma=radius).clip(0, 255).astype(np.uint8)