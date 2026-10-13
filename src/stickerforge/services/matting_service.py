"""rembg wrapper. CPU ONNX by default; u2net_human_seg for portraits."""
from __future__ import annotations

import logging
from functools import lru_cache

import numpy as np

log = logging.getLogger("stickerforge.services.matting")


@lru_cache(maxsize=1)
def _session(model_name: str):
    from rembg import new_session

    return new_session(model_name)


def build_matte_fn(model_name: str = "u2net"):
    from rembg import remove

    def _matte(rgb: np.ndarray) -> np.ndarray:
        rgba = remove(rgb, session=_session(model_name), only_mask=True)
        return np.asarray(rgba, dtype=np.uint8)

    return _matte