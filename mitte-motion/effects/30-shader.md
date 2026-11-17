# `utility.shader`: custom WGSL effects

`utility.shader` runs a WGSL function you write once per pixel of the layer, on the GPU. Everything an assistant needs to write one that compiles on the first try is on this page; [31-shader-gallery.md](31-shader-gallery.md) has seven checked, rendered shaders to copy from.

## The instance

```json
{ "id": "tint", "type": "utility.shader",
  "params": {
    "code": "fn effect(uv: vec2f, t: f32) -> vec4f {\n  let c = textureSampleLevel(input, samp, uv, 0.0);\n  return c * vec4f(params.tint.rgb, 1.0);\n}",
    "params": { "tint": { "type": "color", "default": "#FFB347" } },
    "inputs": [],
    "budgetMs": 0 } }
```

| Parameter | Type | Default | What it does |
|---|---|---|---|
| `code` | string | required | WGSL source defining `fn effect(uv: vec2f, t: f32) -> vec4f`, plus any helper functions, `const`s, structs and `var<private>` globals it needs. ≤ 64 KiB. Not animatable. |
| `params` | object | `{}` | Declared uniforms, `{ "<name>": { "type": "float" | "vec2" | "vec3" | "vec4" | "color", "default": <value> } }`, read in the code as `params.<name>`. Each `default` is animatable on its own (keys, drivers, expressions), by the path `effects.<id>.params.<name>.default`. ≤ 64 uniforms. |
| `inputs` | list of layer ids | `[]` | Up to 4 other layers of the comp, bound as `input1` … `input4` in list order (after their masks and effects; the `effects` source of spec 7 §7.6). `null` entries leave a slot empty. Each is read over its **own** rect through `uv`. |
| `budgetMs` | number ≥ 0 | 0 | Time cap of one dispatch; 0 = the job's budget (below). Animatable. |

Write uniform values under **`default`**, not `value`: the document parser treats `{ "type": …, "value": … }` as an animated value object and fails with `doc.unknown_field "type"`. The registry's doc string for `params` (the catalogue row in [91-catalogue-utility.md](91-catalogue-utility.md)) says the same.

A uniform may also be declared bare, typed by its shape: `"speed": 0.4` (float), `"dir": [1, -1]` (vec2), `"p": [0, 0, 1]` (vec3), `"k": [0, 0, 0, 1]` (vec4), `"c": "#FF0000"` (color). The object form is the one to use when the value animates.

## What your code sees

The engine wraps your source in a prologue and an epilogue; you never write bindings or an entry point. The prologue, exactly:

```wgsl
struct RexxFrame { size: vec2<f32>, t: f32, fps: f32, frame: f32, inputs: f32, pad0: f32, pad1: f32 }
@group(0) @binding(0) var<uniform> rexx: RexxFrame;
struct RexxUniforms { <name>: <wgsl type>, ... }            // only when `params` declares uniforms
@group(0) @binding(1) var<uniform> params: RexxUniforms;    // only then
@group(0) @binding(2) var rexx_out: texture_storage_2d<rgba16float | rgba32float, write>;
@group(0) @binding(3) var input: texture_2d<f32>;
@group(0) @binding(4) var input1: texture_2d<f32>;          // one per entry of `inputs`, up to input4 at binding 7
@group(0) @binding(8) var samp: sampler;
```

and the epilogue, a compute entry point `rexx_main` with 16 × 16 workgroups, one invocation per output pixel, that calls `effect(uv, rexx.t)` with `uv` at the pixel's centre over the layer's rect (`(pixel + 0.5) / rexx.size`) and stores the result with non-finite components zeroed.

| Name | Type | Meaning |
|---|---|---|
| `uv` (argument) | `vec2f` | 0–1 across the layer's logical rect (the running rect of the effect chain, not the comp), pixel centres, y down. |
| `t` (argument) | `f32` | The layer time in seconds (= `rexx.t`). |
| `rexx.size` | `vec2f` | The rect's size in pixels at the effect's resolution. `uv * rexx.size` is the pixel position. |
| `rexx.t`, `rexx.fps`, `rexx.frame` | `f32` | Time, the comp's frame rate, the frame index (frames are keyed by `t`; `frame` is the job's index). |
| `rexx.inputs` | `f32` | How many `inputs` were declared. |
| `params.<name>` | `f32`, `vec2<f32>`, `vec3<f32>`, `vec4<f32>` | Your uniforms (`color` is a `vec4<f32>`, straight RGBA in the comp's working space, scene-linear by default, alpha in `.a`). |
| `input` | `texture_2d<f32>` | The layer so far: premultiplied linear RGBA. |
| `input1` … `input4` | `texture_2d<f32>` | The declared layers, premultiplied linear RGBA, each over its own rect (uv 0–1 spans that layer, whatever its size or position). An empty slot is a 1 × 1 transparent texture. |
| `samp` | `sampler` | Bilinear with clamp-to-edge where the device filters f32 textures (the fleet and lavapipe do), nearest otherwise. |

Sampling: **`textureSampleLevel(input, samp, uv, 0.0)`**, never `textureSample` (a compute stage has no derivatives; the sandbox reports it with that hint). `textureLoad(input, vec2i(uv * rexx.size), 0)` reads an exact texel. `textureDimensions(input)` works.

Colour contract: in and out are **premultiplied**, linear light. To tint keep alpha and scale rgb (`c * vec4f(tint.rgb, 1.0)`); to fade scale all four channels; to recolour from straight values multiply rgb by alpha before returning; to mask, multiply all four channels by the mask's alpha; keep `rgb ≤ a` or the compositor sees "additive" colour. The output rect is the input rect (the effect never grows the layer); a `uv` outside 0–1 samples the clamped edge.

## The sandbox

The whole module is parsed and validated by naga on every box (the CPU included) before a frame is rendered. Rules:

| Rule | On violation |
|---|---|
| Define `fn effect(uv: vec2f, t: f32) -> vec4f` with exactly that shape (`vec2<f32>`, `f32` → `vec4<f32>`). | `effect.shader_invalid`: "`effect` must be `fn effect(uv: vec2f, t: f32) -> vec4f` …" |
| No bindings of your own (`@group`/`@binding`), no storage buffers (`var<storage>`), no workgroup memory (`var<workgroup>`), no atomics, binding arrays or ray queries. `var<private>` globals and `const` are fine. | `effect.shader_invalid` naming the variable. |
| No entry point of your own (`@compute`, `@vertex`, `@fragment`). | `effect.shader_invalid`: "declares an entry point …". |
| No `textureStore` (the engine writes the output), no `discard`, no barriers or subgroup operations. | `effect.shader_invalid` with the line. |
| Every loop has a constant bound of at most 4,096 trips: one local counter (`var i = 0`, or `0u`) starting at a constant, changing by one constant step per trip (in the `for` update, or as the last statement of a `while` body with no `continue`), compared with a constant (`i < N`, `<=`, `>`, `>=`, `!=`), written nowhere else. `const N` expressions and integer arithmetic of constants count as constants; `break` inside is fine; nested loops are each held to the cap. | `effect.shader_invalid`: "a loop needs a constant bound of at most 4096 trips: `for (var i = 0; i < N; i++)` with constant `N` (why…)" or "the loop runs 5000 times; the cap is 4096". |
| Source ≤ 64 KiB; ≤ 64 uniforms; uniform names are WGSL identifiers (letters, digits, `_`; not starting with a digit; not `_` or `__…`; not `rexx`, `params`, `input`, `input1`…`input4`, `samp`, `rexx_out`); ≤ 4 inputs. | `effect.shader_invalid` at `params/params` or `params/inputs`. |
| Anything naga rejects (a type error, an unknown name, a missing `return`). | `effect.shader_invalid` with naga's message and the 1-based line in your `code`. |

Diagnostics are reported at `/comps/<comp>/layers/<i>/effects/<j>/params/code` (or `/params`, `/inputs`), as an **error** from `motion.check` (the document does not render) and as a warning at render time (the effect is skipped). Example:

```
error effect.shader_invalid /comps/main/layers/0/effects/0/params/code:
  Entry point rexx_main at Compute is invalid: Uses operations forbidden at this stage
  (a compute kernel has no derivatives: `textureSample` is `textureSampleLevel(input, samp, uv, 0.0)` here).
```

Compiled modules are cached by source hash: a document re-validates its shader at every check and frame for the cost of a hash, and the device keeps one pipeline per source and output format.

## CPU boxes, the budget, limits

- **GPU only.** On the CPU backend (a job the backend decision puts on the CPU, a box without an adapter, `--backend cpu`) the effect is skipped with `effect.requires_gpu` and the layer passes through unshaded; nothing else changes. `motion.check` reports `estimate.requiresGpu: true` for a document with a shader and warns `effect.requires_gpu` when the chosen backend is `cpu`; the service routes `backend: gpu` jobs to the GPU pool. Check a shader document with `--backend gpu` to see it as the GPU pool will.
- **Time budget.** One dispatch may take `budgetMs`; 0 means the job's budget: 50 ms of device time on a hardware adapter with timestamp queries, 10 × 50 ms of wall clock (dispatch plus readback) without them, and **no budget on a software adapter** (lavapipe runs the kernel on the CPU, so its time is the box's load). Past the budget: `effect.shader_timeout` (warning, the message gives the time and the clock used) and the layer renders unshaded for that frame. A dispatch that never finishes (nested loops whose trips multiply into hours) hits the job's readback deadline: `render.gpu_lost`, the device is retired and the service re-runs the job on the CPU (where the shader is skipped).
- **Determinism.** Across GPU models the pixels are within the shader fidelity tolerance, not bit-exact; the shader golden is blessed on the GPU backend. Do not rely on a shader for something that must be byte-identical across boxes.
- **With other effects.** A stack mixing device-lowered effects and a shader runs on the CPU with the shader through the device seam (readback per shader); fine, just slower. A shader after a backdrop effect is impossible (the backdrop effect must be last).
- **Export.** After Effects export renders the layer to a precomp clip; Lottie drops or rasterizes it like any effect.

## Writing one that works first time

1. Start from the gallery; keep `fn effect(uv: vec2f, t: f32) -> vec4f` verbatim.
2. Sample with `textureSampleLevel(input, samp, uv, 0.0)`.
3. Put every number you may want to animate in `params` as `{ "type", "default" }`; read `params.<name>`.
4. Loops: `for (var i = 0; i < 8; i++) { … }` with a literal or `const` bound.
5. Return premultiplied RGBA; if you built straight colour, multiply rgb by alpha.
6. Use `rexx.size` for aspect-correct distances: `let p = (uv - 0.5) * vec2f(rexx.size.x / rexx.size.y, 1.0);`.
7. Run `motion.check` (or `rexx-engine check --backend gpu`) and read any `effect.shader_invalid` message; the line number is in your `code`.
8. Remember the layer's rect is what `uv` spans: on a text layer that is the ink box plus a 1 px halo, not the comp; put a full-frame shader on a comp-sized solid or an adjustment layer.
