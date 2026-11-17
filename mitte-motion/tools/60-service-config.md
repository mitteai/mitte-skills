# 60 · Service configuration, health and metrics

Every variable the `rexx` service reads, what `/healthz`, `/readyz`, `/v1/status` and `/metrics` answer, and how
the engine is wired. Source: `service/src/config.rs`, `service/src/boot.rs`, `service/src/api.rs`,
`service/src/metrics.rs`, `service/src/janitor.rs`, `.env.example`, 03-architecture §3.10–3.11.

## Environment variables

Framework variables (`toolservice`, prefix `REXX`): **required** `JWT_SIGNING_SECRET`, `R2_BUCKET_NAME`,
`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PUBLIC_URL` (the service refuses to start without
them, exit 2 "missing required env vars: …"); optional `REXX_PORT` (7200), `REXX_BUDGET` (11), `REXX_SCRATCH_ROOT`
(`/var/sandbox`), `REXX_DB_PATH` (the SQLite job store; unset or `off` disables persistence), `REXX_JOBS_MAX_PENDING`
(32), `REXX_JOBS_RETENTION` (168h), `REXX_JOBS_MAX_ATTEMPTS` (2), `REXX_SHUTDOWN_TIMEOUT` (5s; production sets the
job cap plus margin, `deploy.json` `stop_timeout_sec` 1260), `REXX_PRICE_BASE_USD` (0.05), `REXX_PRICE_PER_MB_USD`
(0.0001), `R2_KEY_PREFIX` (`rexx/`), `MITTE_API_URL`, `MITTE_OAUTH_CLIENT_ID`, `MITTE_ADMIN_API_KEY` (the playground
and node sync), `LOG` (`*` for info, a comma list of scopes, empty for warn) or `RUST_LOG`. A `.env` next to the
binary is loaded.

rexx's own (`RexxConfig`; the defaults as the code has them are in [40-limits.md](40-limits.md)):

| Variable | Default | Meaning |
|---|---|---|
| `REXX_CACHE_ROOT` | `/var/cache/rexx` | the asset cache (`assets/`), the physics sim cache (`sim/`, bound read-only into the jail, 10 GB LRU) and the GPU shader cache (`gpu-pipelines/`) |
| `REXX_TENANTS` | empty (everyone) | comma-separated JWT tenants allowed to submit `motion.*` work during internal testing; others get `403 forbidden` |
| `REXX_ENGINE_BIN` | `rexx-engine` | the engine binary (a name on `PATH` or an absolute path) |
| `REXX_FFMPEG` (else `FFMPEG_PATH`) | `ffmpeg` | passed as `--ffmpeg` on every run and on `version`; `ffprobe` is its sibling |
| `REXX_FONTS`, `REXX_LIBRARY` | unset | passed as `--fonts`, `--library`; unset leaves the engine's own resolution (`/opt/rexx/{fonts,library}`, else the checkout). `REXX_LIBRARY` is also where `library:` asset URIs resolve and a read-only bind in the jail |
| `REXX_ALLOW_NO_ENGINE` | off | `/readyz` reports ready without an engine, and a failed jail validation runs the engine unsandboxed (dev only) |
| `REXX_SCHEMA_PATH` | `engine/schema/motion-1.json` | served at `/v1/schema/motion-1.json` (404 "the document schema is not installed on this box" when missing) |
| `REXX_SYNC_BUDGET` | 240s | the scaled-estimate ceiling for `/v1/run` |
| `REXX_JOB_TIMEOUT` | 20m | the job cap (the estimate ceiling on `/v1/jobs`) |
| `REXX_ENGINE_PROFILE` | jail | `native` runs the engine outside the jail (tests, the stub) |
| `REXX_ENGINE_ENV` | empty | `KEY=VALUE,…` for a native engine process (the stub's `STUB_*` knobs) |
| `REXX_ENGINE_BACKEND` | empty (`auto`) | `auto`, `cpu`, `gpu`: passed as `--backend` to `check`, `frames`, `render` |
| `REXX_MAX_DURATION`, `REXX_MAX_FRAMES`, `REXX_MAX_PIXELS` (`WxH`), `REXX_MAX_FPS`, `REXX_MAX_VARIANTS`, `REXX_MAX_STILLS`, `REXX_MAX_SEEDS`, `REXX_MAX_DOC_BYTES`, `REXX_MAX_ASSETS`, `REXX_MAX_ASSET_BYTES`, `REXX_MAX_ASSETS_TOTAL_BYTES`, `REXX_MAX_TRACK_DURATION`, `REXX_MAX_TRACK_ITEMS` (`points,regions`) | see [40-limits.md](40-limits.md) | the request caps; a malformed `REXX_MAX_PIXELS` or `REXX_MAX_TRACK_ITEMS` fails boot (exit 2) |
| `REXX_QUOTA_GUIDE`, `REXX_QUOTA_CHECK`, `REXX_QUOTA_CONVERT`, `REXX_QUOTA_FRAMES`, `REXX_QUOTA_TRACK_SECONDS`, `REXX_QUOTA_RENDER_MINUTES`, `REXX_QUOTA_DB_PATH` | 2000, 2000, 500, 2000, 600, 60; `quota.db` beside the jobs db else memory | the daily per-tenant caps (0 disables one) |
| `REXX_PRICE_PER_MINUTE_USD`, `REXX_PRICE_PER_FRAME_USD`, `REXX_PRICE_TRACK_PER_MINUTE_USD` | 0.35, 0.002, 0.10 | prices |
| `REXX_CHUNK_PEERS`, `REXX_CHUNK_LOCAL`, `REXX_CHUNK_FROM`, `REXX_CHUNK_RETRIES`, `REXX_CHUNK_TIMEOUT` | none, 0, 2m, 2, 15m | chunked rendering ([16-render-pipeline.md](16-render-pipeline.md)) |

The engine itself reads only `REXX_FONTS`, `REXX_LIBRARY`, `REXX_FFMPEG`, `REXX_FFPROBE` (and inside the jail
nothing: the service passes paths as flags).

`.env.example` shows every `REXX_*` default; `service/tests/units.rs` (`env_example_shows_the_defaults`) holds its
limits, admission, quota and pricing lines to the config struct (K-30). The container caps and the expression
budget are the engine's constants, not variables, as 06 §6.9 now says.

## Boot sequence (what can refuse to start)

sim cache dir → jail validation (bwrap; `REXX_ENGINE_PROFILE=native` skips it, `REXX_ALLOW_NO_ENGINE` degrades to
native) → the engine probed (`version --protocol`, `version`, `version --outputs` with the stack flags; a missing
binary leaves `/readyz` at 503 unless allowed) → the asset fetcher → the quota store → R2 → the registry →
jobs recovery from SQLite → the HTTP listener on `0.0.0.0:<port>` → `sd_notify` ready. Exit codes: 0 normal, 1
runtime/boot failure, 2 configuration. `SIGTERM`/`Ctrl-C` marks `/readyz` 503, drains running jobs for
`REXX_SHUTDOWN_TIMEOUT`, then stops. Touching `/var/run/rexx-drain` flips `/readyz` to 503 without stopping.

## `/healthz`

```jsonc
{ "status": "ok", "version": "engine-v0.1.48-2-g975dfdf / 975dfdf",
  "engine": "0.1.48", "engine_bin": "/opt/rexx/bin/rexx-engine", "protocol": "1", "protocol_expected": "1",
  "ffmpeg": "8.1.3-14-g330caae0c1-20261007", "ffmpeg_path": "/opt/rexx/ffmpeg/bin/ffmpeg",
  "fonts": "06acc477…", "library": "2026.10.0", "guide": "2026.10.0",
  "gpu": "NVIDIA RTX 4000 SFF Ada Generation (580.xx)",   // "none" on a CPU box
  "nvenc": "h264,hevc,av1",                               // "none" without a working encoder
  "ready": true, "checks": { "disk": true, "engine": true, "ffmpeg": true, "protocol": true } }
```

Always 200. `engine` is `unavailable` (and `protocol` absent) when the probe failed; the probe is refreshed every
15 s in the background. `fonts`, `library`, `guide`, `ffmpeg` are the hashes/versions `rexx-engine version` reports
and the terms of the render cache key.

## `/readyz`

`200 {"status":"ready"}` when every check passes and the drain marker is absent; otherwise `503` with
`{ "status": "not_ready", "checks": { "ffmpeg": bool, "engine": bool, "protocol": bool, "disk": bool },
"details": { "engine": "binary not found: …", "engine_allowed_missing": true, "protocol": "engine speaks protocol
N, this binary expects 1" } }` (just `{"status":"not_ready"}` while draining). The load balancer polls it.

## `/v1/status` (JWT)

The framework's budget view (`status`, in-use and total budget units, per-tool concurrency) plus `version`,
`jobs: { "pending": n, "in_progress": n }` and `engine: { … }` (the `/healthz` engine fields).

## `/metrics`

The framework's `rexx_requests_total{tool,status}`, `rexx_request_duration_seconds`, `rexx_errors_total{tool,code}`,
`rexx_jobs_*`, budget gauges; plus rexx's: `rexx_ms_per_frame{resolution_class}` (histogram, classes `720`, `1080`,
`1440`, `4k`), `rexx_peak_rss_bytes{tool}`, `rexx_cache_hits_total{kind}` (`render`, `asset`, `track`, `sim`),
`rexx_cache_evictions_total{kind}`, `rexx_cache_objects{kind}`, `rexx_cache_bytes{kind}`,
`rexx_diagnostics_total{code,severity}` (diagnostics returned on the run path's error envelope),
`rexx_quota_rejections_total{tool}`.

## The engine runner

Every engine run gets `--ffmpeg`, `--fonts`, `--library` (when configured), `--sim-dir <cache>/sim`, `--memory-mb`
(90 % of the tool's cgroup: 921 for check/convert, 1843 for frames, 5529 for render, 3686 for track), `--threads`
(renders only: the thread share), `--backend` (when `REXX_ENGINE_BACKEND` is set; `check`, `frames`, `render`) and
`--deadline` (the remaining tool timeout in whole seconds). The jail (`bwrap --unshare-all`, read-only root, the
scratch read-write, `/opt/rexx`, the sim cache, the library and the font pack read-only; on a GPU box the
`/dev/nvidia*` and `/dev/dri` nodes and the shader cache) kills the process group on cancel; a run with no event
for 60 s is killed (`500`); exit codes map to error classes ([30-diagnostics.md](30-diagnostics.md)). The engine's
stdout is the JSON-lines protocol (`diagnostic`, `progress`, `result`, `info` events; unknown events ignored; a line
over 8 MiB is a protocol error); its stderr's last 16 KiB are kept for escalated errors only.

## Caches on disk and in R2

| Cache | Where | Key | Lifetime |
|---|---|---|---|
| assets | `<REXX_CACHE_ROOT>/assets/{objects,meta,urls,tmp}` | SHA-256; URL index without the query string | LRU by atime (janitor; 40 GB in the design) |
| sims | `<REXX_CACHE_ROOT>/sim/<hash>.sim` | the simulation's input hash | LRU by mtime, 10 GB; trimmed after every adoption |
| GPU pipelines | `<REXX_CACHE_ROOT>/gpu-pipelines` | the driver's | the driver's |
| renders | R2 `rexx/cache/{index,objects,touch}/<key>` | [16-render-pipeline.md](16-render-pipeline.md) | 30 days after last use |
| tracks | R2 `rexx/cache/track/{index,objects,touch}/<key>` | [15-motion-track.md](15-motion-track.md) | 90 days |
| locked sims | R2 `rexx/cache/sim/<hash>.sim` (a copy beside the user's own) | the input hash | 180 days after the write |

The janitor sweeps ten minutes after boot and every 24 h, at most 5,000 removals per cache per sweep, and publishes
the cache gauges. Outputs under the caller's prefix are never removed by rexx.
