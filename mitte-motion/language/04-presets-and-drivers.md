# 04. Presets (using, defining, every built-in), drivers, and the data bindings on keys

Scope: spec 2 §2.8 (presets, every built-in with its parameters as the engine defines them in `rexx-normalize/src/presets_builtin.rs`), §2.9 (drivers), spec 10 §10.8.5 (`keys.fromAudio`), spec 12 §12.4 (`keys` list binding). Generated tables: `PresetDef`, `PresetParam`, `PresetKind`, `WiggleDriver`, `NoiseDriver`, `OscillateDriver`, `SpringDriver`, `FollowDriver`, `AudioDriver`, `AudioMode`, `KeysBinding`, `FromAudio`, `FromAudioKeys` in `92-schema-types-*.md`.

## 1. Using a preset

```jsonc
{ "target": "title", "preset": "maskReveal", "props": { "dir": "up" }, "at": 0.3 }
{ "target": "title/words", "preset": "rise", "stagger": 0.06 }
{ "target": "logo", "preset": "popIn", "dur": 0.5, "ease": "back.out(2.5)" }
{ "target": "card", "preset": "mitte/kinetic.slam@1", "props": { "from": 300 } }      // a library preset
{ "target": "badge", "preset": "float", "repeat": -1 }                               // a loop preset for the layer's life
```

`dur` and `ease` on the tween override the preset's own; `stagger` applies to the preset's whole group of tweens per target; `props` fills the preset's params (`preset.param` on a bad value; `preset.unknown` on an unknown name). A preset's `kind` (`enter`, `exit`, `emphasis`, `loop`, `camera`) is what component params of type `preset` filter on.

## 2. Defining a preset

```jsonc
"presets": {
  "riseBlur": {
    "params": { "distance": { "type": "number", "default": 48 }, "blur": { "type": "number", "default": 16 } },
    "dur": "$theme.motion.dur.base",
    "ease": "$theme.ease.enter",
    "tweens": [ { "from": { "y": "+=$props.distance", "opacity": 0, "blur": "$props.blur" } } ]
  }
}
```

| Field | Notes |
|---|---|
| `kind` | `enter`, `exit`, `emphasis`, `loop`, `camera`: set on built-in and library presets (what component params of type `preset` filter on with their own `kind`). **Not accepted on a local preset definition** (`doc.unknown_field`). |
| `params` | map name → `{ type, default, description, values, min, max }` (a subset of component params, [13](13-components-themes-data.md) §3.2; `type` is `number`, `text`, `color`, `enum` with `values`, `boolean`, `vector`, `time`, `ease`); referenced as `$props.<name>` |
| `dur`, `ease` | defaults for the preset's tweens (`$theme` tokens allowed); the using tween's `dur`/`ease` override them |
| `tweens` | tweens without `target` (the preset's target, `$target`, is implied) unless they address a sub-part: `"$target/chars"`, `"$target.effects.glow"`. `at` is relative to the preset's start; `dur` and `at` may be percentages of the preset's effective duration (`"30%"`). |

Presets may use other presets; recursion is `preset.cycle`. Library presets: `"preset": "mitte/<name>@<major>"` (`kinetic.slam`, `kinetic.stomp`, `kinetic.flip`, `kinetic.stretch`, `ui.pop`, `ui.slide`, `ui.fade`, `editorial.rise`, `editorial.fade`; the catalogue is `library/90-catalogue.md`).

## 3. Every built-in preset

54 presets ship in the engine (`presets_builtin.rs`), in the definition format above. `dir` is `up`, `down`, `left`, `right`. Plain ones are tween lists; those marked *code* need measurement or structure and are completed by the presets pass.

**Enter** (default ease `$theme.ease.enter` unless noted)

| Preset | What it does | Params (default) | Notes |
|---|---|---|---|
| `fadeIn` | opacity 0 → current | — | |
| `rise` | from `y + distance`, opacity 0 | `distance` (40) | |
| `drop` | from `y − distance`, opacity 0 | `distance` (40) | |
| `slideIn` | from off-frame in `dir`, no fade | `dir` (left), `overshoot` (0) | code |
| `scaleIn` | scale `from` → current | `from` (0) | |
| `popIn` | scale 0 → current with `back.out(overshoot)`; opacity 0 → 100 over the first 30 % (`linear`) | `overshoot` (2) | |
| `blurIn` | `blur` `amount` → 0, opacity 0 → 100, scale 104 → 100 | `amount` (24) | adds a `_blur` effect |
| `maskReveal` | content slides in from behind an edge of its own bounds (an animated rect mask; bounds at `in`, ignoring animators). On text units: a per-unit `clip` animator | `dir` (up), `distance` (`"100%"`, text) | code |
| `wipeIn` | a `transition.linearWipe` reveal with a soft edge | `dir` (right), `feather` (60) | code |
| `drawOn` | the stroke draws along its path (`trimEnd` 0 → 100) | `from` (`start` \| `end` \| `center`) | code; shape layers with a stroke, else `preset.target_kind` |
| `typeOn` | characters appear one by one (hold, no fade); optional blinking cursor | `cps` (24), `cursor` (false) | code; ease `linear` |
| `scrambleIn` | each character cycles random glyphs of `chars` before settling (a `wiggly` selector on `characterOffset` under a keyed `range` selector) | `chars` (`"A-Z0-9"`), `cycles` (6) | code; ease `linear` |
| `trackIn` | tracking `from` → normal with fade (keys on `style.tracking`) | `from` (400) | |
| `flipIn` | 3D target: rotation X 90 → 0 around the bottom edge (`axis: y`: rotation Y around the left edge). 2D target: `scaleY` (or `scaleX`) 0 → 100 from the edge, no perspective; no diagnostic (`preset.needs_3d` is never raised) | `axis` (`x` \| `y`) | code |
| `growIn` | scale X (or Y) 0 → 100 from an edge | `from` (`left` \| `right` \| `top` \| `bottom` \| `center`) | code |
| `countUp` | number text counts from `from` to its value: `text` becomes `{ "value": "", "expr": "formatNumber(linear(time, t0, t1, from, to), decimals, format)" }` with `tnum` set; the first number run counts, prefix/suffix kept; text without digits is `preset.target_kind` | `from` (0), `decimals` (0), `format` (`"locale"`; a template format such as `currency:USD:0`) | code |
| `zoomIn` | scale `from` → 100 with `blur` 12 → 0 and fade | `from` (140) | |

**Exit** (default ease `$theme.ease.exit`; mirrors of the entrances)

| Preset | What it does | Params (default) |
|---|---|---|
| `fadeOut` | opacity → 0 | — |
| `sink` | to `y + distance`, opacity 0 | `distance` (40) |
| `lift` | to `y − distance`, opacity 0 | `distance` (40) |
| `slideOut` | off-frame in `dir` | `dir` (left), `overshoot` (0) |
| `scaleOut` | scale → `to` | `to` (0) |
| `popOut` | scale → 0 with `back.in(overshoot)`; opacity → 0 over the last 30 % | `overshoot` (2) |
| `blurOut` | blur → `amount`, opacity 0, scale 104 | `amount` (24) |
| `maskHide` | hides behind an edge of its bounds | `dir` (up), `distance` (`"100%"`) |
| `wipeOut` | linear wipe out | `dir` (right), `feather` (60) |
| `drawOff` | `trimEnd` → 0 (or from the other end) | `from` (start) |
| `typeOff` | characters disappear one by one | `cps` (24), `cursor` (false) |
| `scrambleOut` | scramble then vanish | `chars` (`"A-Z0-9"`), `cycles` (6) |
| `trackOut` | tracking → `to` with fade | `to` (400) |
| `flipOut` | as `flipIn`, reversed | `axis` (x) |
| `shrinkOut` | scale X (or Y) → 0 toward an edge | `from` (left) |
| `zoomOut` | scale → `to` with blur 12 and fade | `to` (140) |

**Emphasis**

| Preset | What it does | Params (default) | Ease |
|---|---|---|---|
| `pulse` | scale ×`amount/100` over the first half, back over the second | `amount` (108) | `$theme.ease.emphasis` |
| `shake` | decaying position wiggle | `amp` (12), `freq` (14) | code |
| `wobble` | decaying rotation oscillation | `amp` (6), `freq` (6) | code |
| `bounce` | y up by `height` with squash/stretch (scaleX 94, scaleY 108), then down | `height` (40) | `power2.out` / `power2.in` |
| `glowPulse` | `effects.glow.intensity` ×`amount` and back (the target needs an effect with id `glow`, e.g. `light.glow`) | `amount` (1.5) | `sine.inOut` |
| `highlight` | a marker-style bar sweeps behind the text (a shape layer with `fitTo`) | `color` (`$theme.color.accent`) | code |
| `underline` | a line draws under the text | `color` (accent), `thickness` (6) | code |
| `colorFlash` | fill flashes to `color` and back | `color` (accent) | code, `sine.inOut` |

**Loop** (use `repeat: -1` or across the layer's life)

| Preset | What it does | Params (default) | Ease |
|---|---|---|---|
| `float` | y up by `amp` then back | `amp` (12) | `sine.inOut` |
| `spin` | rotation `+= turns × 360` | `turns` (1) | `linear` |
| `breathe` | scale ×`amount/100` and back | `amount` (104) | `sine.inOut` |
| `sway` | rotation +amp, −2·amp, +amp (25 / 50 / 25 %) | `amp` (4) | `sine.inOut` |
| `drift` | slow position noise (`noise` driver) | `amp` (20), `freq` (0.2) | code |
| `shimmer` | opacity dips by `amount` and back (the spec's gradient sweep is approximated this way) | `amount` (30) | `sine.inOut` |

**Camera** (target a camera, or a null the content is parented to, in 2D)

| Preset | What it does | Params (default) | Ease |
|---|---|---|---|
| `pushIn` | moves the camera `amount` px closer (2D: scale up) | `amount` (120) | `$theme.ease.move` |
| `pullOut` | the reverse | `amount` (120) | `$theme.ease.move` |
| `pan` | position `+= by` | `by` (`[200, 0]`) | `$theme.ease.move` |
| `orbit` | approximated: on a camera `rotationY += degrees`; on other targets a plain `rotation` | `degrees` (30) | `sine.inOut` |
| `dollyZoom` | approximated: `zoom *= amount` on a camera, `scale` elsewhere (no counter-move) | `amount` (1.5) | `$theme.ease.move` |
| `handheld` | `wiggle` drivers on position (8·amount px) and rotationZ (0.6·amount°), two octaves | `amount` (1), `freq` (0.7), `seed` (0) | code |
| `whipTo` | a fast move by `by` with motion blur forced on | `by` (`[-1920, 0]`) | `power4.inOut` |

Transitions between layers or scenes are a separate mechanism ([06-transitions-and-scenes.md](06-transitions-and-scenes.md)).

## 4. Drivers

Procedural motion on top of a property's base value (canonical: they render natively and export to After Effects as expressions). Prefer a driver to an expression for "always moving a little" (`lint.expr_prefer_driver`).

```jsonc
"rotation": { "value": 0, "wiggle": { "freq": 1.5, "amp": 3 } }
"position": { "keys": [ … ], "spring": { "stiffness": 120, "damping": 9 } }
"scale":    { "value": [100, 100], "audio": { "asset": "music", "band": [30, 120], "gain": [25, 25], "smooth": 0.08 } }
"opacity":  { "value": 100, "oscillate": { "freq": 0.5, "amp": 20, "wave": "sine" } }
"position": { "value": [0, 0], "follow": { "path": "leader.position", "delay": 0.12, "offset": [40, 0] } }
```

| Driver | Fields (defaults) | Effect |
|---|---|---|
| `wiggle` | `freq` Hz (1), `amp` (required; number, or a vector per dimension), `octaves` (1), `ampMult` (0.5), `seed` (0), `dims` (all; a list of `x`, `y`, `z`) | smooth fractal noise in [−amp, amp] per dimension, seeded by `seed` + layer id + property path (two layers with the same settings differ unless they share a seed); octaves summed and normalised by Σ ampMultⁱ so \|value\| ≤ amp (deliberately unlike After Effects); sampled at **layer time** |
| `noise` | `freq` (0.5), `amp` (required), `seed` (0), `dims` | single-octave smooth gradient noise, slower and rounder; for drift; layer time |
| `oscillate` | `freq` Hz (1), `amp` (required), `phase` degrees (0), `wave` `sine` \| `triangle` \| `square` \| `saw` (`sine`), `decay` per second (0) | a periodic wave, `amp · e^(−decay·t)`, *t* from the layer's **in point** (so a component instance or trimmed layer starts at full amplitude) |
| `spring` | `stiffness` (170), `damping` (26, > 0), `mass` (1) | **replaces** the value with a spring-filtered version of the base animation (lag, overshoot, follow-through); simulated deterministically from the in point with 1/960 s substeps and checkpoints; before the in point the base value |
| `follow` | `path` (a property path in the comp, required), `delay` s (0), `offset` (0 or a vector), `factor` (1) | `value + factor · other(t − delay) + offset` on **raw property values**, no coordinate conversion; chains are fine, cycles are `ref.cycle`; for world-space following use an expression with `toComp`/`fromComp` |
| `audio` | `asset` (required), `band` Hz (`[20, 20000]`), `gain` (required; property units per unit level, a vector for vector properties), `smooth` s (0.05), `mode` `level` \| `onset` (`level`), `decay` s (0.3, onset), `floor` (0) | the band's RMS envelope normalised so the loudest 50 ms = 1, floored (`max(0, level − floor)/(1 − floor)`), smoothed (attack `smooth/4`, release `smooth`); `onset`: a pulse of 1 at each transient decaying with `decay` ([11](11-media-and-audio.md) §8) |

Order of application is fixed ([01](01-document.md) §10): `follow`, `spring`, `wiggle`, `noise`, `oscillate`, `audio`. Every driver takes `enabled` (default `true`; a disabled driver is removed; inside components and repeat templates it may be `$props.x` or a template). Missing or invalid fields: `anim.driver_params`. A driver on a separated dimension (`position.x`) seeds from the dimension's own path.

## 5. Keys from data and audio

**List binding** (authored): an animatable property takes its keyframes from a list.

```jsonc
"position": { "keys": { "from": "$props.moves", "t": "t", "v": ["x", "y"], "ease": "power2.inOut", "hold": false } }
"opacity":  { "keys": { "from": "$data.fades", "t": "at", "v": "alpha", "ease": "curve" } }
```

| Field | Notes |
|---|---|
| `from` | a reference to a list of row objects |
| `t` | the field holding each key's time |
| `v` | the field (scalar property) or list of fields (one per dimension) holding the value |
| `ease` | a field name holding an ease per row, or a constant ease for every segment |
| `hold` | `true` makes every key a hold key |

Rows are sorted by time; a row missing a field or with a non-numeric value is `data.bad_point`.

**Audio to keys** (authored, for export targets without the driver):

```jsonc
"scale": { "keys": { "fromAudio": { "asset": "music", "band": [30, 120], "gain": [20, 20], "rate": 30 } } }
```

Keyframes at `rate` per second (default 30) from the band's level envelope (same analysis as the `audio` driver), each `default + gain × level` where the default is the property's (`scale` 100 per dimension, `opacity` 100, `position` the comp's centre, others 0), simplified within 1 % of range. Until the audio asset is fetched (`motion.check` on a document with an `https:` asset), the property holds that default and `check` reports the info `asset.unmaterialized` at `…/keys/fromAudio/asset`.

## 6. Examples

`examples/04-presets.json`: one tween per built-in preset family on labelled targets (enter, exit, emphasis, loop with `repeat: -1`, camera on a 2D rig null), a local preset with params used twice, a library preset, and `props` overrides. `examples/04-drivers.json`: every driver (`wiggle` with octaves and `dims`, `noise`, `oscillate` with `decay` and each `wave`, `spring` on keyed motion, `follow` chain with `delay`/`offset`/`factor`, a disabled driver) and a list `keys` binding from `data`. Both check with 0 errors; `04-presets.json` carries lint taste warnings by design (many presets start together: `lint.too_many_simultaneous_moves`; text briefly outside the safe area during entrances; `lint.expensive_effect` on the glow). The `audio` driver and `fromAudio` need an audio asset, so they are shown above and not in the checked examples.
