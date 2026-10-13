"""Filesystem helpers. safe_join is the security-critical one."""
from __future__ import annotations

from pathlib import Path


def safe_join(root: Path, untrusted: str) -> Path:
    """Join untrusted relative path under root, rejecting traversal."""
    root = root.resolve()
    candidate = (root / untrusted).resolve()
    if root != candidate and root not in candidate.parents:
        raise ValueError(f"path traversal blocked: {untrusted!r}")
    return candidate


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path