# 16 · The render pipeline: estimate, backends, the cache, chunking, HDR, NVENC

What happens between a `motion.render` call and its file, and which inputs decide whether two calls share a result.
Source: `service/src/tools/render.rs`, `service/src/cache.rs`, `service/src/chunked.rs`, `service/src/engine.rs`,
`service/src/janitor.rs`, `engine/crates/rexx-engine/src/render.rs`, 03-architecture §3.6–3.8, 04-engine §4.16,
15-gpu-backend §15.2, spec 13 §13.4.4, §13.5.2, §13.5.5.

## The estimate and admission

`rexx-engine check` prices every layer, effect, text animator and particle system per frame from the cost model's
coefficients (`rexx-lint/cost.rs`, calibrated on the reference box) and reports `estimate.renderSeconds` for the
whole render on one box with every thread. The service:

1. scales it to the render's thread share: `× box_threads / share_threads` where `share_threads = ceil(box_threads ×
   cost / budget)` (2 of 4 on a ccx23 at budget 11, so ×2), then by `span / duration` for a `range`;
2. divides it by the worker count when the variant will be chunked;
3. sums the variants and compares with `REXX_SYNC_BUDGET` (240 s) on `/v1/run`, `REXX_JOB_TIMEOUT` (20 min) on
   `/v1/jobs`.

The engine also gets `--memory-mb` (90 % of the cgroup: 5529 MB for a render) and `--deadline` (what remains of the
tool timeout); past the deadline a frame fails with `render.deadline`, an encode with `encode.timeout`
(exit 4, a `400`), before the framework kills the run (`504`).

## Backends: `auto`, `cpu`, `gpu`

A job renders on one backend, decided before the first frame (never per frame):

- `check` reports `estimate.backend` (`cpu` or `gpu`), `cpuMs`, `gpuMs`, `gpuComplete`. The GPU is chosen when the
  box has a usable adapter, the device takes the main comp's frame, the plan has nothing the GPU seam declines (a
  backdrop effect in the main comp or an uncollapsed nested comp, a texture that does not fit) and `gpuMs × 0.85 <
  cpuMs`. Light comps stay on the CPU (upload and readback cost more than they save).
- `REXX_ENGINE_BACKEND` (`auto`, `cpu`, `gpu`) is passed as `--backend` to `check`, `frames` and `render` and
  overrides the decision box-wide; `gpu` on a box without an adapter (or an engine built without the `gpu`
  feature) is `limit.gpu_unavailable`; `auto` falls back to the CPU silently.
- At render time the GPU may still decline the job (the `info` event `render.gpu_declined`, reported once; the whole
  job re-plans on the CPU). A device lost mid-job is `render.gpu_lost`: the job fails and the service re-runs it on
  the CPU once. `limit.gpu_memory`: a texture or readback the job's share cannot hold.
- A GPU-only effect (`utility.shader`) on a CPU job renders unshaded with `effect.requires_gpu` (`check` says so
  with `estimate.requiresGpu`).
- The backend is a term of the cache key and the output's metadata (`rexx_backend=gpu`): a CPU and a GPU render of
  one document are two entries whose bytes differ within the golden tolerance. A render that ran on another backend
  than the key's (the GPU declined after `check` put it there) is not stored.
- `/healthz` shows the adapter as `gpu` ("none" on a CPU box). The fleet routes `backend: gpu` jobs to the GPU pool
  when it has capacity, else to the CPU pool with `backend: cpu` (slower, not wrong).

## The render cache

Key terms, in order, hashed together (`cache::key_of`):

| Term | What changes it |
|---|---|
| engine version | every engine release |
| font pack hash, library version, ffmpeg version | the image (reported by `rexx-engine version`) |
| `doc_hash` | the engine's `sha256:` of the **canonical** document for the variant (so a different `data` overlay, variant or authored form with the same canonical result shares an entry; an engine that reports none falls back to `sha256(authored bytes)/<variant>/<data JSON>`) |
| asset hashes | every materialized asset's SHA-256, sorted (a changed image, a different `library:` file) |
| variant id | |
| settings | the `output` overrides as given (only non-empty fields), the resolved `format`, and the raw `poster` value (so `poster: true` and no poster are different entries; `1.2` and `1.20` are the same number) |
| range | the `range` as given |
| backend | `cpu` / `gpu` from the variant's check |
| encoder | `cpu` / `nvenc` as resolved |

Two calls share a result when every term matches; the document's own `output` block only matters through the
resolved format, `doc_hash` (it is part of the canonical document) and the override fields. A hit (one HEAD on
`rexx/cache/index/<key>`, bounded at 500 ms; any failure is a miss) copies `rexx/cache/objects/<key><ext>` (and
`<key>-poster.png` when a poster was asked) server-side into the caller's prefix, bills the base price only and
reports `cache_hit: true` with the keyed `backend`/`encoder`. A fresh render is stored after upload (index written
last; `stored_at`, `objects`, `tool`, `variant`, `format`, `backend`, `encoder` in the index). The janitor removes
entries unused for 30 days (a hit writes a touch marker). `motion.frames` is **not** cached (06 §6.5 says "the same
applies to `motion.frames` per still"; it does not).

## Chunked rendering (`REXX_CHUNK_*`)

A variant of at least `REXX_CHUNK_FROM` (default 2 min) is rendered in chunks when the box has two or more workers:
`REXX_CHUNK_LOCAL` engine processes on this box (default 0) plus one per `REXX_CHUNK_PEERS` entry (base URLs such
as `http://10.27.1.11:7200`, default none). Chunking is off by default (one worker). Only `mp4`, `mov` and `webm`
outputs chunk, and only when the engine's plan says `chunkable` (not: two-layer alpha streams `yuva420p`, a PQ
output, a two-pass `bitrate` encode, GIF/WebP/AVIF/sequences, a render of 60 s or less).

1. **Plan** on this box: `render --plan <workers> --sims-out <dir>` splits the segments (10 s each, encoded by an
   encoder of their own and joined without re-encoding) into chunks of whole segments and publishes every physics
   bake (`<hash>.sim`) and the particle bakes of systems alive across a boundary (`<hash>.psim`); peers get them as
   URLs under the caller's prefix (`sims/<name>`).
2. **Chunks**: local workers run `render --chunk i/n --sim-dir <dir>`; peers get a `motion.render` job on their
   `/v1/jobs` with the hidden input `chunk: { index, of, sims: [urls], backend }` (the document inline, the variant,
   the `output` overrides, the `data`; no poster), signed with the fleet's `JWT_SIGNING_SECRET` as tenant
   `rexx-chunk:<uid>`; only that tenant prefix may ask for a chunk (a user's own `chunk` input is `400` "chunk is
   not an input of this tool"). A chunk job is neither cached, charged nor counted against quotas. Each worker takes
   the next chunk when free; a failed chunk goes back to the queue for another worker (the failed worker takes no
   more), at most `REXX_CHUNK_RETRIES` (2) times; a peer's chunk may run `REXX_CHUNK_TIMEOUT` (15 min). Every chunk
   renders on the backend the variant's check resolved.
3. **Assemble** on this box: `render --assemble <segments> --sim-dir <dir> --out <file>` joins the segments, mixes
   the audio once, writes the poster. The file is byte-identical to the one-box render. The stats gain `chunks` and
   `chunk_retries`.

Progress during chunks is reported per finished chunk. An output the plan refuses renders on this box as usual.

## Deterministic files and encoders

The same canonical document, assets, engine, ffmpeg build, settings, backend and encoder give the same bytes
(`-fflags +bitexact`, pinned thread counts per preset, no creation time). Videos over 60 s are always written as
10-second segments; `output.bitrate` applies per segment. The CPU encoders: x264 (`h264`), x265 (`hevc`, Main10 by
default; the two-layer alpha encode at one frame thread), SVT-AV1 (`av1`), libvpx (`vp9`), `prores` /
`prores_ks` (`master`), libaom through the `avif` muxer; quality rows in spec 13 §13.5.1.

**NVENC** (`output.encoder: "nvenc"`): `h264_nvenc`, `hevc_nvenc`, `av1_nvenc` with presets `p1`/`p4`/`p5`/`p7`
for `draft`/`standard`/`high`/`master`, constant quality `cq` matched to the CPU rows, B-frames and GOP pinned, so
the bytes are stable per (ffmpeg build, driver, GPU) and are the encoder's own (a separate cache entry; the file
carries `rexx_encoder=nvenc`). The engine probes each encoder by encoding two frames at boot; `rexx-engine version`
lists the codecs that passed as `nvenc` and `/healthz` shows them (`"none"` on a CPU box). Refused with
`output.encoder_unsupported` (pointer `/output/encoder` or `/doc/output/encoder`, before any frame): `prores`,
`vp9`, `alpha: true` (use `"stacked"`), `hdr: "pq"` (HDR10 metadata is written by x265 and SVT-AV1 only; HLG
works), `pixelFormat` `yuv422p10`, 4:4:4 AV1, image/animation/sequence formats, a frame under 160 × 90, a `preset`
outside `p1`–`p7` (`output.value`), `crf` over 51 for h264/hevc, and a box whose probe found no working encoder for
the codec. `check` reports `estimate.encoder` so the router puts an NVENC document on the GPU pool.

## HDR (`output.hdr`)

`hlg` or `pq` keeps values above 1 (1.0 = 203 cd/m²), converts the comp's working space to Rec.2020 and encodes
10-bit HEVC Main10 (`mp4`, `mov`; the default codec with `hdr`) or SVT-AV1 10-bit (`mp4`, `webm`) with BT.2100 tags.
`pq` writes the mastering display (peak `output.hdrPeak`, 100–10,000, default 1,000) and MaxCLL/MaxFALL measured
from the rendered frames (so a PQ output cannot be chunked); `hlg` is fixed at the 1,000 cd/m² display (`hdrPeak`
with `hlg` is `output.value`). The document's `output.toneMap` (`clip`, `soft`, `aces2`) shapes highlights.
Refused with `output.hdr_unsupported`: image and sequence formats, `h264`/`vp9`/`prores`, any alpha, profile
`main`; an 8-bit `pixelFormat` is `output.pixel_format`. Posters and `motion.frames` stills of an HDR document are
SDR. HLG is what Instagram plays as HDR; YouTube takes both.

## Stacked alpha

`alpha: "stacked"` writes colour (premultiplied over black) in the top half and alpha as full-range luma with
neutral chroma in the bottom half of an opaque video twice the comp's height, tagged `rexx_alpha=stacked`; the
`variants.<id>.width`/`height` report the frame size, the file is twice the height. Rows: `mp4`/`mov` + `h264`/`hevc`,
`webm` + `vp9` (stacked AV1 is a later phase).

## Memory, stalls, cancellation

The engine watches its own RSS (plus ffmpeg's) every 25 ms against `--memory-mb`; within 10 % of it the render
caches are evicted, past it the run fails with `limit.memory` (exit 4) before the cgroup kills it. A run with no
event line for 60 s is killed and escalated (`500 internal` "rendering made no progress for 1m0s and was stopped"). A
cancelled job (`DELETE /v1/jobs/{id}`) kills the process group (engine and ffmpeg); partial outputs are removed.
