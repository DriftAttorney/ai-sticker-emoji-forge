"""Logging config. Writes to .stickerforge/logs/last_run.log."""
from __future__ import annotations

import logging
from pathlib import Path

LOG_DIR = Path(".stickerforge") / "logs"


def configure_logging(*, verbosity: int = 0) -> None:
    level = logging.WARNING if verbosity == 0 else logging.INFO if verbosity == 1 else logging.DEBUG
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "last_run.log", encoding="utf-8"),
    ]
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(