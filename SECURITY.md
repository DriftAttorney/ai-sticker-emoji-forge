# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Threat model

ai-sticker-emoji-forge runs entirely on the local machine. It does **not**
upload user photos, prompts, or generated packs to any remote service by
default. The only outbound network calls are:

1. Model weight downloads from Hugging Face (opt-in, gated behind
   `--allow-download` or the Settings toggle).
2. Optional telemetry ping — disabled unless `STICKERFORGE_TELEMETRY=1`.

## What we consider a vulnerability

- Arbitrary code execution via a malicious `.sfpack` file (these are zip
  archives; see `services/packer.py`).
- Path traversal in pack import (`utils/fs.py::safe_join`).
- Pickle deserialization — we do **not** ship pickles; report any `.pkl`
  or `.pt` load path that bypasses `safetensors`.
- Prompt-injection leading to filesystem writes outside the job dir.

## What we do not consider a vulnerability

- NSFW output from a user-supplied prompt. The forge is a tool; the user
  is responsible for what they generate and export.
- Sticker packs that violate a platform's ToS. That's a policy issue,
  not a security issue.

## Reporting

Email `security@ai-sticker-emoji-forge.dev` with a PoC and the exact
commit hash. We aim to respond within 72h. Please do not open a public
issue for memory-safety or RCE bugs.