"""Pack stickers into a .sfpack (zip) for import/export. Path-traversal safe."""
from __future__ import annotations

import json
import logging
import zipfile
from pathlib import Path

from stickerforge.models.pack import PackManifest
from stickerforge.utils.fs import safe_join

log = logging.getLogger("stickerforge.services.packer")

MANIFEST_NAME = "manifest.json"


def write_pack(*, stickers: list[Path], out_path: Path, manifest: PackManifest) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MANIFEST_NAME, manifest.model_dump_json(indent=2))
        for s in stickers:
            zf.write(s, arcname=f"stickers/{s.name}")
    log.info("wrote pack %s (%d stickers)", out_path.name, len(stickers))
    return out_path


def read_pack(pack: Path, *, extract_to: Path) -> PackManifest:
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(pack, "r") as zf:
        manifest = PackManifest.model_validate(json.loads(zf.read(MANIFEST_NAME)))
        for name in zf.namelist():
            if name == MANIFEST_NAME:
                continue
            target = safe_join(extract_to, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))
    return manifest