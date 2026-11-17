# Shader gallery: seven checked, rendered `utility.shader` effects

Each is a complete document in `examples/shader-<name>.motion.json`, checked with `rexx-engine check --backend gpu` (0 errors) and rendered once on the GPU backend (`scripts/skills-effects-check-examples.sh --render`). Copy the `code` and the `params` declaration; the rules are in [30-shader.md](30-shader.md). Every shader keeps the output premultiplied.

## 1. Tint (`shader-tint`): a colour uniform, keyed

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let c = textureSampleLevel(input, samp, uv, 0.0);
  // premultiplied in, premultiplied out: scale rgb, keep alpha
  return c * vec4f(params.tint.rgb, 1.0);
}
```
```json
"params": { "tint": { "type": "color", "default": { "keys": [ { "t": 0, "v": "#FFB347", "ease": "sine.inOut" }, { "t": 3, "v": "#22D3EE" } ] } } }
```
A `color` uniform arrives straight, in the comp's working space, so multiplying premultiplied rgb by it is a valid tint. On a text layer `uv` spans the ink box.

## 2. Ripple (`shader-ripple`): displace the sample position

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let aspect = rexx.size.x / rexx.size.y;
  let p = (uv - 0.5) * vec2f(aspect, 1.0);
  let d = length(p);
  let wave = sin(d * params.frequency - t * params.speed) * params.amount;
  let dir = select(p / d, vec2f(0.0), d < 1e-4);
  let offset = dir * wave / vec2f(aspect, 1.0);
  return textureSampleLevel(input, samp, uv + offset, 0.0);
}
```
`amount` (float, keyed 0 → 0.02 → 0) is in uv units; `frequency` 40 and `speed` 6 are plain floats. Divide the offset back by the aspect so rings stay round. Samples past the edge clamp, so a ripple never reads transparency on a full-frame layer.

## 3. CRT (`shader-crt`): scanlines, barrel, phosphor triads, vignette

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let c = uv - 0.5;
  let r2 = dot(c, c);
  let q = 0.5 + c * (1.0 + params.curvature * r2);          // barrel
  var col = textureSampleLevel(input, samp, q, 0.0);
  let line = 0.5 + 0.5 * sin(q.y * params.lines * 6.2831853); // scanlines
  col *= 1.0 - params.strength * line;
  let px = i32(q.x * rexx.size.x) % 3;                        // triads
  var triad = vec3f(1.0);
  if (px == 0) { triad = vec3f(1.0, 0.7, 0.7); } else if (px == 1) { triad = vec3f(0.7, 1.0, 0.7); } else { triad = vec3f(0.7, 0.7, 1.0); }
  col = vec4f(col.rgb * triad, col.a);
  col *= 1.0 - smoothstep(0.3, 0.75, length(c));              // vignette
  let inside = step(0.0, q.x) * step(q.x, 1.0) * step(0.0, q.y) * step(q.y, 1.0);
  return col * inside;                                         // black outside the curved frame
}
```
Uniforms `curvature` 0.25, `lines` 270 (one dark line per two rows at 540 px), `strength` 0.35. `rexx.size` gives the pixel column for the triad.

## 4. Chromatic aberration (`shader-chromatic`): three samples, alpha kept honest

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let c = uv - 0.5;
  let shift = c * params.amount * dot(c, c) * 4.0;     // grows with the distance from the centre
  let r = textureSampleLevel(input, samp, uv + shift, 0.0);
  let g = textureSampleLevel(input, samp, uv, 0.0);
  let b = textureSampleLevel(input, samp, uv - shift, 0.0);
  let a = max(max(r.a, g.a), b.a);
  return vec4f(min(r.r, a), min(g.g, a), min(b.b, a), a);  // no channel above the alpha
}
```
`amount` keyed 0 → 0.06 → 0.02. When channels come from different positions their alphas differ; take the largest alpha and clamp each channel to it so the output stays premultiplied.

## 5. Two-input blend (`shader-blend`): `inputs` and `input1`

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let a = textureSampleLevel(input, samp, uv, 0.0);
  let b = textureSampleLevel(input1, samp, uv, 0.0);
  let k = smoothstep(params.mix - 0.1, params.mix + 0.1, uv.x * 0.7 + uv.y * 0.3);
  return mix(b, a, k);
}
```
```json
"inputs": ["plate"], "params": { "mix": { "type": "float", "default": { "keys": [ { "t": 0, "v": -0.2 }, { "t": 3, "v": 1.2 } ] } } }
```
`plate` is another layer of the comp (here a gradient solid; it may be hidden). `input1` is read over the plate's own rect, so `uv` lines up only when both layers have the same size; a plate with its own effects is read after them (its shader runs again as an input).

## 6. Time-driven noise (`shader-noise`): helpers, a bounded loop, a generator

```wgsl
fn hash(p: vec2f) -> f32 { return fract(sin(dot(p, vec2f(127.1, 311.7))) * 43758.5453); }
fn vnoise(p: vec2f) -> f32 {
  let i = floor(p); let f = fract(p); let u = f * f * (3.0 - 2.0 * f);
  let a = hash(i); let b = hash(i + vec2f(1.0, 0.0)); let c = hash(i + vec2f(0.0, 1.0)); let d = hash(i + vec2f(1.0, 1.0));
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
fn effect(uv: vec2f, t: f32) -> vec4f {
  let p = uv * vec2f(rexx.size.x / rexx.size.y, 1.0) * params.scale + vec2f(t * params.drift, 0.0);
  var v = 0.0; var amp = 0.5; var q = p;
  for (var i = 0; i < 4; i++) {            // a constant bound: the sandbox accepts it
    v += amp * vnoise(q + vec2f(0.0, t * 0.3));
    q *= 2.0; amp *= 0.5;
  }
  let col = mix(params.dark.rgb, params.light.rgb, v);
  return vec4f(col, 1.0);                  // opaque: straight equals premultiplied at alpha 1
}
```
Uniforms `scale` 4, `drift` 0.4, `dark`/`light` colours. The shader ignores `input` and acts as a generator over a solid. The loop bound must be a literal or `const`; `for (var i = 0; i < n; i++)` with `n` computed from `uv` is rejected.

## 7. Mask from a second layer (`shader-mask`): alpha of `input1`

```wgsl
fn effect(uv: vec2f, t: f32) -> vec4f {
  let c = textureSampleLevel(input, samp, uv, 0.0);
  let m = textureSampleLevel(input1, samp, uv, 0.0).a;   // the other layer's alpha
  let k = select(m, 1.0 - m, params.invert > 0.5);
  return c * k;                                            // every channel scaled: still premultiplied
}
```
```json
"inputs": ["holdout"], "params": { "invert": { "type": "float", "default": 0 } }
```
`holdout` is a hidden comp-sized solid with a keyed `generate.circle`; its alpha moves across the gradient. A boolean uniform is a `float` compared against 0.5 (there is no `bool` uniform type).

## What each example checks

| Example | Exercises |
|---|---|
| `shader-tint` | a `color` uniform with keys; a shader on a text layer (ink-box uv) |
| `shader-ripple` | keyed `float` uniform; aspect-correct geometry; sampling at offsets |
| `shader-crt` | `rexx.size`; integer ops; `if`/`else`; a shader after another effect in the stack |
| `shader-chromatic` | several samples; premultiplied alpha discipline |
| `shader-blend` | `inputs`; `input1`; `mix` of two layers |
| `shader-noise` | helper functions; a bounded `for`; a generator ignoring `input` |
| `shader-mask` | a hidden layer as a mask; `select` |

Rendering with `--render` writes one frame of each at 1.0 s under the chosen `--out` directory; on a CPU-only box `check` still validates the WGSL (the sandbox runs everywhere) and reports `effect.requires_gpu`.
