"""Headless CLI runner. Same pipeline as the GUI, no wxPython."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from stickerforge.config.loader import ForgeConfig
from stickerforge.handlers.prompt_handler import PromptHandler
from stickerforge.models.job import ForgeJob
from stickerforge.services.exporter import export_pack
from stickerforge.services.pipeline import ForgePipeline

log = logging.getLogger("stickerforge.cli")


def run_cli(*, cfg: ForgeConfig, job_path: Path | None, preset: str) -> int:
    if job_path is None:
        log.error("no --job given; CLI mode requires a job file")
        return 2

    raw = json.loads(job_path.read_text(encoding="utf-8"))
    job = ForgeJob.model_validate(raw)
    log.info("job %s: %d prompt(s), pack=%s", job.job_id, len(job.prompts), job.pack_format)

    pipeline = ForgePipeline(cfg=cfg, preset_name=preset)
    handler = PromptHandler(pipeline=pipeline)

    results = []
    for prompt in job.prompts:
        results.append(handler.run(prompt=prompt, style=job.style))

    out_dir = cfg.runtime.output_dir / job.job_id
    pack_path = export_pack(results=results, out_dir=out_dir, pack_format=job.pack_format)
    log.info("packed %d sticker(s) -> %s", len(results), pack_path)
    return 0