# 13 · `motion.render`

A document to video or image files, in one or several variants, through the render cache. A **job**
(`POST /v1/jobs`; `/v1/run` only when the scaled estimate fits the 240 s sync budget), cost 4, max 2 concurrent per
box, 20-minute cap, cgroup 4 CPU / 6 GiB, output asset type `video`, rate class `render`, daily quota 60 rendered
minutes (`REXX_QUOTA_RENDER_MINUTES`). Source: `service/src/tools/render.rs`,
`engine/crates/rexx-engine/src/render.rs`, `rexx-encode/src/settings.rs`, spec 13 §13.5, 06 §6.5. The cache,
backends, chunking, HDR and NVENC are in [16-render-pipeline.md](16-render-pipeline.md).

## Input

| Field | Type | Default | Meaning |
|---|---|---|---|
| `doc` / `doc_url` | | — | Exactly one. |
| `variants` | list of ids, ≤ 6 (`REXX_MAX_VARIANTS`) | `["default"]` | Every variant rendered in one job, each its own labelled file; ids are trimmed and deduplicated; an empty id is `400`; both `variants` and `variant`: `400` "use either variants or variant, not both". |
| `variant` | id | — | One variant (the alternative to `variants`). |
| `output` | object | — | Overrides the document's `output` block **field by field** (table below). |
| `poster` | `true` \| number ≥ 0 | absent | Also return a PNG per variant (label `<variant>-poster`, file `<variant>-poster.png`): `true` picks the frame at the latest layer `in` plus its arrival (0.6 s or a tenth of the piece), clamped into the comp; a number is that time in seconds (clamped). `false`/`null` is absent; a negative number "poster time must not be negative"; anything else "poster must be true or a time in seconds". Posters are always SDR 8-bit PNGs, opaque. |
| `data` | object | — | Merged over the document's `data`. |

### `output` overrides

Only these fields can be overridden per call; every other output setting (`profile`, `crf`, `bitrate`, `preset`,
`size`, `pixelFormat`, `toneMap`, `gamutMap`, `dither`, `transferTag`, `signalRange`, `hdrPeak`, `audio.*`,
`allowSolo`, `locale`, `faststart`, `gif.*`, `loop`) is read from the document's `output` block by the engine.

| Field | Values | Default | Notes |
|---|---|---|---|
| `format` | `mp4`, `mov`, `webm`, `gif`, `webp`, `png`, `png-seq`, `tiff-seq`, `exr-seq`, `jpg`, `avif` (the published enum is what this box's engine reports with `version --outputs`) | the document's `output.format`, else `mp4` | `png`, `jpg`, `avif` are single stills (the frame at `poster`'s time, else the range start); `png-seq`, `tiff-seq`, `exr-seq` are zips of per-frame files. A name outside the table: `400` "unknown output format …"; a format the box's ffmpeg cannot write: `output.format_unavailable`. |
| `codec` | `h264`, `hevc`, `av1`, `prores`, `vp9` | by format: `mp4` → `h264`, `mov` → `prores`, `webm` → `vp9`; with `hdr`: `hevc` in `mp4`/`mov`, `av1` in `webm` | By container: `mp4`: h264, hevc, av1; `mov`: prores, h264, hevc; `webm`: vp9, av1; image formats take none. The document's `codec` is inherited only when `format` is **not** overridden (an override to another container takes that container's default). A mismatch is `output.codec_container` at `/output/codec` (or `/doc/output/codec`). |
| `quality` | `draft`, `standard`, `high`, `master` | `standard` | The encoder preset rows of spec 13 §13.5.1. `draft` renders at `scale` 0.5 unless `scale` or `size` is set. |
| `alpha` | `true`, `false`, `"stacked"` | the document's, else `false` | `true` keeps transparency: `mov`+`prores` (4444), `mov`+`hevc` (8-bit `yuva420p`, two-layer), `webm`+`vp9`, `png`, `png-seq`, `webp`, `gif` (1-bit), `avif`, `tiff-seq`, `exr-seq`. `"stacked"`: colour on top, alpha as luma below, in an opaque video of twice the height: `mp4`/`mov` + `h264`/`hevc`, `webm`+`vp9`. With alpha the comp background is ignored. Otherwise `output.alpha_unsupported` with a hint listing the rows that carry the mode. The strings `"true"`/`"false"` are accepted as the booleans. |
| `fps` | number > 0 | the comp's | Render at another rate: every output frame is sampled at its own exact time (not a frame-rate conversion); footage keeps its own frames. ≤ `REXX_MAX_FPS` (60); the engine's own ceiling is 240. A GIF ignores it (`gif.fps`). |
| `scale` | 0.25–2 | 1 (0.5 for `draft`) | Output size = comp size × scale, rounded; video sizes are forced even. Outside the range: the engine's `output.value` at `/output/scale`. |
| `range` | `[in, out]` seconds | the whole comp | `out > in ≥ 0` ("output.range must be [in, out] seconds with out > in >= 0"); `out` is clamped to the comp's duration; a range starting past the comp: `400` "output.range starts at Ns, past the "v" comp's Ms". The rendered span, frames and estimate follow the range. The engine also accepts marker and frame forms here, but the tool takes numbers only. |
| `audio` | boolean | `true` | `false` passes `--no-audio` (no mixdown, no audio track). |
| `hdr` | `hlg`, `pq` | the document's `output.hdr`, else SDR | 10-bit Rec.2020 HDR: `hevc` (mp4, mov) or `av1` (mp4, webm); no alpha; `pq` adds mastering-display and measured MaxCLL/MaxFALL metadata and takes `output.hdrPeak` (100–10,000 cd/m², default 1,000) from the document. Refused with `output.hdr_unsupported` for other formats, codecs, alpha, profile `main` or an 8-bit `pixelFormat`. |
| `encoder` | `cpu`, `nvenc` | the document's `output.encoder`, else `cpu` | `nvenc` uses the GPU encoder for `h264`, `hevc`, `av1` (presets p1–p7 by quality) on a box whose probe lists the codec (`/healthz` `nvenc`); refused with `output.encoder_unsupported` for prores, vp9, `alpha: true`, `hdr: "pq"`, 4:2:2, 4:4:4 AV1, image and sequence formats, frames under 160 × 90, and on a box without it. Never a fallback. |

Resolution order for `format`, `codec`, `alpha`, `hdr`, `encoder`: the override, else the document's `output`, else
the default; the refusal's `path` names which (`/output/<field>` or `/doc/output/<field>`). These checks run before
admission, so a refused output costs nothing.

## What runs

1. `variants` resolved; `poster` and `output` parsed; the document fetched; the output selection refused early.
2. Every asset materialized (https fetched, `library:` probed in place).
3. **One `check` per variant**: the estimate gates admission, `stats` sizes the limits, `doc_hash` keys the cache.
   An invalid document fails here with its diagnostics (`400`, nothing rendered, nothing charged).
4. Limits per variant after the overrides: duration ≤ `REXX_MAX_DURATION` (600 s), fps ≤ 60, width × height ≤
   3840 × 2160 (`REXX_MAX_PIXELS`); frames over all variants ≤ `REXX_MAX_FRAMES` (86,400). Each is `413`.
5. Admission: the summed estimates, scaled to the thread share, against the sync budget or the job cap
   ([00-overview.md](00-overview.md)). The render-minutes quota is charged now (rendered seconds rounded up to minutes).
6. Per variant: cache lookup (one HEAD, 500 ms bound) → a hit copies the stored file (and poster) into the caller's
   prefix; else `rexx-engine render --doc … --assets … --out render/<variant><ext> [--variant v] [--range a,b]
   --format f [--codec c] [--quality q] [--alpha | --alpha stacked] [--fps n] [--scale s] [--no-audio] [--hdr h]
   [--encoder e] [--poster [t]] [--data …] --deadline <remaining> --threads <share>`, chunked across workers when
   configured and the variant is at least `REXX_CHUNK_FROM` long.
7. Progress: `frames_done / frames_total` over all variants, visible on `GET /v1/jobs/{id}`.

## Output

`files`: `{ "<variant>": url, "<variant>-poster": url, … }` (a label map). Extensions: `.mp4`, `.mov`, `.webm`,
`.gif`, `.webp`, `.png`, `.jpg`, `.avif`, and `.zip` for `png-seq`, `tiff-seq`, `exr-seq`.

```jsonc
{
  "variants": {
    "default": { "duration_s": 15, "frames": 450, "fps": 30, "width": 1920, "height": 1080, "bytes": 6123456,
                 "codec": "h264", "ms_per_frame": 21.7, "wall_ms": 10100, "cache_hit": false,
                 "backend": "cpu", "encoder": "cpu", "warnings": [] },
    "vertical": { "…": "…" }
  },
  "doc_hash": "sha256:…",
  "engine": { "version": "0.1.48", "library": "2026.10.0", "fonts": "06acc477…" },
  "input_bytes": 31457280,
  "duration_s": 30,
  "billing": { "price": { "amount": 0.228, "currency": "USD" } }
}
```

| Field | Meaning |
|---|---|
| `variants.<id>.duration_s` | the rendered span (the range's when given). |
| `frames`, `fps` | the output frame count and rate (after `fps`/`range`, from the engine's stats when it rendered). |
| `width`, `height` | the frame size after `scale` (from the engine's stats); with `alpha: "stacked"` the frame size, the file is twice the height. |
| `bytes` | the file's size (0 on a cache hit). |
| `codec` | the codec as the engine reports it (empty on a cache hit or for an image format). |
| `ms_per_frame` | the engine's mean render cost per frame (0 on a cache hit). |
| `wall_ms` | the variant's wall time, cache copy included. |
| `cache_hit` | the variant came from the render cache. |
| `backend` | `cpu` or `gpu`: what rendered it (on a hit: what the entry was keyed with). |
| `encoder` | `cpu` or `nvenc`: what encoded it (likewise). |
| `warnings[]` | the check's warnings and infos plus the renderer's (`font.*`, `media.*`, `render.*`, `effect.*`, …), deduplicated by code and path. |
| `doc_hash` | `sha256:<hex>` of the authored document bytes as received. |
| `input_bytes` | every materialized asset's bytes (the billed MB). |
| `duration_s` | the sum over variants (what billing and the quota use). |

Container metadata written by the engine: colour tags, `rexx_version`, `motion_doc_sha256` (the canonical hash),
`comment` = `meta.title`, `rexx_backend=gpu` on a GPU render, `rexx_encoder=nvenc` on an NVENC encode,
`rexx_alpha=stacked` for stacked alpha.

## Errors

| Status | When |
|---|---|
| 400 `bad_request` | the document has errors (first three in the message, all in `error.data.diagnostics` on the run path); neither/both of `doc`/`doc_url`; `variants` and `variant` together, an empty id; an unknown `format`; a bad `poster` or `range`; a refused output: `output.format_unavailable`, `output.codec_container`, `output.alpha_unsupported`, `output.hdr_unsupported`, `output.encoder_unsupported` (as diagnostics at `/output/<field>` or `/doc/output/<field>`); the engine's own output refusals (`output.size_aspect`, `output.size_odd`, `output.pixel_format`, `output.value`, `output.audio_invalid`); a render failure at a frame (`expr.runtime`, `media.decode_failed`, `encode.ffmpeg`, …); an asset that cannot be used |
| 413 `too_large` | > 6 variants; a variant over 600 s, 60 fps or 3840 × 2160; > 86,400 frames over all variants; the estimate over the sync budget ("submit via POST /v1/jobs") or the job cap; document or asset caps |
| 429 | render-minutes quota (`overloaded`), the `render` class per minute (`rate_limited`) |
| 500 `internal` | "rendering produced no file", engine exit 5, a stall (no progress for 60 s) |
| 502 `upstream_failure` | a chunk peer or the object store failed |
| 503 `overloaded` | budget/slots, queue full, no engine on the box |
| 504 `timeout` | the job outlived its 20-minute deadline (the engine stops itself first: `render.deadline` / `encode.timeout` as a `400`) |

## Examples

```json
{ "doc_url": "library:mitte/demo/title-card@1", "variants": ["default", "vertical", "square"] }
```
Three MP4s (H.264, standard) in one job: labels `default`, `vertical`, `square`.

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "output": { "format": "mov", "codec": "prores", "alpha": true, "quality": "high" } }
```
ProRes 4444 with alpha for an editor.

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "output": { "format": "mp4", "codec": "h264", "alpha": "stacked" } }
```
Stacked alpha for players without alpha support (file twice the height).

```json
{ "doc_url": "library:mitte/demo/title-card@1", "output": { "quality": "draft", "scale": 0.5, "fps": 15, "range": [0, 2] }, "poster": 1.2 }
```
A fast two-second draft at half size plus a poster at 1.2 s.

```json
{ "doc_url": "library:mitte/demo/glow@1", "output": { "format": "mp4", "hdr": "hlg" } }
```
HDR for Instagram: 10-bit HEVC HLG (the codec defaults to `hevc` with `hdr`).

```json
{ "doc_url": "library:mitte/demo/title-card@1", "output": { "format": "png-seq", "alpha": true } }
```
A zip of transparent PNG frames.

```json
{ "doc_url": "library:mitte/demo/title-card@1", "output": { "codec": "hevc", "encoder": "nvenc" } }
```
NVENC HEVC on a GPU box; `output.encoder_unsupported` elsewhere.

Registry examples: `showreel`, `three-variants`, `prores-alpha`, `templated-poster`, `kinetic-quote`, `data-story`,
`classic-3d`, `glow`, `trim-paths`, `text-on-path`, `reels-presets`, `glass-loop-60fps`, `webm-alpha`,
`draft-range`, `stacked-alpha-mp4` ([93-schema-render.md](93-schema-render.md)).

