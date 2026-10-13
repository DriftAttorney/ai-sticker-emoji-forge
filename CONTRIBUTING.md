# Contributing to ai-sticker-emoji-forge

Thanks for wanting to forge stickers. This repo is a Windows desktop toolkit
that turns prompts, photos, or reference art into sticker packs (Telegram,
WhatsApp, Discord) and emoji grids (Slack, Twemoji-style sheets).

## Dev setup

```
git clone https://github.com/potato-forge/ai-sticker-emoji-forge
cd ai-sticker-emoji-forge
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

CPU-only install is fine for the pipeline tests. Diffusion inference needs a
GPU with >=6GB VRAM for SDXL-Turbo sticker presets; SD1.5 presets run on
4GB. The `rembg` matting stage runs on CPU via onnxruntime.

## Layout

- `src/stickerforge/app/` — bootstrap + CLI + wxPython shell
- `src/stickerforge/core/` — pure pipeline logic (no UI, no I/O side effects)
- `src/stickerforge/handlers/` — one handler per input source (prompt, photo, ref)
- `src/stickerforge/services/` — diffusion, matting, packing, export
- `src/stickerforge/models/` — pydantic schemas for jobs, packs, presets
- `src/stickerforge/utils/` — filesystem, image, telemetry helpers
- `src/stickerforge/config/` — YAML presets and loader
- `native/` — optional C++/C# accelerators (tiling, sheet layout)
- `tests/` — pytest, no GPU required

## Style

- Ruff + Black, line length 100.
- Mypy strict on `core/` and `models/`.
- No `print()` in `core/` or `services/` — use `logging`.

## PR checklist

- [ ] `pytest -q` passes locally
- [ ] `ruff check src tests` clean
- [ ] new presets added under `src/stickerforge/config/presets/`
- [ ] CHANGELOG entry under `[Unreleased]`

## Reporting bugs

Open an issue with: OS build, Python version, GPU + driver, preset name,
and the contents of `.stickerforge/logs/last_run.log`.