# 00 · The rexx service and the `motion.*` tools

rexx is mitte's motion graphics engine and service. A **motion document** (one JSON object, `"motion": 1`) goes in;
video, stills, converted files or track data come out. The service (binary `rexx`, port 7200) wraps the engine
(binary `rexx-engine`) as five tools on the fleet tool-service contract. Sources: `service/src/tools/*.rs` (the
registry entries), `service/src/{api,boot,config,shared,engine,cache,chunked,quota,pricing}.rs`,
`docs/proposal/06-service-api.md`, `docs/proposal/03-architecture.md`.

The assistant sees the tools with underscores (`motion_check`); this folder writes them with dots. The input is the
same JSON object either way.

## The five tools

| Tool | What it does | Runs as | Cost | Max concurrent | Timeout | Sandbox / cgroup | Output asset type | Price |
|---|---|---|---|---|---|---|---|---|
| `motion.check` | validate, normalize, lint, estimate; no pixels | sync | 1 | 8 | 60 s | `local`, 1 CPU / 1 GiB / 256 pids | none (a file only with `canonical: "url"`) | free |
| `motion.frames` | stills at times or key moments, or one contact sheet | sync | 2 | 2 | 120 s | `local`, 4 CPU / 2 GiB | `image` | $0.002 per cell |
| `motion.render` | video or image files, one per variant | **job** | 4 | 2 | 20 min | `local`, 4 CPU / 6 GiB | `video` | base + MB + minutes |
| `motion.convert` | export to canonical/Lottie/dotLottie/AE script/camera path; import Lottie/dotLottie/SVG | sync | 1 | 4 | 120 s | `local`, 1 CPU / 1 GiB | `text` | free |
| `motion.track` | follow points, planes, masks, camera shake, the camera in 3D, a face; returns a track file | **job** (`sync: false`; short classic tracks are admitted on `/v1/run`) | 2 | 2 | 10 min | `local`, 4 CPU / 4 GiB | `text` | free under 10 s of footage, else $0.10 per footage minute |

"Runs as" is the registry's `sync` flag, which mitte's node list exports as `node_json.sync`: a sync tool settles in
the assistant's turn on `POST /v1/run`; a job tool is submitted to `POST /v1/jobs` and polled. Any tool may be sent to
either endpoint; the admission gate (below) decides whether a long run is refused on the sync path.

## The workflow

1. Read this skill: the `language` pages for the document, `library/90-catalogue.md` for the only source of valid
   `mitte/…@n` references, `30-diagnostics.md` for the meaning of a diagnostic.
3. `motion.check`: fix every `error`, weigh every `warning`, read the `estimate` and the timing sheet. A document that
   passes check never fails a render on a limit (the service passes its caps to the engine).
4. `motion.frames`: look before rendering (`auto` + `sheet` + `trails` for a review; `safe_overlay` for platform UI).
5. `motion.render`: every variant the user needs in one call. An unchanged document is a cache hit.
6. `motion.convert` for Lottie, dotLottie, an After Effects script, a camera path, or to import an SVG/Lottie.
   `motion.track` before pinning graphics to footage.

## HTTP surface

Base URL in production: `https://rexx.mitte.ai` (behind a load balancer whose idle timeout is 300 s; the service's
own request timeout is 6 min). Everything is JSON; every response carries `X-Request-ID` (sent or generated).

| Route | Auth | Purpose |
|---|---|---|
| `POST /v1/run` | JWT | run a tool synchronously: `{"tool": "motion.check", "input": {…}}` |
| `POST /v1/jobs` | JWT | submit the same body as a job; answers `202` with the job |
| `GET /v1/jobs/{id}` | JWT | poll a job (progress merged in while it runs) |
| `DELETE /v1/jobs/{id}` | JWT | cancel: kills the engine process group (ffmpeg with it) |
| `GET /v1/status` | JWT | `{status, version, jobs: {pending, in_progress}, engine: {…}}` |
| `GET /v1/registry`, `GET /v1/registry/{name}` | public | every tool with schema, instructions, examples (the dump in [90-schemas.md](90-schemas.md)) |
| `GET /v1/schema/motion-1.json` | public | the full document JSON Schema (`application/schema+json`), generated from the engine types |
| `GET /healthz`, `GET /readyz`, `GET /metrics` | public | health, readiness, Prometheus ([60-service-config.md](60-service-config.md)) |
| `/`, `/playground`, `/playground/token`, `/playground/docs`, `/playground/sync`, `/login`, `/logout` | mitte OAuth | the browser playground (default tool `motion.check`) |

**Auth.** `Authorization: Bearer <JWT>`, HS256 with `JWT_SIGNING_SECRET`, claims `sub`, `tenant_id` (else `sub`),
`iat`, `exp`. `rexx --mint-jwt --sub dev --tenant <t> --ttl 24h` mints one locally. `X-Tenant-Id` overrides the
tenant for the request. mitte's tool layer sends tenants as `socket-service:<userID>`. While `REXX_TENANTS` is set
(internal testing), tenants not in the list get `403 forbidden` on `motion.*` submits.

**Body limit.** `REXX_MAX_DOC_BYTES` (default 1 MiB) plus 1 MiB of envelope; the tenant gate reads at most 4 MiB.
Larger documents go by `doc_url`.

### Run response (`POST /v1/run`)

```jsonc
{
  "output": { "files": { "default": "https://media.mitte.ai/u/<uid>/rexx/render/<request id>/default.mp4" },
              "data": { "…": "tool-specific, see each tool page" } },
  "trace": { "request_id": "…", "tool": "motion.render", "duration_ms": 10100, "success": true, "steps": [ … ] },
  "usage": { "wall_ms": 10100, "bytes_in": 31457280 },
  "billing": { "price": { "amount": 0.14, "currency": "USD" } }
}
```

`files` is a `{label: url}` map when every file has a unique label (`motion.render`: `<variant>`, `<variant>-poster`;
`motion.track`: `track`, `preview`; `motion.convert` with extra files), else a plain list of URLs (`motion.frames`,
`motion.check` with `canonical: "url"`, `motion.convert` with one file). Files live under the caller's prefix
`u/<uid>/rexx/<tool>/<request id>/<name>` on the public media host; the `<uid>` is the tenant with its
`socket-service:` prefix stripped. `billing` is lifted from `data.billing`, so both carry the same price.

### Error response

```jsonc
{ "error": { "code": "bad_request", "message": "bad_request: the document is invalid: /comps/main/layers/2/type: …",
             "data": { "diagnostics": [ { "severity": "error", "code": "doc.enum", "path": "…", "message": "…", "hint": "…" } ] } },
  "trace": { … "success": false, "error": "…" }, "usage": { … } }
```

| HTTP | `error.code` | When |
|---|---|---|
| 400 | `bad_request` | a malformed input (neither or both of `doc`/`doc_url`, invalid JSON, bad enum, a negative time, …); a document with errors on `frames`, `render`, `convert` (the first three diagnostics in the message, all of them in `error.data.diagnostics`, on `/v1/run` only); an asset that cannot be used (`asset.*` prefix in the message); an output the box cannot write (`output.*` diagnostic) |
| 401 | `unauthorized` | missing or invalid JWT |
| 403 | `forbidden` | tenant not in `REXX_TENANTS` |
| 404 | `not_found` | unknown tool or job id |
| 413 | `too_large` | a cap: document bytes, variants, frames, duration, fps, size, stills, seeds, footage, track items; **an estimate above the sync budget** ("… above the 4m0s sync budget; submit via POST /v1/jobs") or the job cap |
| 429 | `rate_limited` | per-tenant per-minute class limit; `Retry-After: 5` |
| 429 | `overloaded` | a daily quota: "daily render (minutes) quota of 60 reached; resets at 2026-10-13T00:00:00Z" |
| 502 | `upstream_failure` | object storage or a chunk peer failed |
| 503 | `overloaded` | budget or per-tool slot unavailable, job queue full (`REXX_JOBS_MAX_PENDING`, 32), draining, the engine missing on the box |
| 504 | `timeout` | the run outlived its tool timeout (the engine is killed) |
| 500 | `internal` | engine crash (exit 5), stalled run (no event for 60 s), protocol error; escalated |

Job errors (`GET /v1/jobs/{id}` with `status: "error"`) carry `error: {code, message}` without `data.diagnostics`
(the side map is drained on the run path only); check the document with `motion.check` first.

### Jobs

```jsonc
// POST /v1/jobs → 202
{ "id": "…", "tool": "motion.render", "status": "pending", "created_at": "2026-10-12T05:00:00Z" }
// GET /v1/jobs/{id} while running
{ "id": "…", "tool": "motion.render", "status": "in_progress", "created_at": "…", "started_at": "…",
  "progress": { "stage": "render", "frame": 120, "frames": 900, "fraction": 0.133 } }
// done
{ "id": "…", "status": "done", "settled_at": "…", "wall_ms": 10100, "bytes_in": 31457280,
  "output": { "files": { … }, "data": { … } }, "billing": { "price": { "amount": 0.14, "currency": "USD" } } }
```

Statuses: `pending`, `in_progress`, `done`, `error`, `stopping`, `stopped`. `attempts` appears after a recovery re-run
(`REXX_JOBS_MAX_ATTEMPTS`, 2): a retried render produces the same bytes. `progress.frames` counts over all variants;
`stage` is `render` (or `frames`, `track`). Jobs are kept `REXX_JOBS_RETENTION` (168 h) in the SQLite store
(`REXX_DB_PATH`). A render under `motion.render` runs its own `--deadline` from the tool timeout, so a job never
outlives 20 min.

## Admission: sync budget, job cap, box budget

- Every `motion.render` call runs `check` per variant first; the engine's `estimate.renderSeconds` (one box, all
  threads) is scaled to the render's thread share (`× box_threads / share_threads`; 2 of 4 on a ccx23, so about ×2).
- On `/v1/run` the scaled estimate must be ≤ `REXX_SYNC_BUDGET` (240 s), else `413 too_large` "… submit via POST
  /v1/jobs". On `/v1/jobs` it must be ≤ `REXX_JOB_TIMEOUT` (20 min), else `413` "… above the 20m0s job cap; shorten or
  split the document". A chunked variant ([16-render-pipeline.md](16-render-pipeline.md)) is admitted at its estimate
  divided by the number of workers.
- `motion.track` has no engine estimate: 8 s of box time per second of footage (unknown footage counts as the 120 s
  cap) must fit the sync budget; `type: "camera"` is refused on `/v1/run` ("camera solves run as jobs").
- The box budget is `REXX_BUDGET` (default 11): two renders (4 each) plus one `frames` (2) and one `check` (1). A
  quarter (2) is reserved for the sync lane. Over budget the call waits, then `503 overloaded`.
- Render threads: `--threads ceil(box_threads × cost / budget)` (2 on a 4-vCPU box); `check`, `frames`, `convert`
  and `track` run at the engine's own count inside their cgroups.

## Rate limits and quotas

Per tenant per minute (`429 rate_limited`): class `data` (`motion.check`, `motion.convert`) 300;
`frames` 60; `render` (`motion.render`, `motion.track`) 30.

Per tenant per UTC day (`429 overloaded`, reset at the next midnight; charged before the run, so a run that fails
late still counts):

| Class | Tool | Unit | Default | Env |
|---|---|---|---|---|
| `check` | `motion.check` | calls | 2,000 | `REXX_QUOTA_CHECK` |
| `convert` | `motion.convert` | calls | 500 | `REXX_QUOTA_CONVERT` |
| `frames` | `motion.frames` | cells (times × seeds) | 2,000 | `REXX_QUOTA_FRAMES` |
| `track_seconds` | `motion.track` | footage seconds, rounded up | 600 | `REXX_QUOTA_TRACK_SECONDS` |
| `render_minutes` | `motion.render` | rendered minutes over all variants, rounded up | 60 | `REXX_QUOTA_RENDER_MINUTES` |

A cap of 0 disables the class. Counters live in `REXX_QUOTA_DB_PATH` (default `quota.db` next to the jobs database,
else memory).

## Pricing

`data.billing` and the envelope's `billing` carry `{ "price": { "amount": <USD, 6 decimals>, "currency": "USD" } }`.
Free tools return an explicit `0`.

| Tool | Price (defaults; `REXX_PRICE_*`) |
|---|---|
| `motion.check`, `motion.convert` | 0 |
| `motion.frames` | cells × `REXX_PRICE_PER_FRAME_USD` (0.002); a 12-cell sheet is $0.024 |
| `motion.render` | `REXX_PRICE_BASE_USD` (0.05) + input MB (decimal, every materialized asset incl. library files) × `REXX_PRICE_PER_MB_USD` (0.0001) + rendered seconds over all variants / 60 × `REXX_PRICE_PER_MINUTE_USD` (0.35); every variant a cache hit: the base only; a failed render: nothing (but the render-minutes quota was charged) |
| `motion.track` | 0 under 10 s of footage or on a cache hit; else footage seconds / 60 × `REXX_PRICE_TRACK_PER_MINUTE_USD` (0.10) |

## Determinism and caching in one paragraph

The same canonical document, assets, engine, fonts, library, ffmpeg build, variant, output settings, range, backend
and encoder give identical bytes, so renders and tracks are cached by content (R2, `rexx/cache/…`; render entries
expire 30 days after last use, tracks 90, content-keyed sim copies 180). A hit copies the object into the caller's
prefix server-side and reports `cache_hit: true`. The physics sim cache is box-local (`<REXX_CACHE_ROOT>/sim`, 10 GB
LRU). Details: [16-render-pipeline.md](16-render-pipeline.md).

## What is where in this folder

| Page | Covers |
|---|---|
| [01-documents-and-assets.md](01-documents-and-assets.md) | `doc` vs `doc_url`, `library:` URIs, `data`, variants, how assets are fetched and refused |
| [11-motion-check.md](11-motion-check.md) … [15-motion-track.md](15-motion-track.md) | one page per tool: every input and output field, every error |
| [16-render-pipeline.md](16-render-pipeline.md) | the estimate, backends, the render cache key, chunked rendering, HDR, NVENC, encoders |
| [30-diagnostics.md](30-diagnostics.md), [31-diagnostics-2.md](31-diagnostics-2.md), [32-lint.md](32-lint.md), [33-codes-inventory.md](33-codes-inventory.md) | every diagnostic code with severity, trigger and fix |
| [40-limits.md](40-limits.md) | every limit, cap and budget in one table |
| [50-engine-cli.md](50-engine-cli.md) | `rexx-engine` subcommands, flags, event protocol, exit codes |
| [60-service-config.md](60-service-config.md) | `REXX_*` variables, `/healthz`, `/readyz`, `/v1/status`, `/metrics` |
| [90-schemas.md](90-schemas.md), [91-schema-check.md](91-schema-check.md) … [95-schema-track.md](95-schema-track.md) | the registry dump: schemas, instructions, fields, examples (generated) |
