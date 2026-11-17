# Transitions as components

The engine has a built-in transition catalogue (`cut`, `crossfade`, `fadeThrough`, `push`, `slide`, `cover`, `reveal`, `wipe`, `maskWipe`, `shapeReveal`, `zoom`, `whip`, `blurDissolve`, `glitch`, `lightLeak`, `filmBurn`, `morph`; spec 3 §3.8.3, the layers area) and the library ships **14 transition components**: ordinary components with two required slots `a` (the outgoing picture) and `b` (the incoming one), a canvas of `["100%", "100%"]` and a duration of `$props.dur`. They can be used in three ways. Source: `passes/components.rs::library_transition`, `passes/transitions.rs`; spec 3 §3.8.3 (`<library ref>` row), 12 §12.6.4.

## 1. In a scene sequence

```json
{ "size": [1920, 1080], "fps": 30, "duration": "auto",
  "scenes": [
    { "comp": "one", "dur": 3 },
    { "transition": { "type": "mitte/transition.glass-swipe@1", "dur": 1.0, "props": { "tint": "#FFFFFF10", "frost": 6 } } },
    { "comp": "two", "dur": 3 },
    { "transition": { "type": "mitte/transition.iris@1", "dur": 0.8, "props": { "center": ["30%", "40%"], "thickness": 24 } } },
    { "comp": "three", "dur": 3 } ] }
```

`type` is the library reference, `dur` the span *d* (default `$theme.motion.dur.transition`), `props` the component's params (`dur` is set from *d* automatically). The components pass turns it into an instance `scene.<k>.transition` (`in` = the cut time t₀, `out` = t₀ + d) whose slot `a` holds a comp layer of the outgoing scene and slot `b` one of the incoming scene, each offset so the scenes keep running inside the transition (`scene.<k>.transition.slot.a/b` comps of the host's duration with `offset`). The outgoing scene layer ends at t₀ and the incoming one starts at t₀ + d, so for the span only the component draws (verified: `scene.0` out 2.5, `scene.1` in 3.5 around a 1 s transition at 2.5). The resolved versions land in `stats.library`.

Fallbacks, each an **info** `effect.unavailable` "Library transition "…" is not available in this release; a crossfade was used.": the type is not a library component, or has no slots `a` and `b` (`mitte/lower-third.bar@1`), or a scene's timing is not a plain number. A crossfade of *d* overlaps the two scenes instead.

## 2. Instanced by hand between two layers

```json
{ "id": "shotA", "type": "solid", "color": "#1D2B53", "out": 1.5 },
{ "id": "shotB", "type": "solid", "color": "#7E2553", "in": 2.3 },
{ "id": "tx", "type": "component", "use": "mitte/transition.wipe@1", "in": 1.5,
  "props": { "dur": 0.8, "angle": 120, "bar": 120, "slant": -20 },
  "slots": { "a": [ { "id": "a1", "type": "solid", "color": "#1D2B53" } ],
             "b": [ { "id": "b1", "type": "solid", "color": "#7E2553" } ] } }
```

Give the instance `in` = the cut time and `props.dur` = the span; end the outgoing layers at `in` and start the incoming ones at `in + dur`; put copies of (or precomps of) the two pictures in the slots. The slot content is positioned in the parent frame's pixels (slots are `100%` of the parent, `fit: cover`). The library's own examples do this with two `image` layers and the transition between them (`transition.push.examples.json`). A `transitionIn`/`transitionOut` on a layer may name a library transition too (`"transitionIn": { "type": "mitte/transition.push@1", "dur": 0.6, "props": { … } }`): the engine instances it over the span above the layer (`<layer>.transitionIn`), with the layer in slot `b` and nothing in `a`, so it reveals the layer over whatever is below; a `transitionOut` is the same played backwards (the instance has `stretch: -100`), so it hides the layer the way the component reveals one; the layer itself starts at the transition's end (in) or ends at its start (out), and its tweens play in the slot copy. This needs plain-number `in`/`out` on the layer and no `matte` on it; otherwise it falls back to a crossfade with the `effect.unavailable` info.

## 3. As building blocks of your own transition

Write a component with slots `a` and `b`, `size ["100%", "100%"]`, `duration: "$props.dur"` (or `"auto"`), a `dur` param (default `$theme.motion.dur.transition`), and layers that reveal `b` over `a`: an alpha track matte riding a null (`transition.wipe`, `.iris`, `.glass-swipe`), a cut at `{{$props.dur / 2}}` under cover (`transition.shape`, `.stripes`: `a` slot `out` and `b` slot `in` at the midpoint), or both slots moving (`transition.push`, `.whip`, `.zoom`). Keys use `"t": "$props.dur"` and `"{{$props.dur * 0.5}}"` so the look scales with the span; sizes use multiples of `$theme.space.9` (0.3 × the shorter side) so one definition covers 16:9 and 9:16. `04-components-writing.md` has the general rules; `transition.wipe`'s file is the clearest model (a null `rig` rotated by `angle`, a `front` null whose position is keyed from −3.9 to +3.9 shorter-sides, a `matte` rect parented to it, `b` matted by it, two bars with `enabled: "{{$props.bar > 0}}"` and `motionBlur: true`).

## The 14 shipped transition components

All take slots `a` and `b` (required, `100%`, `fit: cover`). Full params and notes in `91-components-transitions.md`.

| `mitte/…@1` | `duration` | Params (default, range) | Look |
|---|---|---|---|
| `transition.push` | `$props.dur` | `travel` `["-100%", 0]`, `dur` `$theme.motion.dur.transition` (0.15–2) | `a` slides out along `travel`, `b` in from the opposite side, edge to edge |
| `transition.whip` | `$props.dur` | `travel` `["-100%", 0]`, `angle` 90 (0–360), `blur` 120 (0–400), `dur` (0.15–2) | push with a quartic in-out, directional blur peaking at the cut, 360° shutter motion blur |
| `transition.zoom` | `$props.dur` | `amount` 1.4 (1.05–3), `blur` 16 (0–80), `dur` (0.15–2) | `a` scales up, blurs, fades; `b` grows from 1/amount |
| `transition.mask-wipe` | `$props.dur` | `center` `["50%", "50%"]`, `feather` 0 (0–200), `dur` (0.15–2) | `b` through a growing ellipse (circle only; the other shapes are the built-in `maskWipe`) |
| `transition.shape-wipe` | `auto` | `color` accent, `color2` `palette.1`, `center`, `dur` (0.2–2) | two rounded squares scale up from `center`; `b` inside the second |
| `transition.shape` | `auto` | `start` `["-80%", "50%"]`, `travel` `["260%", 0]`, `color`, `color2`, `radius` 240 (0–1200), `skew` −12 (−45–45), `dur` (0.2–2) | a 2400 px rounded rectangle sweeps across, cut at the midpoint, a trailing shape follows |
| `transition.wipe` | `$props.dur` | `dur` 0.8 (0.25–3), `angle` 0 (−180–180), `accent`, `second` fg, `bar` 56 (0–400), `slant` 12 (−45–45) | slanted wipe at any angle behind an accent bar and a thin trailing bar |
| `transition.iris` | `$props.dur` | `dur` 0.9 (0.3–3), `center`, `ring` accent, `thickness` 18 (0–120), `ease` `power2.inOut` | a circle opens from a point led by an accent ring; `b` settles from a slight zoom |
| `transition.stripes` | `$props.dur` | `dur` 1.0 (0.4–3), `count` 5 (2–12), `color` accent, `color2` fg, `spread` 0.18 (0–0.6) | two-colour bands interlock from opposite sides, cut underneath, slide away |
| `transition.glitch` | `$props.dur` | `dur` 0.6 (0.2–2), `amount` 70, `shift` 60 (0–300), `split` 14 (0–60), `jitter` 24 (0–120), `blocks` false, `seed` 7 | slice displacement and RGB split (`stylize.glitch`, `stylize.rgbSplit`) peak at a hard cut with held jitter frames |
| `transition.light-leak` | `$props.dur` | `dur` 1.2 (0.4–4), `intensity` 95 (20–100), `color` `#FF6A1F`, `hot` `#FFE0A3`, `tint` accent, `side` left \| right, `push` 4 (0–20) | nests `mitte/light-leak@1` over a push-in; `b` dissolves in under the peak |
| `transition.glass-swipe` | `$props.dur` | `width` 420 (120–1600), `radius` 140 (0–800), `refraction` 1.5 (1–3), `thickness` 300 (0–512), `dispersion` 0.03 (0–0.2), `frost` 10 (0–60), `tint` `#FFFFFF05`, `dur` (0.3–3) | a liquid-glass pane (`distort.glass`) sweeps left to right; `b` is revealed under its centre |
| `transition.glass-lens` | `$props.dur` | `dur` 1.0 (0.4–3), `center`, `refraction` 1.6 (1–3), `thickness` 260 (0–512), `dispersion` 0.04 (0–0.2), `frost` 4 (0–60) | a glass lens opens from a point; `b` inside it |

Lottie export: `push`, `whip` (minus motion blur), `zoom`, `mask-wipe`, `shape-wipe`, `shape`, `wipe` (minus motion blur), `iris`, `stripes` (minus motion blur) and `light-leak` export as shapes, mattes and keys; `glitch`, `glass-swipe` and `glass-lens` lose their effect layers and keep the cut or reveal (`library/README.md`).

Where the built-in `lightLeak` and `filmBurn` transition types draw their overlay: they instance `mitte/light-leak@1` / `mitte/film-burn@1` above the scenes (`scene.<k>.overlay`), with `duration` = max(d, 0.6) (a shorter d stretches the instance), `color`, `intensity × 100` and `dir: "right"` → `side: "right"`; a one-sided `transitionIn`/`Out` draws it only when the layer's `in` and `out` are plain times.

A library type that cannot be instanced (a layer's one-sided `transitionIn`/`transitionOut`) falls back to a crossfade with the warning `effect.unavailable`, as spec 3 §3.8.3 says.

Worked example (checked): `examples/concepts/07-transitions.motion.json` (three scenes joined by `glass-swipe` and `iris`, and a second comp `byHand` with `transition.wipe` instanced between two solids).
