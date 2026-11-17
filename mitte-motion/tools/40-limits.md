# 40 · Limits, caps and budgets in one place

Every number that can refuse, truncate or time out a call: the service's request caps (06 §6.9), the engine's
document ceilings (spec 1 §1.12), the chapter limits (spec 9 §9.11, 10 §10.10, 19 §19.11), the memory and time
budgets of a run, and the diagnostic codes each one raises. The first tables are generated from the sources by
`scripts/skills-tools-limits.py`; the rest is written against the spec and the code, with the code's value where
they differ.

## The checked-against rule

`motion.check` validates against the service's caps (`Limits::service_p1`: 3840 × 2160, 600 s, 1–60 fps; everything
else the engine ceiling), so a document that passes check never fails a render on a document limit. Request caps
(variants, stills, seeds, footage, items, bytes) are enforced at the tool boundary as `413 too_large`, before the
engine runs; document limits are the engine's `limit.*` diagnostics (exit 4).

## Request caps and quotas (the service)

| What | Cap | Env | Refusal |
|---|---|---|---|
| Inline `doc` (re-encoded) and a fetched `doc_url` | 1 MiB | `REXX_MAX_DOC_BYTES` | `413` "the document is N KB; the limit is M KB"; the HTTP body is this + 1 MiB |
| Declared assets per document | 512 | `REXX_MAX_ASSETS` | `413` |
| One asset / all assets of a document / fetch time | 512 MiB / 2 GiB / 120 s | `REXX_MAX_ASSET_BYTES`, `REXX_MAX_ASSETS_TOTAL_BYTES` | `413 asset.too_large`, `400 asset.unreachable` (timeout) |
| Rendered seconds per variant | 600 s | `REXX_MAX_DURATION` | `413` "variant … is Ns long; the limit is 600s per variant" |
| Frames per render, all variants | 86,400 | `REXX_MAX_FRAMES` | `413` |
| Output size per variant (after `scale`) | 3840 × 2160 (width × height ≤ 8,294,400) | `REXX_MAX_PIXELS` | `413` |
| Output fps | 60 | `REXX_MAX_FPS` | `413` |
| Variants per render | 6 | `REXX_MAX_VARIANTS` | `413` |
| Cells per `motion.frames` call (times × seeds) | 24 | `REXX_MAX_STILLS` | `413` |
| Seeds per `motion.frames` call | 6 | `REXX_MAX_SEEDS` | `413` |
| Footage per `motion.track` call | 120 s | `REXX_MAX_TRACK_DURATION` | `413` "(use range)" |
| Items per `motion.track` call | 32 point/face, 8 planar/mask | `REXX_MAX_TRACK_ITEMS` | `413` |
| Sync estimate (scaled to the thread share) | 240 s | `REXX_SYNC_BUDGET` | `413` "submit via POST /v1/jobs" |
| Job estimate | 20 min | `REXX_JOB_TIMEOUT` | `413` "shorten or split the document" |
| Track admission (no engine estimate) | 8 s box time per footage second (unknown duration = 120 s) | — | `413` |
| Pending jobs per box | 32 | `REXX_JOBS_MAX_PENDING` | `503` "job queue full; retry with backoff" |
| Per-minute per tenant | data 300, frames 60, render 30 | — | `429 rate_limited` |
| Per-day per tenant | guide 2,000, check 2,000, convert 500, frames 2,000, track 600 s, render 60 min | `REXX_QUOTA_*` | `429 overloaded` |
| Box budget | 11 units (render 4, frames 2, check/convert/guide 1, track 2); 2 reserved for sync | `REXX_BUDGET` | wait, then `503` |

## Time and memory budgets of a run

| Run | Timeout (`--deadline`) | cgroup | `--memory-mb` (90 %) | Threads |
|---|---|---|---|---|
| `motion.check` | 60 s | 1 CPU / 1 GiB / 256 pids | 921 | engine's own |
| `motion.frames` | 120 s | 4 CPU / 2 GiB | 1843 | engine's own |
| `motion.render` | 20 min | 4 CPU / 6 GiB | 5529 | `ceil(box × 4 / 11)` (2 of 4) |
| `motion.convert` | 120 s | 1 CPU / 1 GiB | 921 | engine's own |
| `motion.track` | 10 min | 4 CPU / 4 GiB | 3686 | engine's own |

Inside a run: a frame past the deadline is `render.deadline`; the encoder's wall limit is what remains of the
deadline (without one: rendered seconds × 60 + 600 s) → `encode.timeout`; RSS over `--memory-mb` after cache
eviction → `limit.memory` (all exit 4); no event line for 60 s → killed (`500`); an engine deadline-free `check`
has the normalization budget `limit.normalize_time` in the spec (20 s; not enforced by the engine today, the tool
timeout is the bound). Engine-side: at most 64 `frames` times per call (`limit.frames`), 216,000 camera-path
frames (`limit.frames`), 200 diagnostics per run (errors first; the engine keeps at most 10,000 per frame), a
chunk peer job 15 min (`REXX_CHUNK_TIMEOUT`), chunk retries 2, guide sections sized under 2,000 tokens.

## Document limits (spec 1 §1.12 and the chapters)

| Limit | Engine ceiling | Service cap | Code |
|---|---|---|---|
| Document size (authored JSON) | 2 MB | 1 MiB inline (`doc_url` up to 2 MB) | `limit.doc_size` |
| Canonical document | 32 MB | same | `limit.canonical_size` |
| `data` | 512 KB | same | `limit.data_size` |
| Comps | 256 | same | `limit.comps` |
| Layers per comp (after normalization; counted before expansion) | 2,000 | same | `limit.layers` |
| Comp nesting (also Lottie precomp depth) | 16 | same | `limit.nesting` (at render `render.depth`) |
| Keys per property / total | 10,000 / 1,000,000 | same | `limit.keys`, `limit.keys_total` |
| `repeat` count per repeat / per document | 1,000 / 10,000 | same | `limit.repeat` |
| Frame size (output comp and variants) | 7680 × 4320, 33.2 MP; nested comps 16,384 px per side, 64 MP | 3840 × 2160 | `limit.frame_size` |
| Rendered duration | 30 min | 600 s per variant | `limit.duration` |
| Frame rate | 1–240 | 1–60 | `limit.fps` |
| Text per layer | 10,000 characters | same | `text.too_long` |
| Expression steps per evaluation / per check or render; call depth; heap | 100,000 / 5 × 10⁸; 64; 16 MB | same | `expr.budget`, `limit.expr_total`, `expr.depth`, `expr.memory` |
| Assets per document / total | 512 / 4 GB (service 2 GB) | | `limit.assets` |
| Image pixels per asset | 16,384 px per side, 64 MP | | `media.image_too_large` (spec 1 names `limit.image_size`, never emitted) |
| Video | 7680 × 4320 | | `media.video_too_large` |
| Video / audio sources per render | 32 / 64 | | `limit.video_sources` (not emitted today), `limit.audio_sources` |
| Decoded audio in memory | the crate cap | | `limit.audio_duration` |
| Image sequence frames | 20,000 | | `limit.sequence_frames` |
| Archives (sequence zips, dotLottie) | ≤ 2 GB unpacked, ratio ≤ 100, ≤ 1,000 entries | | `limit.archive` |
| SVG | 50,000 nodes, `use` depth 16 | | `limit.svg` |
| Lottie import | 20 MB JSON, 5,000 layers, depth 16; input file ≤ 256 MB | | `limit.lottie` (`asset.unreadable` over 256 MB) |
| Caption words | 50,000 | | `limit.caption_words` |
| Gradient stops | 64 (resampled, no error) | | — |
| Particles: systems per layer / alive per system / per layer / births per layer / `preroll` / line pairs per frame | 8 / 1,000,000 / 2,000,000 / 50,000,000 / 30 s / 2,000,000 | | `limit.particle_systems`, `limit.particles`, `limit.particle_births`, `limit.preroll`, `limit.particle_lines` (warning) |
| Particles: sprite pixels per frame per layer (alive × largest diameter², glow included, each ≤ the frame) | 128 frames of the comp, at least 128 × 1920 × 1080 | | `limit.particles` |
| Particles: ribbon segments / texture frames | 64 / 64 | | clamped |
| Particles: shadowlet `resolution` / a layer's own `limits` | 8–128 / at most the engine caps | | `doc.type` |
| Physics: bodies / bake / joints / forces per comp | 2,000 / 64 MB / 1,000 / 256 | | `limit.physics_bodies`, `limit.physics_bake`, `limit.physics_joints`, `limit.physics_forces` |
| Physics: rate / span / convex parts per body / vertices per part / named groups | 60–960 Hz / ≤ comp and the duration cap / 64 / 256 / 30 | | `physics.rate_range`, `physics.span`, `physics.shape_too_complex`, `physics.unavailable` |
| Tracking: footage per file / items per request | 10 min / 64 | 120 s / 32 + 8 | `limit.track_duration`, `limit.track_items` |
| Track file read by a document (`type: "track"` asset) | 16 MB (not the 512 KB `data` cap) | same | `track.asset_missing` |
| 3D: drawable layers per run / lights / shadow lights / shadow map side | 256 / 64 / 8 / 64–4096 (default 1024) | | `limit.3d_run_layers`, `limit.3d_lights` (w), `limit.3d_shadow_lights` (w), clamped |
| 3D bounds | zoom 10⁻³–10⁷ px, coordinates ±10⁹ px, circle of confusion 128 px | | clamped; `layer.light_invalid` (w) for lights beyond |
| Matte chain depth | 8 | | `matte.depth` (spec), `render.matte` (w, renderer) |
| Component nesting | 4 instances deep inside definitions; expansion depth 16 | | `component.depth`, `component.cycle` |
| GPU memory | the job's share of the budget | | `limit.gpu_memory` |

## Generated defaults

<!-- gen:tools-limits:start -->

### Service request caps (`service/src/config.rs`, `Limits::default`)

| Field | Default |
|---|---|
| `max_duration` | 600 s |
| `max_frames` | 86,400 |
| `max_width` | 3840 |
| `max_height` | 2160 |
| `max_fps` | 60 |
| `max_variants` | 6 |
| `max_stills` | 24 |
| `max_seeds` | 6 |
| `max_doc_bytes` | 1048576 bytes (1 MiB) |
| `max_assets` | 512 |
| `max_asset_bytes` | 536870912 bytes (512 MiB) |
| `max_assets_total` | 2147483648 bytes (2 GiB) |
| `max_track_duration` | 120 s |
| `max_track_points` | 32 |
| `max_track_regions` | 8 |

### Daily quotas (`QuotaConfig`)

| Class | Default |
|---|---|
| `check_calls` | 2000 (`REXX_QUOTA_CHECK`) |
| `convert_calls` | 500 (`REXX_QUOTA_CONVERT`) |
| `frames` | 2000 (`REXX_QUOTA_FRAMES`) |
| `track_seconds` | 600 (`REXX_QUOTA_TRACK_SECONDS`) |
| `render_minutes` | 60 (`REXX_QUOTA_RENDER_MINUTES`) |

### Every `REXX_*` default the service reads (`config.rs`, `chunked.rs`)

| Variable | Default |
|---|---|
| `REXX_MAX_PIXELS` | 3840x2160 |
| `REXX_MAX_TRACK_ITEMS` | 32,8 |
| `REXX_QUOTA_CHECK` | 2000 |
| `REXX_QUOTA_CONVERT` | 500 |
| `REXX_QUOTA_FRAMES` | 2000 |
| `REXX_QUOTA_TRACK_SECONDS` | 600 |
| `REXX_QUOTA_RENDER_MINUTES` | 60 |
| `REXX_CACHE_ROOT` | /var/cache/rexx |
| `REXX_ENGINE_BIN` | rexx-engine |
| `REXX_SCHEMA_PATH` | engine/schema/motion-1.json |
| `REXX_SYNC_BUDGET` | 240 s |
| `REXX_JOB_TIMEOUT` | 1200 s |
| `REXX_MAX_DURATION` | 600 s |
| `REXX_MAX_FRAMES` | 86,400 |
| `REXX_MAX_FPS` | 60 |
| `REXX_MAX_VARIANTS` | 6 |
| `REXX_MAX_STILLS` | 24 |
| `REXX_MAX_SEEDS` | 6 |
| `REXX_MAX_DOC_BYTES` | 1048576 bytes (1 MiB) |
| `REXX_MAX_ASSETS` | 512 |
| `REXX_MAX_ASSET_BYTES` | 536870912 bytes (512 MiB) |
| `REXX_MAX_ASSETS_TOTAL_BYTES` | 2147483648 bytes (2 GiB) |
| `REXX_MAX_TRACK_DURATION` | 120 s |
| `REXX_PRICE_PER_MINUTE_USD` | 0.35 |
| `REXX_PRICE_PER_FRAME_USD` | 0.002 |
| `REXX_PRICE_TRACK_PER_MINUTE_USD` | 0.10 |
| `REXX_CHUNK_LOCAL` | 0 |
| `REXX_CHUNK_FROM` | 120 s |
| `REXX_CHUNK_RETRIES` | 2 |
| `REXX_CHUNK_TIMEOUT` | 900 s |
| `(framework `REXX_PORT`)` | 7200 |
| `(framework `REXX_BUDGET`)` | 11 |
| `(framework `REXX_SCRATCH_ROOT`)` | /var/sandbox |
| `(framework) r2_key_prefix` | rexx/ |
| `(framework) price_base_usd` | 0.05 |
| `(framework) price_per_mb_usd` | 0.0001 |

### Engine ceilings (`rexx-doc` `Limits::engine`) and the P1 service caps passed to it (`Limits::service_p1`)

| Field | Engine ceiling | Service P1 |
|---|---|---|
| `doc_size` | 2 MiB | same |
| `canonical_size` | 32 MiB | same |
| `data_size` | 512 KiB | same |
| `comps` | 256 | same |
| `layers` | 2,000 | same |
| `nesting` | 16 | same |
| `keys` | 10,000 | same |
| `keys_total` | 1,000,000 | same |
| `repeat` | 1,000 | same |
| `repeat_total` | 10,000 | same |
| `frame_width` | 7680 | 3840 |
| `frame_height` | 4320 | 2160 |
| `frame_pixels` | 33,200,000 | same |
| `frame_side` | 16,384 | same |
| `nested_pixels` | 67,108,864 (64 MP) | same |
| `duration` | 1800.0 | 600.0 |
| `fps_min` | 1.0 | same |
| `fps_max` | 240.0 | 60.0 |
| `assets` | 512 | same |
| `particle_systems` | 8 | same |
| `particles` | 1,000,000 | same |
| `particles_layer` | 2,000,000 | same |
| `particle_births` | 50,000,000 | same |
| `preroll` | 30.0 | same |
| `physics_bodies` | 2,000 | same |
| `physics_joints` | 1,000 | same |
| `physics_forces` | 256 | same |
| `text_chars` | 10,000 | same |
<!-- gen:tools-limits:end -->
