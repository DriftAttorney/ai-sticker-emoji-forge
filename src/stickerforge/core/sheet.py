"""Emoji sheet layout — pack N stickers into a Twemoji-style grid PNG."""
from __future__ import annotations

import numpy as np


def layout_grid(tiles: list[np.ndarray], *, cols: int = 4, pad: int = 8, bg: tuple[int, int, int, int] = (0, 0, 0, 0)) -> np.ndarray:
    """Tile RGBA stickers into one sheet. All tiles must be the same size."""
    if not tiles:
        raise ValueError("no tiles to lay out")
    h, w = tiles[0].shape[:2]
    for t in tiles:
        if t.shape[:2] != (h, w):
            raise ValueError("tiles must share dimensions")

    rows = (len(tiles) + cols - 1) // cols
    cell = h + pad
    sheet = np.zeros((rows * cell + pad, cols * cell + pad, 4), dtype=np.uint8)
    sheet[:, :] = bg

    for idx, tile in enumerate(tiles):
        r, c = divmod(idx, cols)
        y = pad + r * cell
        x = pad + c * cell
        sheet[y : y + h, x : x + w] = tile
    return sheet