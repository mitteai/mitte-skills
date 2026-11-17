# 06. Transitions: `transitionIn` / `transitionOut`, scene sequences, the whole catalog

Scope: spec 3 §3.8 (authored form only). Transitions compile to ordinary keyframes, effects, masks, mattes and helper layers in canonical form, with ids under the transition (`scene.1.tw.push`, `scene.1.tw.leak`, `<layer>.transitionIn.overlay`), so canonical form shows exactly what a transition did. Generated tables: `Transition`, `Scene`, `Dir`, `Edge` in `92-schema-types-*.md`.

## 1. Layer transitions

```jsonc
{ "id": "card", "type": "comp", "comp": "card", "in": 2, "out": 6,
  "transitionIn":  { "type": "maskWipe", "shape": "circle", "dur": 0.6, "ease": "expo.out", "center": ["50%", "50%"] },
  "transitionOut": { "type": "push", "dir": "left", "dur": 0.5 } }
```

A one-sided transition reveals the layer over whatever is below it (`transitionIn`, starting at the layer's `in`) or hides it (`transitionOut`, ending at its `out`). Valid one-sided types: `cut`, `crossfade`, `slide`, `cover`, `wipe`, `maskWipe`, `shapeReveal`, `zoom`, `blurDissolve`, `glitch`, `lightLeak`, `filmBurn`. `push`, `reveal`, `fadeThrough`, `morph` need two scene layers and are `layer.transition_needs_pair` here. A `maskWipe` `center` in percent resolves against the layer's content bounds. A one-sided `lightLeak`/`filmBurn` draws its overlay only when the layer's `in` and `out` are plain times.

## 2. Scene sequences

```jsonc
"comps": { "main": {
  "size": [1920, 1080], "fps": 30, "duration": "auto",
  "scenes": [
    { "comp": "intro",    "dur": 3 },
    { "transition": { "type": "whip", "dir": "left", "dur": 0.4 } },
    { "comp": "features", "dur": 5 },
    { "transition": { "type": "lightLeak", "dur": 0.8, "variant": 2 } },
    { "comp": "outro",    "dur": 3, "offset": 0 }
  ],
  "layers": [ { "id": "music", "type": "audio", "asset": "music" } ]
} }
```

`scenes` lays scene comps end to end with a transition between consecutive scenes. It compiles to one `comp` layer per scene (ids `scene.0`, `scene.1`, …) inserted at the **bottom** of `layers`, so the comp's own layers (music, captions, a logo bug) sit above every scene. Each entry is either a scene (`comp`, `dur`, `offset`) or a transition (`{"transition": {…}}` on its own, between the two scenes it joins); an entry with both `comp` and `transition` is `doc.required`.

| Field | Notes |
|---|---|
| `comp` | the scene comp's id; its `size` must equal the root comp's (`layer.scene_size`); use collapsed comp layers inside a scene for other sizes |
| `dur` | the scene's length on the timeline; default the scene comp's `duration` |
| `offset` | optional: the scene comp's own time at the nominal start (for scene comps with handles, which start *d*/2 early) |
| `transition` | a transition object (§3) between the scene before and after it |
| comp `duration: "auto"` | the comp ends with the last scene; total length = the sum of the `dur`s whatever the transitions |

Timing: with scene *k*'s nominal start *s_k* (the sum of the previous `dur`s) and transitions of duration *d_in* / *d_out*, its layer gets `in = s_k − d_in/2`, `out = s_k + dur_k + d_out/2`, `offset = s_k`, `hold: "both"`: the two scenes overlap by *d* centred on the cut, and a scene comp exactly `dur` long holds its first and last frame during the overlaps.

## 3. The transition catalog

Common fields: `type`; `dur` (`$theme.motion.dur.transition`, else 0.5 s); `ease` (`$theme.ease.transition`, else `power3.inOut`); `dir` (`left`, `right`, `up`, `down`; default `left`). **A** is the outgoing scene layer, **B** the incoming one; a `transitionIn` has only B (A is whatever is below), a `transitionOut` only A. "Over the transition" is the span `[t0, t0 + dur]`.

| `type` | Extra fields (defaults) | Compiles to | Status (engine 0.1.48) |
|---|---|---|---|
| `cut` | — | no overlap; B starts where A ends | yes |
| `crossfade` | `alpha`: `cover` (default) \| `preserve` | B `opacity` 0 → 100; with `preserve` A 100 → 0 at the same time (for scenes with transparency: both fade against what is below) | yes |
| `fadeThrough` | `color` (`#000000`) | a solid of `color` above both: opacity 0 → 100 over the first half, 100 → 0 over the second; A ends and B starts at the midpoint | yes |
| `push` | `dir` | A `position` moves by one frame width (or height) in `dir`; B moves in from the opposite side; the same ease, so they stay edge to edge | yes |
| `slide` | `dir`, `shadow` (true) | B slides in from the side opposite `dir` over a static A; `shadow` adds a `dropShadow` style (opacity 40, size 40, distance 0) | yes |
| `cover` / `reveal` | `dir` | `cover` = slide; `reveal` = A slides out in `dir` uncovering a static B (B moved below A for the span) | yes |
| `wipe` | `dir`, `feather` (40), `angle` (from `dir`) | a `transition.linearWipe` effect on B, `completion` 100 → 0 | yes |
| `maskWipe` | `shape`: `circle` (default) \| `rect` \| `diamond` \| `iris` \| `diagonal` \| `star`; `center` (`["50%", "50%"]`); `feather` (0) | a mask on B growing from zero size at `center` to cover the frame (the radius to the farthest corner) | yes |
| `shapeReveal` | `shape`: `circle` \| `roundedRect` \| `blob` \| a shape layer id; `color` (`$theme.color.accent`); `layers` (2) | `layers` coloured shapes (theme colours) scale up in quick succession from `center` to fill the frame; B is revealed by the last one as an alpha matte | yes |
| `zoom` | `amount` (1.4), `blur` (16) | A `scale` 100 → 100 × amount with `blur` 0 → blur and `opacity` 100 → 0; B `scale` 100/amount → 100 with blur → 0 and opacity 0 → 100; motion blur forced on | yes |
| `whip` | `dir`, `blur` (120) | a push with `power4.inOut`, a `blur.directional` effect (`_whip`) on A and B whose `length` rises to `blur` at the midpoint and back, `motionBlur: true` on both with hold keys raising the comp's `shutterAngle` to 360° for the span; the cut at the midpoint under maximum blur | yes |
| `blurDissolve` | `blur` (40) | A blurs 0 → blur and fades out; B fades in while its blur goes blur → 0 | yes |
| `glitch` | `amount` (1), `seed` (0) | a `stylize.glitch` effect (`_glitch`) on A rising to the midpoint and on B falling after, hard cut at the midpoint, a few hold keys of position jitter | yes |
| `lightLeak` | `variant` (1), `color` (theme accent), `intensity` (1) | an instance of the library component `mitte/light-leak@1` above both over the span (id `scene.<k>.overlay` or `<layer>.transitionIn.overlay`/`.transitionOut.overlay`), props `duration` = *d* (at least 0.6 s; shorter stretches the instance), `color`, `intensity` × 100, `dir: "right"` → `side: "right"`; A cuts to B at the midpoint. Without the library component a screen-blended solid of `color` peaking at the midpoint stands in | yes (`variant` is not read) |
| `filmBurn` | `variant` (1) | as `lightLeak` with `mitte/film-burn@1` (additive); the stand-in solid uses `add` | yes (`variant` is not read) |
| `morph` | `match`: `[[aLayerId, bLayerId], …]` | specified: B's matched layers animate from A's matched layers' position, scale and path while the rest crossfades | **not built**: a crossfade with the warning `effect.unavailable` |
| a library reference | `props` | specified: `"type": "mitte/transition.glass-swipe@1"` instances a transition component with slots `a` and `b` | in `scenes`: instanced with the outgoing scene in slot `a` and the incoming one in `b` (`scene.<k>.transition`, [library/07](../library/07-transitions.md)); elsewhere (a layer's `transitionIn`/`transitionOut`) a crossfade with the warning `effect.unavailable` |

An unknown type is `doc.enum` with the list above as the hint.

> **Spec gap:** spec 3 §3.8.3 defines `morph` (P2); the engine compiles it to a crossfade with the warning `effect.unavailable` at the transition's `type`.

## 4. Examples

`examples/06-scenes.json`: a `duration: "auto"` scene sequence through every two-sided transition type that is built (`crossfade` with `preserve`, `fadeThrough`, `push`, `slide`, `reveal`, `wipe`, `maskWipe` with `star`, `shapeReveal`, `zoom`, `whip`, `blurDissolve`, `glitch`, `lightLeak`, `filmBurn`, `cut`), with a music layer above the scenes. `examples/06-layer-transitions.json`: `transitionIn`/`transitionOut` on individual layers with each one-sided type. Both check with 0 errors; `06-scenes.json` reports the expected `lint.missing_exit`-free result and a few `lint.expensive_effect` warnings on the blur and glow spans.
