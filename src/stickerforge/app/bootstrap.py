"""Entry point. Wires config -> services -> handlers -> UI or CLI."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from stickerforge.app.cli import run_cli
from stickerforge.app.shell import launch_shell
from stickerforge.config.loader import load_config
from stickerforge.utils.logging import configure_logging


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="sticker-forge", description="AI sticker / emoji generator")
    p.add_argument("--config", type=Path, default=None, help="path to forge.yaml")
    p.add_argument("--job", type=Path, default=None, help="run a job file and exit (headless)")
    p.add_argument("--preset", default="sticker_sdxl_turbo", help="preset name from config/presets")
    p.add_argument("--allow-download", action="store_true", help="permit HF weight downloads")
    p.add_argument("--no-gui", action="store_true", help="force CLI mode")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    configure_logging(verbosity=args.verbose)
    log = logging.getLogger("stickerforge.bootstrap")

    cfg = load_config(args.config)
    cfg.runtime.allow_download = cfg.runtime.allow_download or args.allow_download

    log.info("forge %s starting (preset=%s)", __import__("stickerforge").__version__, args.preset)

    if args.job is not None or args.no_gui:
        return run_cli(cfg=cfg, job_path=args.job, preset=args.preset)

    try:
        return launch_shell(cfg=cfg, preset=args.preset)
    except Exception as exc:  # wxPython missing on headless CI
        log.warning("GUI unavailable (%s); falling back to CLI", exc)
        return run_cli(cfg=cfg, job_path=args.job, preset=args.preset)


if __name__ == "__main__":
    sys.exit(main())