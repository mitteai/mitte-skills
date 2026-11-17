# Presets: the library packs, using them, writing your own

A preset is a named, parameterized list of tweens. The engine ships 54 built-in presets (spec 2 §2.8.3, documented in the animation area; names listed below so references resolve), the library ships 9 more in three packs (`kinetic.*`, `ui.*`, `editorial.*`), and a document may define its own under `presets`. All three kinds use the same definition format and the same expansion pass (`engine/crates/rexx-normalize/src/passes/presets.rs`; built-ins in `presets_builtin.rs`). Every preset below is listed with every param and its tween list in `93-presets.md`.

## Using a preset

```json
{ "target": "slam/words", "preset": "mitte/kinetic.slam@1", "props": { "from": 240, "blur": 14 }, "stagger": 0.12, "at": 0.3 }
```

| Entry field | Meaning |
|---|---|
| `preset` | a built-in name (`rise`), a local preset id, or a library reference `mitte/<pack>.<name>@1` |
| `props` | param values. An unknown name is `preset.param` ("The preset "mitte/ui.slide@1" has no param "nope"." hint "Valid params: offset."). Values are checked like component params (spec 12 §12.3.2), each as `preset.param` at `/…/props/<name>`: type (`"amount": "big"` on a number is "amount: expected a number, got "big"."), `min`/`max` ("amount: 150 is above the maximum 100."), enum `values` ("dir: "sideways" is not one of up, down."), `maxChars`, list item counts. A `$props`/`{{ }}` value still dynamic passes. `$theme`/`$data` references and `{{ }}` templates are allowed in props. |
| `dur`, `ease` | override the preset's own `dur` and `ease` for every tween in it (a nested preset inherits them too) |
| `stagger` | per target when the target is a list, a `.*` wildcard or a text unit path (`title/words`, `title/chars`, `title/lines`); the whole tween group is staggered per unit |
| `at`, `id`, `label`, `repeat`, `yoyo`, `repeatDelay`, `enabled` | as on any tween |

Effective duration: the entry's `dur`, else the enclosing preset's (when nested), else the preset's own `dur` (after `$theme` resolution), else `$theme.motion.dur.base`. Effective ease: the entry's `ease`, else the enclosing preset's, else the preset's own, else `$theme.ease.default`. A tween inside the preset that carries its own `dur`/`ease` keeps it (the library's `opacity` sub-tweens do: `kinetic.slam` fades over `dur.xs` while scaling over `dur.s`).

Resolution order for a name: a library reference resolves against the library (`ref.library_unknown` / `ref.library_version` from the library pass; a **component** reference in `preset` is also `ref.library_unknown` because kinds are separate); then the document's `presets`; then the built-ins. An unknown name is `preset.unknown` with a did-you-mean over built-in and local names. `preset.target_kind` is raised when the preset has no meaning for the target ("drawOn needs a shape layer with a stroked path; "v" is a text layer." hint "Apply it to a shape layer, or use wipeIn."). `preset.cycle`: "Presets use each other in a loop: loopA → loopB → loopA."

## The three library packs

| Preset | Pack intent | Does | `dur` / `ease` | Params (default, documented range) | Use on |
|---|---|---|---|---|---|
| `mitte/kinetic.slam@1` | bold per-word type entrances with overshoot and squash; one slam per piece | scale `from` → 100 with `power4.out`, opacity in over `dur.xs`, `blur` px clearing as it lands | `$theme.motion.dur.s` / `power4.out` | `from` 260 (120–600), `blur` 10 (0–40) | `title/words` with stagger 0.08–0.16 s, or one hero word; pair with `shake` on a rig null |
| `mitte/kinetic.stomp@1` | | from `y − distance` with `power3.in`, then a 0.06 s squash (`scaleX +squash`, `scaleY −squash`) that recovers over `dur.s` with `$theme.ease.emphasis` | `dur.s` / `power3.in` | `distance` 160 (40–600), `squash` 14 (0–40) | the last word of a line |
| `mitte/kinetic.flip@1` | | 2D flip: `scaleY` 0 → 100 with a `drop` px fall, `back.out(1.8)`; opacity over `dur.xs` | `dur.base` / `back.out(1.8)` | `drop` 24 (0–120) | words or whole lines, stagger ≈ 0.06 s |
| `mitte/kinetic.stretch@1` | | `scaleX` from `stretch`, `tracking` from wide to normal, elastic settle; opacity over `dur.s` | `dur.l` / `elastic.out(1, 0.55)` | `tracking` 300 (0–1000), `stretch` 150 (100–300) | a single kicker or brand word, not long copy |
| `mitte/ui.pop@1` | Material-timed UI motion; durations fixed (not theme tokens) | scale `from` → 100 and opacity 0 → 100 (0.15 s linear) | 0.25 / `[0.05, 0.7, 0.1, 1]` | `from` 92 (50–100) | modals, popovers, cards that appear on a click |
| `mitte/ui.slide@1` | | position from `+= offset` with a 0.2 s fade | 0.3 / `[0.2, 0, 0, 1]` | `offset` `[0, 32]` (a two-number list: `[0, 32]` rises from below, `[-48, 0]` comes from the left) | sheets, toasts, panels |
| `mitte/ui.fade@1` | | opacity 0 → 100 | 0.2 / `[0.3, 0, 0.8, 0.15]` | — | tooltips, hover states, secondary labels |
| `mitte/editorial.rise@1` | long, soft serif entrances, nothing bounces | from `y + distance`, opacity 0, `blur` px clearing over `dur.l` with `sine.out` | `dur.xl` / `[0.16, 1, 0.3, 1]` | `distance` 60 (10–300), `blur` 8 (0–30) | `title/lines` with a 0.12–0.2 s stagger: pull quotes, chapter titles |
| `mitte/editorial.fade@1` | | opacity 0 → 100 with a `scale` → 100 settle | `dur.l` / `sine.inOut` | `scale` 102 (100–110) | body text, captions, bylines, images |

Because `kinetic.*` and `editorial.*` take their durations from theme tokens, the same preset is 0.22 s under `bold` and 0.4 s under `editorial`; `ui.*` is the same under every theme on purpose.

## Built-in presets (names)

Enter: `fadeIn`, `rise`, `drop`, `slideIn`, `scaleIn`, `popIn`, `blurIn`, `maskReveal`, `wipeIn`, `drawOn`, `typeOn`, `scrambleIn`, `trackIn`, `flipIn`, `growIn`, `countUp`, `zoomIn`. Exit: `fadeOut`, `sink`, `lift`, `slideOut`, `scaleOut`, `popOut`, `blurOut`, `maskHide`, `wipeOut`, `drawOff`, `typeOff`, `scrambleOut`, `trackOut`, `flipOut`, `shrinkOut`, `zoomOut`. Emphasis: `pulse`, `shake`, `wobble`, `bounce`, `glowPulse`, `highlight`, `underline`, `colorFlash`. Loop: `float`, `spin`, `breathe`, `sway`, `drift`, `shimmer`. Camera: `pushIn`, `pullOut`, `pan`, `orbit`, `dollyZoom`, `handheld`, `whipTo`. Library components name built-ins in their `preset`-typed params (`lower-third.bar` `enter`: `slideIn`, `wipeIn`, `fadeIn`); the `kind` on such a param (`enter`, `exit`, `emphasis`, `loop`, `camera`) is documentation, not enforced.

## Writing a preset

```json
{ "presets": {
    "riseBlur": {
      "params": { "distance": { "type": "number", "default": 48 }, "blur": { "type": "number", "default": 16 } },
      "dur": "$theme.motion.dur.base", "ease": "$theme.ease.enter",
      "tweens": [ { "from": { "y": "+=$props.distance", "opacity": 0, "blur": "$props.blur" } } ] },
    "heroIn": {
      "params": { "glow": { "type": "number", "default": 2.2 } },
      "dur": "$theme.motion.dur.l",
      "tweens": [
        { "preset": "riseBlur", "props": { "distance": 90, "blur": 24 }, "at": 0 },
        { "target": "$target.effects.glow", "fromTo": [{ "intensity": "$props.glow" }, { "intensity": 0.8 }], "dur": 0.6, "ease": "power2.out", "at": 0.15 },
        { "preset": "shake", "props": { "amp": 10, "freq": 12 }, "at": ">" } ] } } }
```

| Definition field | Notes |
|---|---|
| `params` | map name → `{ type, default, description?, values?, min?, max? }`. Types as for components (`number`, `text`, `enum`, `boolean`, `color`, `time`, `ease`, `list` with `item`, …), checked the same way. A param without a default and not given is `null`. |
| `dur`, `ease` | the preset's own; may be `$theme.…` or a `{{ }}` template (`popIn` builds its ease as `{{'back.out(' + $props.overshoot + ')'}}`). Optional. |
| `tweens` | the list. Each tween is an ordinary tween (`from`, `to`, `fromTo`, `dur`, `ease`, `at`, `stagger`, `repeat`, `yoyo`, `enabled`) **without `target`** (the entry's target is implied), or `{ "preset": "<name>", "props": … }` to nest another preset (built-in, local or library). `at` is relative to the preset's start; `0` is the start, `">"` the end of the previous tween in the preset, `"<0.1"` 0.1 s after the previous one's start. A `dur` or `at` written as a percentage (`"30%"`) is accepted only inside the **built-in** table (schema rejects it in a document preset: `doc.type` "Invalid time "20%""). |
| sub-targets | `"target": "$target"` (explicit), `"target": "$target.effects.<effect id>"` (a parameter of a named effect on the target) and `"target": "$target/chars"` (`/words`, `/lines`: the target's text units, staggered by the tween's own `stagger`, so the per-unit motion is part of the preset) work. |
| `enabled` | a boolean, a `$props.<boolean>`, or a template (`"{{$props.n > 0}}"`); a disabled tween is dropped at expansion (verified). |
| `kind`, `description` | free metadata (built-ins carry `kind`; the library adds `description`, read by the catalogue). |

Rules: a preset may use other presets to any depth, recursion is `preset.cycle`; `$props` works anywhere inside, including `at` and nested `props`; `$theme` and `$data` are the document's. Library presets are the same format wrapped in an `x-library` pack file (`04-components-writing.md` explains the wrapper; a pack is `{ "x-library": { "meta": { "name": "<pack>", … }, "presets": { "<pack>.<name>": { … } } } }` and each entry's name must carry the pack prefix).

## Rhythm

Entrances 0.4–0.8 s, exits 0.3–0.5 s (≈ 0.6–0.75 × the entrance, `.in` eases), holds ≥ reading time, one overshoot per piece; stagger words at 0.04–0.16 s. Anything still on screen when its comp ends needs an exit (`lint.missing_exit`).

Worked example (checked, no warnings): `examples/concepts/02-presets.motion.json`: `kinetic.slam` on `slam/words` with a 0.12 s stagger, `kinetic.stretch` on a kicker, the custom `heroIn` above nesting `riseBlur` and `shake` with a glow sub-target, `ui.pop` and `editorial.fade` on a card, `sink` as the exit.
