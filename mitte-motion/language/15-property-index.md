# 15. The property index: addressing any property, units, ranges and clamps, what animates, authored-only constructs

Scope: spec 17. The machine-derived list of every animatable path is generated from the schema in [91-animatable-paths.md](91-animatable-paths.md) (539 paths); every field of every type is in [92-schema-types-*.md](92-schema-types-1.md). This page is the hand-written half: how a path is written in each place that takes one, the unit and clamp range of each animatable property kind, which fields animate only with hold keys, and what exists in authored form only.

## 1. Writing a path

| Where | Form | Example |
|---|---|---|
| tween `target` | a layer id, then optional `.contents.<item>…`, `.effects.<id>`, or `/chars` etc. | `"logo.contents.ring"`, `"card.effects.glow"`, `"title/words"`, `"bars.*"` |
| tween property name | relative to the target: a shorthand or a dotted path, `transform` optional | `"y"`, `"scale"`, `"contents.ring.trim.end"`, `"effects.glow.intensity"`, `"text.animators.a.amount"`, `"masks.m1.feather"`, `"effects.glass.specular.angle"`, `"dof.focusDistance"`, `"style.tracking"` |
| `follow.path` (driver) | an absolute path in the comp | `"leader.position"`, `"leader.position.x"`, `"rig.contents.g.rotation"` |
| expressions | the object model ([12](12-expressions.md) §4); spec names and After Effects names | `thisComp.layer("a").transform.position`, `content("ring").content("trim").end`, `effect("glow")("radius")` |
| JSON pointers in diagnostics | RFC 6901 into the **authored** document | `/comps/main/layers/2/transform/position/keys/0` |
| layer `pin`/`stabilize`, text `path.source.shape` | layer id, or `layer.contents.item` | `"ribbon.contents.spine"` |

Rules: the first segment is a layer id of the current comp (comps are never in a path); transform properties may skip `transform`; one dimension of a vector is `.x`, `.y`, `.z`; `*` matches one id segment and is allowed only in tween targets; generated ids contain dots (`bars.3`, `lt1.comp`, `scene.0`, `logo.contents.leaf`).

## 2. Units, ranges and clamps of animatable properties

Step 4 of the evaluation order ([01](01-document.md) §10) clamps the final value to the listed range; silent at render, reported by lint for key values outside it. Unlisted = not clamped.

| Property kind | Unit | Clamp | Default |
|---|---|---|---|
| `opacity` (layers, groups, paints, masks, animators as targets, styles) | percent | 0–100 | 100 |
| `scale` | percent per axis | none (negative mirrors) | `[100, 100(, 100)]` |
| `rotation`, `rotationX/Y/Z`, `orientation`, `skewAxis`, angles in effects | degrees (clockwise) | none | 0 |
| `skew` (layers, groups, animators) | degrees | −85–85 | 0 |
| `position`, `anchor`, `pointOfInterest`, shape item `position`, gradient `from`/`to`, point effect params | px | none (3D coordinates clamped to ±10⁹ at render) | per type |
| `trim.start`, `trim.end` | percent of length | 0–100 | 0, 100 |
| `trim.offset` | degrees, 360 = one length | none | 0 |
| stroke `width`, `miterLimit`, `roundCorners.radius`, `offset.amount`, `feather`, `expansion`, blur radii | px (ratio ≥ 1 for miterLimit) | width ≥ 0, miterLimit ≥ 1, feather ≥ 0 | per item |
| `repeater.copies` | copies | 0–1000 | 3 |
| `offset.copies` | copies | 1–100 | 1 |
| `polystar.points` | count | 3–100 (fractions truncate) | 5 |
| `outerRoundness`, `innerRoundness`, `puckerBloat.amount` | percent | −100–100 | 0 |
| `wigglePaths.size` / `detail` / `wigglesPerSecond` | px / subdivisions / Hz | −4096–4096 / 0–10 / 0–1000 | 10 / 3 / 2 |
| stroke `wave.amount` | percent of width | 0–1000 | 0 |
| gradient `highlightLength` | percent of radius | −100–100 | 0 |
| gradient `stops`, `opacityStops`, `midpoints` | position 0–1 | positions in [0, 1], 2–64 stops | black → white |
| text `size` | px | > 0 | `$theme.type.size.0` |
| text `weight` / `axes.wght` | 1–1000 | the font's axis range | 400 |
| text `tracking` | thousandths of an em | none | 0 |
| text `leading` | px or `auto` | none | `auto` |
| `horizontalScale`, `verticalScale` | percent | none | 100 |
| `baselineShift` | px | none | 0 |
| range selector `start`/`end`/`offset` | percent or index | none | 0 / 100 / 0 |
| range selector `amount`, `easeHigh`, `easeLow` | percent | −100–100 | 100 / 0 / 0 |
| range `smoothness` | percent | 0–100 | 100 |
| wiggly `maxAmount`, `minAmount` | percent | none | 100, −100 |
| animator `opacity`, `fillOpacity`, `strokeOpacity` (targets) | percent | 0–100 after blending | 100 |
| animator `clip` edges | percent of the unit's bounds | 0–100 | 0 |
| audio `volume` | dB | none (`-inf` / ≤ −96 mutes) | 0 |
| audio `pan` | −100–100 | −100–100 | 0 |
| `timeRemap` | seconds (source time) | 0–source duration | none |
| `box` (text) | px | > 0 | none |
| camera `zoom` | px | 10⁻³–10⁷ at render | `w·50/36` |
| `dof.aperture`, `focusDistance`, `focusOffset` | px | CoC ≤ 128 px at render | 25.3, `zoom`, 0 |
| `dof.blurLevel`, light `intensity`, material percents | percent | none (light sum floored at 0) | 100 / 100 / per field |
| light `coneAngle`, `coneFeather`, `radius`, `falloffDistance`, `shadowDarkness`, `shadowDiffusion` | degrees, percent, px, px, percent, px | none | 90, 50, 500, 500, 100, 0 |
| style `opacity`, `spread`/`choke`, `noise`, `range`, `jitter` | percent | 0–100 | per style |
| style `depth` | percent | 1–1000 | 100 |
| style `distance`, `size`, `soften` | px | ≥ 0 | per style |
| `globalLight.angle`, `.altitude` | degrees | none | 120, 30 |
| colours | linear working-space floats | none (HDR allowed; the output stage tone-maps) | per field |
| `motionBlur.shutterAngle`, `shutterPhase` (hold keys only) | degrees | 0–720, −360–360 | 180, −90 |
| mask `opacity` | percent | 0–100 | 100 |
| effect parameters | per effect (the effects area) | per parameter | per effect |

## 3. What animates how

| Animation form | Properties |
|---|---|
| full (keys with any ease, drivers, expressions) | every path in [91](91-animatable-paths.md) whose static type is a number, vector, colour, gradient, path or time |
| hold keys only | `text` (source text), enum-valued fields that are animatable (`motionBlur.shutterAngle`/`shutterPhase` per spec; `characterRange`, `trackingType` as animator switches), booleans where stated |
| per entry | stroke `dashes` (each entry its own animatable), `axes.<tag>` (each axis) |
| whole array | gradient `stops`, `opacityStops`, `midpoints`, mask `variableFeather` (P3) |
| spatial (motion paths, arc-length easing, `rove`) | `position`, `anchor`, `pointOfInterest`, shape item `position`, gradient `from`/`to`, point and 3D-point effect parameters, light and camera positions; a separated position is not spatial |
| not animatable | `id`, `name`, `type`, timing fields (`in`, `out`, `offset`, `stretch`), `parent`, switches (`threeD`, `motionBlur`, `collapse`, `quality`, `sampling`, `guide`, `visible`, `enabled`), `blend`, `matte`, mask `mode`/`inverted`/`featherFalloff`/`motionBlur`/`rotobezier`, shape `direction`, `lineCap`/`lineJoin`/`rule`/`composite`/`mode` on items, text `font`/`italic`/`kerning`/`fontFeatures`/`language`/`opticalSize`/`allCaps`/`smallCaps`/`superscript`/`subscript`/`underline`/`strike`, paragraph fields, `cameraType`, `filmSize`, `dof.enabled`/`iris`, light `kind`/`falloff`/`castsShadows`, `material.castsShadows`/`acceptsShadows`/`acceptsLights`, output settings (`anim.not_animatable` when keyed) |

## 4. Authored-only constructs (expanded by the normalizer; never seen by the renderer or exporters)

| Construct | Expands to | Page |
|---|---|---|
| `$theme`, `$data`, `$props`, `$item`, `$index`, `$count`, `$parent.*`, `$target`, `$slots.*` references; colour modifiers | values | [01](01-document.md) §5, [13](13-components-themes-data.md) |
| `{{ … }}` templates with formats and arithmetic | strings or numbers | [13](13-components-themes-data.md) §2 |
| percent values | pixels | [05](05-layers.md) §5 |
| time forms other than seconds (`"12f"`, timecode, `"@marker"`) | seconds (ticks) | [01](01-document.md) §7 |
| `timeline` tweens, labels, the position parameter, `stagger` | keyframes, text animators with stagger selectors, added effects (`_blur`) and trim items | [03](03-timeline-and-tweens.md) |
| presets (built-in, local, library) and tween shorthands | tweens → keys | [04](04-presets-and-drivers.md), [03](03-timeline-and-tweens.md) §4 |
| `aeIn`/`aeOut` eases, `path: "auto"`/`"continuous"`, `firstVertex` | cubic-bezier eases, explicit tangents, rotated path keys | [02](02-keys-and-eases.md) |
| layer `dur`, video `speed`/`reverse`/`sourceIn`/`sourceOut`/`freeze`, comp `loopMode`, audio `fadeIn`/`fadeOut`/`duck` | `out`, `offset`, `stretch`, `timeRemap`, volume keys | [05](05-layers.md), [11](11-media-and-audio.md) |
| `origin`, `align`, `measureAt`, `keepPlace`, static `fitTo`, `layout` | anchors and positions (expressions when live) | [05](05-layers.md) §5, [13](13-components-themes-data.md) §5 |
| `transitionIn`/`transitionOut`, `scenes`, comp `duration: "auto"` | keys, effects, masks, helper layers, scene comp layers | [06](06-transitions-and-scenes.md) |
| `crawl` | integer-pixel position keys, `motionBlur: false` | [03](03-timeline-and-tweens.md) §7 |
| shape presets (`shape`), paint shorthands, `d` strings, `fromSvg`/`svg`, `points` bindings | shape contents | [07](07-shapes.md) §8 |
| mask `shape` primitives | mask paths | [09](09-masks-mattes-blending.md) §1.1 |
| text `words`/`wordStyle`/`paging` | spans, hold keys, animators | [08](08-text.md) §8 |
| camera `focalLength`/`fov`/`fStop`/`focusOn`, `orbit`/`dolly`/`dollyZoom`/`handheld` | `zoom`, `aperture`, keys, expressions, a rig null | [10](10-3d.md) §3–4 |
| marker `from`, `keys.fromAudio`, `keys: { from, t, v }` | markers, keyframes | [11](11-media-and-audio.md) §8, [04](04-presets-and-drivers.md) §5 |
| `lottie` on comp layers | generated comps | [11](11-media-and-audio.md) §5 |
| `theme`, `data` | tokens and values resolved | [13](13-components-themes-data.md) |
| `components`/`component` layers, `slot` layers, `repeat` layers, `enabled` templates | generated comps, comp layers, N layers, kept or dropped items | [13](13-components-themes-data.md) |
| `variants` | a different root comp per render | [01](01-document.md) §8 |
| `track` references, `pin`, `stabilize`, camera `solve` | keyframes, a keyed `distort.cornerPin`, camera keys | spec 18 (tracking area) |
| comp `physics`, layer `body` | bake references (`{ sim, body }` with `pre` = the keys before the hand-off), the `_physics` animator, `sims` | spec 19 (physics area) |

## 5. Canonical-only constructs

`sims` (the bake map), `{ "sim": hash, "body": id }` property bases, the `_physics` text animator, the `{ "ae": { … } }` zero-delta ease form, `x-component` on generated comp layers, `src` on generated keys. Writing any of the first three in an authored document is `doc.canonical_only`.

