# 12 · `motion.frames`

Stills at chosen times or at the piece's key moments, or one contact sheet. Sync, cost 2, max 2 concurrent, 120 s,
cgroup 4 CPU / 2 GiB, $0.002 per cell, daily quota 2,000 cells (`REXX_QUOTA_FRAMES`), rate class `frames`.
Source: `service/src/tools/frames.rs`, `engine/crates/rexx-engine/src/frames.rs`, 06 §6.4.

## Input

| Field | Type | Default | Meaning |
|---|---|---|---|
| `doc` / `doc_url` | | — | Exactly one. |
| `variant` | string | `"default"` | The variant to render. |
| `times` | list, ≤ 24 entries | — | Moments to render. A **number** is seconds (negative → `400` "times[i]: -1 is negative"). A **string** is passed to the engine as written and must contain no space or comma: `"12f"` (frames at the comp's rate), `"@beat4"` (a marker; `"@beat4+0.5"` with an offset; `"@beat*"` matches the first marker with that prefix), `"50%"` (of the duration), `"end"`, `"end-0.5"` (from the last frame), `"1.5s"`, `"00:00:01:12"` (timecode). Exclusive with `auto`. A time outside `[0, duration]` is the diagnostic `doc.type` at `/times` (a `400` with `error.data.diagnostics`); an unknown marker `ref.marker`. A time at the exact end is clamped to the last frame. |
| `auto` | integer 1–24 | — | N frames at the key moments: the first frame, every layer's `in`, its arrival (0.6 s or half its span later), its last visible frame, every marker, the last frame; the candidates are spread evenly in time order, padded with evenly spaced frames when there are fewer than N. Exclusive with `times`; one of the two is required ("give times (a list of moments) or auto (a number of key moments)"; both: "use either times or auto, not both"). |
| `sheet` | boolean | `false` | One contact-sheet PNG (`sheet.png`) instead of one PNG per time: a grid, as square as the count allows, at most 6 columns × 4 rows, dark background, each cell labelled with its time (`1.50s`). |
| `width` | integer 64–3840 | single stills: `min(comp width, 960)`; sheet: 1920 | Width in px. For single stills the still's width, the height follows the aspect. For a sheet the **whole sheet's** width; each cell is `width / columns` (at least 16 px). |
| `safe_overlay` | enum | none | Draw the platform's UI safe zone as a 2 px magenta rectangle: `tiktok`, `reels`, `shorts`, `youtube`, `linkedin`, `x`, `broadcast` (the engine also accepts `story`, `square`, `none`; a portrait-only preset on a landscape comp draws the broadcast zone). The zone is spec 3 §3.5's safe-area table, the same one `lint.platform` uses. |
| `transparent` | boolean | `false` | Keep alpha (every comp's `background` is dropped) instead of compositing over the comp background. |
| `depth` | `8` \| `16` | 8 | 8: display-referred sRGB PNG, dithered, deflated at the fast level (same pixels as a render's frame, different bytes). 16: scene-linear, un-premultiplied 16-bit PNG (the golden-frame form, for pixel comparison). Anything else: `400` "depth must be 8 or 16". |
| `motion_blur` | boolean | `true` | `false` passes `--no-motion-blur`: every comp's motion blur is switched off for the stills. (The published schema prints `default: false` for this field; the behaviour is `true`.) |
| `trails` | boolean | `false` | Onion skin: each still also draws the frame at −2, −1, +1 and +2 frames as ghosts at 22 % opacity (frames outside the comp are skipped), so motion shows in a still. About four extra frame evaluations per still. |
| `seeds` | list of integers, ≤ 6 (`REXX_MAX_SEEDS`) | — | Physics variations: the document is normalized once per seed with every comp's `physics.seed` set to it; needs `sheet: true` ("seeds needs sheet: true (one row of takes per seed)"); the sheet gets one **row per seed** (labelled `#<seed>` in its first cell) and one column per time. The cell count is `times × seeds`. When the document's `physics.vary` is all zero (or absent) the exploration vary `{ "velocity": 60, "spin": 45, "rotation": 4, "position": 0 }` is used and reported in `data.vary`. Each variation's bake lands in the box's sim cache, so rendering the chosen seed afterwards does not simulate again. A document without physics gets the info `physics.seed_no_effect` at `/seeds`. |
| `data` | object | — | Merged over the document's `data`. |

Cells = `times` (or `auto`) × `max(1, seeds)` and must be ≤ `REXX_MAX_STILLS` (24): `413` "N frames requested; the
limit is 24 per call". The engine's own cap is 64 (`limit.frames`).

## What runs

`rexx-engine frames --doc … --assets … [--variant v] --times a,b,c | --auto N [--sheet] [--width W]
[--safe-overlay p] [--transparent] [--depth 16] [--no-motion-blur] [--trails] [--seeds 1,2,3 --sims] [--data …]
[--png-fast] --out frames/ --deadline <remaining s>`. Every asset is materialized (unlike `check`). Guide layers
(`guide: true`) render in stills, never in `motion.render` outputs. Stills are encoded on up to four threads while
the next frames render. The backend (CPU or GPU) is the engine's `auto` decision unless `REXX_ENGINE_BACKEND` pins it.

## Output

`files`: a list of URLs, `frame-00.png`, `frame-01.png`, … in `times` order (row-major over seeds), or `sheet.png`.

```jsonc
{ "frames": [ { "t": 0.5, "cell": 0 }, { "t": "@beat4", "cell": 1 }, { "t": 2.0, "cell": 2, "seed": 7 } ],
  "width": 960, "height": 540,
  "diagnostics": [ { "severity": "warning", "code": "font.fallback_used", "…": "…" } ],
  "ms": 640,
  "vary": { "velocity": 60, "spin": 45, "rotation": 4, "position": 0 },   // only when the exploration vary was used
  "billing": { "price": { "amount": 0.006, "currency": "USD" } } }
```

| Field | Meaning |
|---|---|
| `frames[].t` | the time as the caller gave it (a number stays a number; a string stays a string; `auto` times are seconds); `frames[].cell` the index (file index, or sheet cell row-major); `frames[].seed` with `seeds`. |
| `width`, `height` | the sheet's size with `sheet: true`, else each still's. |
| `diagnostics[]` | warnings and infos only (normalization's, filtered by `lint.disable`, plus the renderer's per-frame warnings deduplicated by code and path: `font.*`, `media.*`, `render.*`, `effect.*`). |
| `ms` | wall time of the whole call. |

## Errors

| Status | When |
|---|---|
| 400 `bad_request` | the document has errors (the first three in the message, all in `error.data.diagnostics`; nothing rendered, nothing charged); both or neither of `times`/`auto`; a negative or malformed time; `seeds` without `sheet`; `depth` not 8 or 16; a time outside the comp or an unknown marker (engine diagnostics); an asset that cannot be used |
| 413 `too_large` | over 24 cells; over 6 seeds; document or asset caps |
| 500 `internal` | "rendering produced no frames", engine exit 5, a stalled run |

A render error at a frame (`expr.runtime`, `render.deadline`, `limit.memory`, `media.*` errors) fails the whole call
with the diagnostic (exit 2/3/4 → `400`).

## Examples

```json
{ "doc_url": "library:mitte/demo/title-card@1", "auto": 10, "sheet": true, "trails": true }
```
A review sheet: ten key moments with motion ghosts.

```json
{ "doc_url": "library:mitte/demo/title-card@1", "variant": "vertical", "times": ["@beat2", "50%"], "safe_overlay": "reels" }
```
Two stills of the vertical variant with the Reels zone drawn.

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "times": [1.8], "transparent": true, "depth": 16, "width": 1920 }
```
One linear 16-bit transparent still at full width.

```json
{ "doc_url": "library:mitte/demo/showreel@1", "times": [6, 7, 8], "sheet": true, "seeds": [1, 2, 3, 4], "width": 1440 }
```
Twelve cells: four physics takes of three moments, one row per seed ($0.024).

Since engine 0.1.59 (K-30) a call for the same document, times, width and quality flags is served from the result
store (`data.cache_hit: true`, the first call's cells, size, diagnostics and `vary`; billed as rendered; 30 days
from last use).

Registry examples: `review-sheet`, `entrance`, `safe-zone`, `3d-sheet`, `transparent-still`, `data-story-moments`
([92-schema-frames.md](92-schema-frames.md)).

