# 50 · The engine CLI: `rexx-engine`

For an assistant that runs the engine directly (a dev box, CI, the eval suite) instead of the service. One binary,
seven subcommands, no network, no clock, no environment beyond four path variables. Source:
`engine/crates/rexx-engine/src/{main,cli,session,events,exit,check,frames,render,convert,track,version,effects}.rs`,
04-engine §4.4.

```
rexx-engine check   --doc doc.json [--assets assets.json] [--variant v] [--data data.json] [--canonical]
                    [--lint-platform tiktok] [--lint-disable a,b] [--sims] [--cost-model model.json] [--backend auto|cpu|gpu]
rexx-engine frames  --doc doc.json --out dir/ (--times 0,1.5,@beat2,50%,end-0.5 | --auto 6) [--sheet] [--width 960]
                    [--safe-overlay tiktok] [--transparent] [--no-motion-blur] [--trails] [--seeds 1,2,3 [--sims]]
                    [--format png|webp] [--depth 8|16] [--png-fast] [--scale s] [--no-layer-cache] [--backend …]
rexx-engine render  --doc doc.json --out out.mp4 [--variant v] [--data …] [--range in,out] [--format mp4] [--codec h264]
                    [--quality standard] [--alpha [stacked]] [--fps 30] [--scale 0.5] [--no-audio] [--poster [t]]
                    [--hdr hlg|pq] [--hdr-peak 1000] [--encoder cpu|nvenc] [--no-layer-cache] [--backend …]
                    [--plan n [--sims-out dir]] [--chunk i/n] [--assemble dir] [--segment seconds]
rexx-engine convert --doc doc.json --to canonical|lottie|dotlottie|aejsx|camera --out file [--variant v] [--data …] [--options o.json]
rexx-engine convert --from lottie|dotlottie|svg --in file --out doc.motion.json [--options o.json]
rexx-engine track   --video clip.mp4 --request track.json --out clip.track.json [--base old.track.json] [--preview path|sheet|none]
rexx-engine version [--protocol | --outputs]
rexx-engine effects [--pretty]
```

Flags are `--name value` or `--name=value`; a flag whose next token starts with `--` (or is last) is bare; a repeated
flag keeps the last value; flags are order-independent; a positional argument, an unknown flag or an unknown
subcommand is a usage error (`internal.usage`, exit 5). Flag values are never read from the environment.

## Common flags (every subcommand)

| Flag | Meaning |
|---|---|
| `--memory-mb N` | the run's memory cap: RSS of the engine plus its ffmpeg children; within 10 % the render caches shrink, past it `limit.memory` (exit 4); the render caches get 60 % of it (2 GiB without a cap) |
| `--threads N` | a fixed worker-thread count (rayon); 0/absent: `available_parallelism` inside the cgroup |
| `--fonts DIR` | the font pack (else `REXX_FONTS`, `/opt/rexx/fonts`, the checkout's `fonts/`); without one every text layer is `font.not_found` and the run warns `font.pack_missing` |
| `--library DIR` | the library (else `REXX_LIBRARY`, `/opt/rexx/library`, the checkout's `library/`): themes, presets, components and `library:` assets |
| `--ffmpeg PATH` | the ffmpeg binary (else `REXX_FFMPEG`, then `PATH`); ffprobe is looked for next to it (else `REXX_FFPROBE`) |
| `--sim-dir DIR` | the read-only physics (and particle) bake cache read by input hash; `check` reports `simCacheHits` when set |
| `--no-verify-fonts` | skip the pack's hash check (0.5 s) |
| `--deadline S` | the run's wall-clock deadline in seconds from start-up (> 0): a frame past it is `render.deadline`, the encoder gets what remains (`encode.timeout`) |

The service passes `--ffmpeg`, `--fonts`, `--library`, `--sim-dir`, `--memory-mb`, `--deadline`, `--backend` (when
configured) and, for renders, `--threads`.

## Subcommands

### `check`

| Flag | Meaning |
|---|---|
| `--doc PATH` (required) | the authored document |
| `--assets PATH` | the manifest `{ "<id>": { "path", "sha256", "bytes", "content_type", "probe", "deferred" } }`; absent: `library:` assets are resolved against `--library`, everything else is `asset.unmaterialized` when read |
| `--variant ID` | the variant (`default` or empty: the root comp) |
| `--data PATH` | a JSON object merged over `data` (`null` ignored; invalid JSON: `doc.json` at `/data`) |
| `--canonical` | include the canonical document in `data.canonical` |
| `--lint-platform P` | `none`, `broadcast`, `youtube`, `shorts`, `reels`, `tiktok`, `story`, `square`, `linkedin`, `x` (else `doc.enum` at `/lint/platform`, exit 2) |
| `--lint-disable a,b` | codes to silence (added to the document's `lint.disable`) |
| `--sims` | write every comp's bake to `sims/<hash>.sim` under the working directory and list `{comp, hash, file}` in `data.sims` |
| `--cost-model PATH` | calibration constants for the estimator (`CostModel::from_json`); for fitting, not for callers |
| `--backend B` | the backend the estimate reports (`auto` decides as `render` would) |

Result `data`: `ok`, `doc_hash` (`sha256:` of the canonical export), `stats`, `estimate`, `timing`, `variant`
(when given), `canonical`, `simCacheHits`, `sims`, `diagnosticsTruncated` (past 200). Exit 0 with `ok: true`;
2/3/4 with the diagnostics when the document fails ([11-motion-check.md](11-motion-check.md) for the fields).

### `frames`

| Flag | Meaning |
|---|---|
| `--out DIR` (required) | where `frame-NN.<format>` or `sheet.<format>` go |
| `--times a,b,c` | seconds, `12f`, `@marker[+off]`, `50%`, `end[-off]`, `1.5s`, timecode; outside the comp: `doc.type` at `/times`; unknown marker: `ref.marker` |
| `--auto N` | N key moments (1–64) |
| `--sheet` | one contact sheet (≤ 6 × 4 cells; with seeds: one row per seed) |
| `--width W` | 16–7680 px (single: the still; sheet: the whole sheet; defaults 960 / 1920) |
| `--safe-overlay P` | a platform zone drawn in magenta (`doc.enum` at `/safe_overlay` otherwise) |
| `--transparent` | drop every comp's background |
| `--no-motion-blur` | switch every comp's motion blur off |
| `--trails` | ghosts at ±1, ±2 frames (22 %) |
| `--seeds a,b` | physics seeds (needs `--sheet`; `seeds × times ≤ 64`); non-integers: `output.value` at `/seeds` |
| `--sims` | with `--seeds`: write each variation's bakes to `sims/` and list them in `data.sims` |
| `--format png\|webp` | still format (`webp` through ffmpeg; `output.value` at `/format` otherwise) |
| `--depth 8\|16` | 8: display PNG; 16: linear un-premultiplied 16-bit PNG (`png` only) |
| `--png-fast` | fast deflate for 8-bit PNGs (same pixels) |
| `--scale S` | accepted by the parser; the width decides the scale |
| `--no-layer-cache` | disable the static-layer frame cache (A/B runs) |
| `--backend B` | `auto` (default), `cpu`, `gpu` |

Result: `files`, `stats` {`frames`, `ms_per_frame`, `wall_ms`, `peak_rss_mb`, `layer_cache_hits`,
`layer_cache_misses`, `checkpoint_hits`}, `data` {`frames: [{t, cell, seed?}]`, `width`, `height`, `vary?`,
`sims?`}. Progress events use stage `frames`.

### `render`

| Flag | Meaning |
|---|---|
| `--out PATH` (required except with `--plan`) | the output file (a directory with `--chunk`) |
| `--range in,out` | times in any time form (`out` as seconds is clamped to the comp); empty: `output.value` at `/output/range` |
| `--format`, `--codec`, `--quality`, `--alpha [stacked]`, `--fps`, `--scale`, `--no-audio`, `--hdr`, `--hdr-peak`, `--encoder` | each overrides one field of the document's `output` block ([13-motion-render.md](13-motion-render.md)); unknown values are `output.value` at `/output/<field>` |
| `--poster [t]` | a poster PNG `<stem>-poster.png` beside the output (`true`/bare: the auto frame; else a time) |
| `--no-layer-cache` | as in `frames` |
| `--backend B` | the renderer |
| `--plan n [--sims-out DIR]` | chunk plan: prints `{chunkable, unchunkable?, frames, fps, segmentFrames, segments, chunks: [{index, segments: [a,b], frames: [a,b]}], sims: [files]}` and publishes the bakes into `DIR` |
| `--chunk i/n` | render chunk `i` of `n` into `--out` as `seg<k:05>.<ext>` files (no audio, no poster) |
| `--assemble DIR` | join the segments in `DIR`, mix the audio, write `--out` and the poster |
| `--segment S` | segment length in seconds (1–600; default 10 s for videos over 60 s) |

Result: `files` (the output, then the poster), `stats` {`frames`, `ms_per_frame`, `peak_rss_mb`, `codec`, `format`,
`fps`, `duration`, `width`, `height`, `wall_ms`, `convert_ms`, `write_ms`, `layer_cache_hits`, `layer_cache_misses`,
`checkpoint_hits`, `backend`, `encoder`, and after a chunked assembly `chunks`, `chunk_retries`}. Progress stage
`render`, `frame`/`frames` over the rendered range. A failed run removes its partial files.

### `convert`

| Flag | Meaning |
|---|---|
| `--to T` | `canonical` (default), `lottie`, `dotlottie`, `aejsx`, `camera`; anything else `convert.unavailable` |
| `--from F` | `lottie`, `dotlottie`, `svg`; anything else `convert.unavailable`; needs `--in` |
| `--in PATH` | the file to import (≤ 256 MB for Lottie; a dotLottie must start with `PK`) |
| `--out PATH` | the output; extra files go next to it (`images/`, `fonts/`, `audio/`, `assets/`) |
| `--options PATH` | the options object as JSON ([14-motion-convert.md](14-motion-convert.md); not an object: `doc.type` at `/options`; invalid JSON: `doc.json`) |

Result: `files` (the output first), `data.coverage`. A particle layer rendered for an export runs this same
binary as a child `render --backend cpu` with the common flags forwarded.

### `track`

| Flag | Meaning |
|---|---|
| `--video PATH` | the clip (else the `video` entry of `--assets`); hashed, or the manifest's hash |
| `--request PATH` (required) | the request JSON (`type`, `items`, `range`, `from`, `direction`, `method`, `options`, `corrections`, `solve`, `stabilize`, `camera`; unknown fields are `track.request_invalid`) |
| `--out PATH` | the track file (default `<video stem>.track.json` next to the video) |
| `--base PATH` | a previous track file |
| `--preview PATH\|sheet\|none` | the sheet (a path; `sheet` = `<stem>.track-sheet.png` next to the track; bare = `sheet`) |

Result: `files` (track, sheet), `stats` {`frames`, `wall_ms`, `peak_rss_mb`}, `data` {`type`, `frames`, `summary`,
`method`, `cache_key`, `range`, `from`, `items`, `source: {sha256, size, fps, duration}`, `engine`}. Progress stage
`track`. `method: "ml"` is `track.unavailable` at `/method`.

### `version`

Prints one line: `{"event":"result","engine":"0.1.48","protocol":1,"fonts":"<pack sha256>","library":"2026.10.0",
"ffmpeg":"8.1.3-…","gpu":{"adapter","driver","backend"}|null,"nvenc":["h264","hevc","av1"]|[]}`. `--protocol`
prints the bare protocol number (`1`); `--outputs` prints `{"event":"result","outputs":[{"format","codec","alpha",
"phase"}]}`, the (format, codec, alpha) rows the probed ffmpeg can write (31 with the pinned build: `codec` `""`
for image formats, `alpha` `false`/`true`/`"stacked"`, `phase` `P1`/`P2`).

### `effects`

Prints the effect catalogue as one JSON object: `{"event":"result","engine","counts":{total, implemented,
specified},"effects":[{id, category, phase, implemented, control, tiling, deps, readsTime, params:[{name, kind,
default, animatable, doc}]}]}` (`--pretty` indents). 245 ids in 0.1.48, 240 implemented. The `effects` area of
this folder is generated from it.

## The event protocol (stdout)

One JSON object per line; stderr carries only internal failures.

| `event` | Fields |
|---|---|
| `diagnostic` | `severity`, `code`, `path`, `message`, `hint?`, `related?`, `fix?`, `at?` — sorted by severity, path, code; at most 200 per run |
| `progress` | `stage` (`frames`, `render`, `track`), `frame`, `frames`, `elapsed_ms`; throttled to one per 100 ms except the last of a stage |
| `result` | `files` (paths), `stats?`, `data?` — the last line of a successful run |
| `info` | `code`, `message`, extra fields: today only `render.gpu_declined` with `adapter` |

## Exit codes

| Exit | Meaning | Service class |
|---|---|---|
| 0 | success (warnings and infos may be present) | 200 |
| 2 | the document is invalid: `doc.*`, `ref.*`, `anim.*`, `tween.*`, …, `track.*`, `output.*`, `convert.svg_invalid`, `*.unavailable` | `400 bad_request` with the diagnostics |
| 3 | an asset could not be used: `asset.*`, `media.*` | `400 bad_request` |
| 4 | a resource limit: every `limit.*`, `render.deadline`, `encode.timeout`, `cancelled` (SIGTERM) | `400 bad_request` |
| 5 | a bug or a bad invocation: `internal.*`, `encode.*` (except `encode.timeout`), a panic (`internal.panic`), a usage error (`internal.usage`), an unreadable input file (`internal.io`) | `500 internal`, escalated |

When several errors are present the most specific class wins (5 > 4 > 3 > 2). Cancellation: `SIGTERM` stops at the
next frame (`cancelled`, exit 4, partial outputs removed); the service kills the process group with `SIGKILL`.

## Running it on a dev box

```sh
rexx-engine check --doc my.motion.json --fonts fonts --library library --ffmpeg ~/.cache/rexx-build/ffmpeg/bin/ffmpeg
rexx-engine frames --doc my.motion.json --auto 6 --sheet --out /tmp/sheet --fonts fonts --library library --ffmpeg …
rexx-engine render --doc my.motion.json --out /tmp/out.mp4 --quality draft --fonts fonts --library library --ffmpeg …
```

`fonts/files` must hold the pack (`python3 fonts/fetch.py`, or a symlink to a fetched pack); `library/` is the
checkout's. Assets by https URL need a manifest the service would have written: on a dev box use `library:` assets
or write `assets.json` by hand with local paths.

## Flag inventory (generated from `cli.rs`)

<!-- gen:tools-cli:start -->

| Subcommand | Flags (in parser order) |
|---|---|
| every subcommand (`COMMON`) | `--memory-mb`, `--threads`, `--fonts`, `--library`, `--ffmpeg`, `--sim-dir`, `--no-verify-fonts`, `--deadline` |
| `check` | `--doc`, `--assets`, `--variant`, `--data`, `--canonical`, `--lint-platform`, `--lint-disable`, `--sims`, `--cost-model`, `--backend` |
| `frames` | `--doc`, `--assets`, `--variant`, `--data`, `--times`, `--auto`, `--sheet`, `--width`, `--safe-overlay`, `--transparent`, `--no-motion-blur`, `--trails`, `--seeds`, `--sims`, `--out`, `--format`, `--scale`, `--depth`, `--png-fast`, `--no-layer-cache`, `--backend` |
| `render` | `--doc`, `--assets`, `--variant`, `--data`, `--out`, `--range`, `--format`, `--codec`, `--quality`, `--alpha`, `--fps`, `--scale`, `--no-audio`, `--poster`, `--hdr`, `--hdr-peak`, `--encoder`, `--no-layer-cache`, `--backend`, `--plan`, `--chunk`, `--assemble`, `--segment`, `--sims-out` |
| `convert` | `--doc`, `--assets`, `--variant`, `--data`, `--to`, `--out`, `--from`, `--in`, `--options` |
| `track` | `--video`, `--assets`, `--request`, `--out`, `--base`, `--preview` |
| `version` | `--protocol`, `--outputs` |
| `effects` | `--pretty` |
<!-- gen:tools-cli:end -->
