# 03. The timeline: tweens, the position parameter, targets, property names, text-unit tweens, staggers, crawl

Scope: spec 2 §2.6, 2.7, 2.13 (authored form only). The timeline is the GSAP-shaped way to write motion; the normalizer compiles every tween to keyframes (or, for text units, to a text animator) and deletes the timeline. Presets, which expand into tweens, are in [04-presets-and-drivers.md](04-presets-and-drivers.md). Generated tables: `Tween`, `Target`, `Targets`, `PropValue`, `Position`, `Stagger`, `StaggerObject`, `StaggerFrom`, `StaggerGrid`, `StaggerAxis`, `Crawl`, `CrawlEdge` in `92-schema-types-*.md`.

```jsonc
"timeline": [
  { "label": "intro", "at": 0 },
  { "target": "bg",    "from": { "opacity": 0 }, "dur": 0.4 },
  { "target": "title", "from": { "y": "+=80", "opacity": 0, "blur": 20 }, "dur": 0.8, "ease": "expo.out", "at": "<0.1" },
  { "target": "title/chars!", "from": { "opacity": 0, "y": "+=24" }, "dur": 0.5, "stagger": 0.025, "ease": "back.out(1.6)" },
  { "target": ["icon1", "icon2", "icon3"], "preset": "popIn", "stagger": { "each": 0.08, "from": "center" }, "at": "@beat1" },
  { "target": "title", "to": { "scale": 106 }, "dur": 4, "ease": "sine.inOut", "at": "intro+0.5" },
  { "target": "card",  "fromTo": [ { "rotation": -8 }, { "rotation": 0 } ], "dur": 0.6, "ease": "spring(260, 14)" },
  { "target": "logo",  "set": { "opacity": 0 }, "at": 5.5 }
]
```

## 1. Tween fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `target` | target or list of targets | — | Required except on label entries (§3). |
| `from` | props | — | Animate **from** these values to the property's value at the tween's end. |
| `to` | props | — | Animate from the property's value at the tween's start **to** these. |
| `fromTo` | `[props, props]` | — | Both ends given. |
| `set` | props | — | An instant change at `at` (hold keys); `dur` must be absent or 0 (`tween.set_with_duration`). |
| `preset` | name | — | A built-in, local or library preset, or `$props.x` ([04](04-presets-and-drivers.md)). Combines with `dur`, `ease`, `stagger`, `props`. |
| `props` | object | `{}` | Preset parameters. |
| `dur` | time or `"auto"` | `$theme.motion.dur.base` (0.5 s in the default theme) | `"auto"` only with a spring ease (`tween.auto_duration`): the spring's settle time. Inside a preset a percentage (`"30%"`) is a fraction of the preset's duration. |
| `ease` | ease | `$theme.ease.default` (`power2.out`) | Any form of [02](02-keys-and-eases.md) §2. |
| `at` | position | `"+=0"` | §2. |
| `stagger` | number or object | none | §6. |
| `repeat` | integer or `-1` | `0` | Extra repeats; `-1` repeats until the target layer's out point. |
| `yoyo` | boolean | `false` | With `repeat`, alternate direction (the ease is mirrored `.in` ↔ `.out`). |
| `repeatDelay` | time | `0` | Gap between repeats. |
| `label` | id | none | Names this entry's start time. A tween-less `{ "label": "x", "at": … }` defines a label at a position. |
| `id` | id | none | For diagnostics and lint; also a position reference (`"at": "hi"` = the start of tween `hi`); the key for `variants[].override.timeline`. |
| `enabled` | boolean or template | `true` | `false` drops the tween (no keys, no time on the timeline). Inside a component definition or repeat template it may be `$props.x` or `"{{$props.style == 'pill'}}"`. |

Exactly one of `from`, `to`, `fromTo`, `set`, `preset` (`tween.no_action`, `tween.multiple_actions`).

**Relative values** inside props:

| Form | Meaning | Example |
|---|---|---|
| `"+=n"` | add to the other end's value | `"y": "+=80"` |
| `"-=n"` | subtract | `"rotation": "-=15"` |
| `"*=n"` | multiply | `"scale": "*=1.2"` |
| `"+=[a, b]"` | add a vector | `"position": "+=[0, 80]"` |

In `from`, relative means relative to the **end** value (the property's value when the tween finishes: `"y": "+=80"` = start 80 px lower than where it ends). In `to`, relative to the **start** value. In `fromTo`, relative to the other end; both ends relative is `tween.both_relative`. A relative value on a non-numeric property is `tween.relative_type`. Templates work inside values (`"+=$props.distance"`, `"*={{$props.amount / 100}}"`).

## 2. The position parameter `at`

| `at` | Starts at |
|---|---|
| `2.5`, `"2.5s"`, `"75f"`, `"00:00:02:15"` | that absolute comp time |
| `"+=0.3"` | 0.3 s after the **end of the timeline so far** (the latest end of all earlier entries). Default `"+=0"`: sequence after everything before. |
| `"-=0.2"` | 0.2 s before the end of the timeline so far (overlap) |
| `"<"` | the **start** of the previous entry |
| `">"` | the **end** of the previous entry (differs from `"+=0"` when an earlier entry ended later) |
| `"<0.1"`, `"<-0.1"` | the previous entry's start ± |
| `">0.2"`, `">-0.2"` | the previous entry's end ± |
| `"intro"`, `"intro+=0.5"`, `"intro+0.5"`, `"intro-0.5"` | a label or a tween `id` (its start) ± . Undefined: `tween.unknown_label` (never created silently, unlike GSAP). |
| `"@beat3"`, `"@beat3+0.1"`, `"@beat3-2f"` | a comp marker ± . Undefined: `tween.unknown_marker`. |
| `"$props.start"`, `"{{$props.hold + 0.2}}"` | inside components and presets: a reference or template that yields a position |

"Previous entry" is the previous element of the `timeline` array (labels included). A staggered tween's end is its last element's end; a repeating tween's end includes all repeats. Times are comp times; the normalizer converts to each target layer's own time under `offset`/`stretch`. A tween that resolves before 0 is `tween.negative_time`; an unparsable `at` is `tween.bad_position`. Inside a preset, `at` is relative to the preset's start.

## 3. Targets

| Target | Meaning |
|---|---|
| `"title"` | the layer with id `title` |
| `["a", "b", "c"]` | each target in this order (the order a stagger uses). A list may mix every form below: `["kicker", "title/words", "cta"]` flattens into one sequence of items (a layer counts as one item, a unit target as its units) and one `stagger` runs across all of them. |
| `"bars.*"` | every layer whose generated id starts with `bars.` (a `repeat`), in index order |
| `"title/chars"`, `"title/words"`, `"title/lines"` | the text units of a text layer (§5); `!` skips whitespace: `"title/chars!"` |
| `"title/span:price"`, `"title/span:price/chars"` | one span as a unit; the characters of a span |
| `"logo.contents.ring"` | a shape group or item inside a shape layer; property names are then relative to it |
| `"card.effects.glow"` | an effect instance; property names are its parameters |
| `"cam"` | a camera or light layer (`position`, `pointOfInterest`, `zoom`, `dof.focusDistance`, `intensity`, …) |
| `"$props.layer"`, `"tick-{{$props.side}}"` | inside a component definition or repeat template: resolved after expansion against the generated comp's layers |

A target that matches nothing is `tween.unknown_target`. A target that existed in the definition but was dropped by `enabled: false` (or a `repeat` whose list came out empty) is a no-op with the info `tween.target_disabled`; a list target loses only the dropped items.

## 4. Property names inside `from` / `to` / `set`

Keys are property paths relative to the target, plus shorthands:

| Shorthand | Expands to | Value |
|---|---|---|
| `x`, `y`, `z` | `transform.position.x` / `.y` / `.z` (separate dimensions) | px |
| `position`, `anchor`, `opacity`, `skew`, `skewAxis` | the transform property | spec units |
| `scale` | `transform.scale`; a number applies to every dimension | percent |
| `scaleX`, `scaleY`, `scaleZ` | one dimension of scale, written as whole-vector keys with the other dimensions held at their value at each key time | percent |
| `rotation` | `transform.rotation` (2D) or `transform.rotationZ` (3D layers) | degrees |
| `rotationX`, `rotationY`, `rotationZ`, `orientation` | the 3D transform | degrees |
| `blur` | the `radius` of a `blur.gaussian` effect with id `_blur`, added at the end of the target's `effects` if missing (dropped again at normalization when it stays 0 everywhere). On a text-unit target: the animator's per-unit `blur`. | px |
| `color`, `fill` | the text fill, the first `fill` item of a shape layer, or a solid's `color`; a shape layer with no fill item is `tween.no_paint` | colour |
| `stroke`, `strokeWidth` | the first stroke item's colour / width of a shape layer; on text `style.stroke.color` / `style.stroke.width`; no stroke item is `tween.no_paint` | colour, px |
| `tracking`, `size`, `weight`, `axes.<tag>` | text style properties (`weight` and `axes` animate variable fonts) | [08](08-text.md) units |
| `trimStart`, `trimEnd`, `trimOffset` | the first `trim` item of the target, added at defaults as the last item if missing (works on shape-preset layers too) | percent, degrees |
| `volume` | audio volume | dB |
| any path | `contents.ring.trim.end`, `effects.glow.intensity`, `text.animators.a.amount`, `masks.m1.feather`, `effects.glass.specular.angle` (object-valued effect parameters by dotted sub-path), `dof.focusDistance` | the property's units |

A name the target lacks is `tween.unknown_property` (the hint lists valid names). Tweening a dimension (`x`) and the whole vector (`position`) of one property on one layer is allowed. A property is stored separated only when more than one dimension carries its own keys (or a driver or expression rides on a dimension); a single keyed dimension beside static ones is rejoined into whole-vector keys. Separating a property with `path` tangents or roving keys is refused (`anim.separate_discards_path`: tween `position` instead).

### How tweens become keyframes

Processed in timeline order. For each (target property, tween): compute the start and end values, write two keys (start with the tween's ease, end with the property's following ease), more for repeats and staggers.

1. **Base**: before any tween a property's value is its static value or its explicit keys.
2. **`to`**: start = the property's value at the tween's start given everything processed so far; end = the `to` value (relative resolved against the start).
3. **`from`**: end = the property's value at the tween's **end** given everything processed so far (a `from` respects a later explicit key or an earlier-processed tween, GSAP's "from the given value to the current one"); start = the `from` value.
4. **Overlap**: a new tween whose span overlaps an animated span on the same property removes the existing keys inside its span and inserts a hold key at its start (GSAP `overwrite: auto`). Lint reports it (`lint.tween_overlap`).
5. **Explicit keys win their ticks**: a tween may not place a key at the exact tick of an explicit key (`tween.key_collision`).
6. **Hold outside**: before the first tween key and after the last the property holds.
7. **`set`**: a key at `at` with a `hold` segment before it; one tick later when a key already sits there.
8. **Repeat / yoyo**: each repeat writes another key pair; repeat *k*'s end segment is `hold` and repeat *k+1* starts at `end_k + repeatDelay` (one tick after when 0); `yoyo` swaps ends and mirrors the ease.

Every generated key carries the tween's `id` (or index) in a private `src` field, so diagnostics point back to the tween.

## 5. Text-unit tweens

A tween on `layer/chars`, `layer/words`, `layer/lines` or `layer/span:id` animates each unit separately, offset by its stagger. It creates no layers: it compiles to a text animator with a `stagger` selector ([08-text.md](08-text.md) §6.4).

```jsonc
{ "target": "title/chars!", "from": { "opacity": 0, "y": "+=40", "rotation": -12 },
  "dur": 0.6, "ease": "back.out(1.4)", "stagger": { "each": 0.03, "from": "start" }, "at": 0.4 }
```

compiles to (canonical, abbreviated):

```jsonc
"animators": [{ "id": "_tw3", "props": { "opacity": 0, "position": [0, 40], "rotation": -12 },
  "selectors": [{ "type": "stagger", "by": "chars", "skipSpaces": true, "start": 0.4, "each": 0.03, "dur": 0.6,
                  "ease": "back.out(1.4)", "direction": "out", "from": "start" }] }]
```

`direction: "out"` for `from` tweens (the values apply fully then release), `"in"` for `to` tweens.

| Allowed property | Kind | Value |
|---|---|---|
| `x`, `y`, `z`, `position`, `rotation`, `rotationX`, `rotationY`, `skew`, `tracking`, `characterOffset`, `blur`, `clip` | **offset per unit** | relative values only (`"y": "+=40"`), or a bare number read as an offset; an absolute value (`"x": 960`) is `tween.unit_absolute` |
| `opacity`, `fill`, `stroke`, `strokeWidth`, `scale`, `weight`, `axes.<tag>` | **target** | absolute values |

Any other name is `tween.text_unit_property`. `rotationX`/`rotationY` need `threeDPerChar`. `maskReveal`/`maskHide` on a unit target compile to a per-unit `clip` animator (each unit is revealed from behind its own edge). A tween on `title/span:price/chars` intersects the stagger with a range selector over the span; the stagger index runs over the layer's characters, so a span starting at the *k*-th character starts *k* × `each` late (start the tween earlier or put the span first).

## 6. Staggers

```jsonc
"stagger": 0.05                                   // each target starts 0.05 s after the previous
"stagger": { "each": 0.05, "from": "center" }     // from the middle outwards
"stagger": { "amount": 0.6, "from": "end" }       // all starts spread across 0.6 s
"stagger": { "each": 0.04, "grid": [8, 4], "from": [0, 0], "axis": null, "ease": "power2.in" }
"stagger": { "each": 0.03, "from": "random", "seed": 7 }
```

| Field | Default | Meaning |
|---|---|---|
| `each` | — | delay between consecutive targets (exactly one of `each` / `amount`) |
| `amount` | — | total spread; `each = amount / d_max` (`amount / (n − 1)` from `start`/`end`) |
| `from` | `"start"` | `start`, `end`, `center`, `edges`, `random`, an index (0-based), or `[col, row]` with `grid` |
| `grid` | none | `[cols, rows]` (row-major) or `"auto"` (inferred from the targets' positions at the tween start); distance is Euclidean in cells |
| `axis` | null | with `grid`: `"x"` or `"y"` (distance along one axis) |
| `ease` | `linear` | distributes start times along an ease (`power2.in` bunches early starts) |
| `seed` | 0 | the seeded permutation for `random`, stable across renders |

Target *i* starts at `tween start + ease(d_i / d_max) · amount`, *d_i* its distance from `from`, `amount = each · d_max` when `each` is given (GSAP: the spread is `each · (n − 1)` from `start`/`end`, about half from `center`/`edges`; with `center` and even *n* the two middle targets start together). One target: the stagger is ignored. Durations and eases do not change per target. Ill-formed staggers (neither/both of `each`/`amount`, negatives, a grid that does not cover the targets, an index out of range, `[col, row]` or `axis` without `grid`) are `tween.stagger_params`. Lint: `lint.stagger_too_fast` (`each` < 0.012 s with > 4 targets), `lint.stagger_too_slow` (spread > 2 s or `each` > 0.25 s with > 6 targets).

## 7. Crawl

A layer field (authored only), on `text` and `comp` layers: constant whole-pixel-per-frame scrolling for end credits and tickers (fractional speeds shimmer; blur hurts legibility; the duration follows from the speed).

```jsonc
{ "id": "credits", "type": "comp", "comp": "creditsSheet",
  "crawl": { "dir": "up", "speed": 2, "from": "below", "to": "above", "hold": [1, 1] } }
{ "id": "ticker", "type": "text", "text": "$data.headline", "crawl": { "dir": "left", "duration": 12 } }
```

| Field | Default | Notes |
|---|---|---|
| `dir` | `up` | `up`, `down`, `left`, `right` |
| `speed` | — | whole pixels per comp frame; exactly one of `speed` / `duration` |
| `duration` | — | desired travel time; the normalizer picks the nearest whole-pixel speed; `lint.crawl_duration_mismatch` when the actual differs by > 5 % |
| `from` | the edge behind the direction (`below` for `up`) | `below`, `above`, `left`, `right`, `edge` (the leading edge at the comp edge), or a number along the travel axis |
| `to` | the edge ahead | same |
| `hold` | `[0, 0]` | still time before the crawl starts and after it ends |
| `at` | the layer's `in` | when the crawl starts (after `hold[0]`) |

Compiles to a `linear` position pair on the travel axis snapped to integer pixels per frame, `motionBlur: false`, and `in`/`out` covering `hold[0]` + travel + `hold[1]` unless given. Travel *L* = content extent + comp extent (less with `edge`/numbers); with `speed` *s* the duration is *L*/*s* frames. Explicit position keys with a crawl are `tween.key_collision`. Per variant the same `speed` gives a different duration (`duration` gives the same duration at a different speed). Lint: `lint.crawl_fractional_speed` (a hand-made constant non-integer scroll > 2 s), `lint.motion_blur_on_scroll_text`, `lint.crawl_too_fast` (> max(4 px, size/6) per frame at 24 fps, scaled by 24/fps; comp layers 4 px).

## 8. Examples

`examples/03-timeline.json`: labels, every `at` form, `from`/`to`/`fromTo`/`set`, relative values, list targets mixing layers and text units, a repeat target with `bars.*`, a shape-item target, an effect target, shorthands (`blur`, `fill`, `trimEnd`, `scaleX`), `repeat`/`yoyo`/`repeatDelay`, text-unit tweens on chars/words/lines/span, and staggers (`each`, `amount`, `from: center`, `grid`, `random`). `examples/03-crawl.json`: a text ticker by `duration` and a comp credits crawl by `speed`. Both check with 0 errors. Expected warnings on `03-timeline.json`: `lint.too_many_simultaneous_moves` (the grid stagger with `axis: "x"` starts each column together), `lint.expensive_effect` (the glow), and the info `lint.on_beat`. On `03-crawl.json`: `lint.offscreen_while_visible` on the credits (a crawl starts fully below the frame by design) and `lint.text_outside_safe_area` on the ticker (it crosses the frame edges by design).
