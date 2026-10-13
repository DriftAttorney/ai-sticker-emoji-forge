"""Export forged stickers to platform-specific pack formats."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

from stickerforge.handlers.prompt_handler import StickerResult
from stickerforge.models.pack import PackManifest
from stickerforge.services.packer import write_pack

log = logging.getLogger("stickerforge.services.exporter")

PLATFORM_SIZES = {
    "telegram": 512,
    "whatsapp": 512,
    "discord": 320,
    "slack": 128,
}


def export_pack(*, results: list[StickerResult], out_dir: Path, pack_format: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stickers = [r.path for r in results]
    manifest = PackManifest(
        name=out_dir.name,
        format=pack_format,
        count=len(stickers),
        entries=[s.name for s in stickers],
    )
    pack_path = out_dir / f"{out_dir.name}.sfpack"
    write_pack(stickers=stickers, out_path=pack_path, manifest=manifest)

    if pack_format in PLATFORM_SIZES:
        plat_dir = out_dir / pack_format
        plat_dir.mkdir(exist_ok=True)
        for s in stickers:
            shutil.copy2(s, plat_dir / s.name)
    return pack_path