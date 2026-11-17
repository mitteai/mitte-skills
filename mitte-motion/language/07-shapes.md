# 07. Shapes: every item kind, evaluation order, the path value, paints, gradients, morphing, every operator, authoring sugar, `fitTo`

Scope: spec 4 in full. Generated tables: `ShapeItem`, `ShapeKind`, `GroupTransform`, `PathValue`, `BezierPath`, `SvgPath`, `Paint`, `FillRule`, `LineCap`, `LineJoin`, `Composite`, `Taper`, `LengthUnits`, `StrokeWave`, `WaveUnits`, `Gradient`, `GradientType`, `GradientStop`, `OpacityStop`, `GradientInterpolation`, `GradientSpread`, `FreeformPoint`, `Morph`, `MorphMatch`, `FirstVertex`, `TrimMode`, `RepeaterTransform`, `MergeMode`, `ZigzagPer`, `PointStyle`, `FeatherDirection`, `FitTo`, `FitAxes`, `ShapePreset`, `PresetStroke`, `SvgFit`, `PointsBinding` in `92-schema-types-*.md`.

## 1. The shape layer and its items

```jsonc
{ "id": "badge", "type": "shape", "position": [960, 540],
  "contents": [
    { "type": "group", "id": "ring", "contents": [
      { "type": "ellipse", "size": [400, 400] },
      { "type": "stroke", "color": "#FFFFFF", "width": 12, "lineCap": "round" },
      { "type": "trim", "id": "trim", "end": { "keys": [ { "t": 0, "v": 0, "ease": "expo.out" }, { "t": 1.2, "v": 100 } ] } } ] },
    { "type": "group", "id": "disc", "contents": [
      { "type": "ellipse", "size": [340, 340] }, { "type": "fill", "color": "$theme.color.accent" } ] } ] }
```

Shape coordinates are layer pixels with (0, 0) at the layer origin; a new shape layer's anchor is `[0, 0]` and its position the comp centre, so shapes drawn around (0, 0) appear centred. `origin` measures the **untrimmed** bounds plus paint extents (so a `drawOn` shape at `trim.end: 0` still centres on its full outline). Every item has an optional `id` (unique among siblings), `name`, and `enabled` (default true; disabled items are skipped). Animatable fields take the four animatable shapes.

| `type` | Category | After Effects | Lottie `ty` | Status (engine 0.1.48) |
|---|---|---|---|---|
| `group` | container | Group | `gr` | rendered |
| `rect` | shape | Rectangle | `rc` | rendered |
| `ellipse` | shape | Ellipse | `el` | rendered |
| `polystar` | shape | Polystar | `sr` | rendered |
| `path` | shape | Path | `sh` | rendered |
| `fill` | paint | Fill | `fl` | rendered |
| `stroke` | paint | Stroke | `st` | rendered incl. `taper`, `wave`, `dashes` |
| `gradientFill` | paint | Gradient Fill | `gf` | rendered |
| `gradientStroke` | paint | Gradient Stroke | `gs` | rendered |
| `trim` | operator | Trim Paths | `tm` | rendered |
| `repeater` | operator | Repeater | `rp` | rendered |
| `roundCorners` | operator | Round Corners | `rd` | rendered |
| `offset` | operator | Offset Paths | `op` | rendered incl. `copies` > 1 |
| `zigzag` | operator | Zig Zag | `zz` | rendered |
| `puckerBloat` | operator | Pucker & Bloat | `pb` | rendered |
| `twist` | operator | Twist | `tw` | rendered |
| `wigglePaths` | operator | Wiggle Paths | baked on export | rendered |
| `merge` | operator | Merge Paths | `mm` | rendered, all five modes |
| `feather` | operator | (Rive feathering) | — | softens the edges of the paints above it in its group (§7) |

## 2. Evaluation order (After Effects' rules)

Within a group's `contents` the **first item is on top** and the list reads as a pipeline: geometry, then operators, then paints.

1. Shapes (`rect`, `ellipse`, `polystar`, `path`) create paths. A nested `group` contributes its painted output and its paths (transformed into this group's space), so later operators modify them; the nested group's own paints draw those paths as the enclosing group's later operators leave them.
2. An operator modifies every path **earlier in the array** in the same group (nested groups' paths included), operators in array order (`[path, roundCorners, trim]` rounds then trims).
3. A paint draws every path earlier in the array **in its final form**, after all operators of the group wherever they sit (a `trim` below a `stroke` still trims it, as in After Effects).
4. Earlier items draw **on top** of later ones: `[shape, stroke, fill]` draws the fill first, the stroke over it.
5. `repeater` duplicates everything above it (paths, paints, nested groups, already painted); operators and paints below it see all copies.
6. `merge` replaces the paths above it with one combined path; paints above the merge in the same group stop contributing (`lint.paint_above_merge`); paints below draw the merged path.

Worked example: `[rect A, ellipse B, roundCorners 20, stroke, fill, trim 60]` rounds A (B has no corners), trims both to 60 %, fills them (later in the array, so underneath) and strokes them on top. To fill the full shapes while stroking only the trimmed outline, put the fill with its own copies of the shapes in another group.

## 3. Groups and shapes

**`group`**: `contents`, `transform` (`anchor` `[0, 0]`, `position` `[0, 0]` spatial, `scale` `[100, 100]`, `rotation` 0, `opacity` 100, `skew` 0 (−85–85), `skewAxis` 0; all animatable; may be written directly on the group), `blend` (one of the 38 modes; the group renders to a buffer and blends once, each repeater copy its own). Matrix `T(position) · R(rotation) · Skew · S(scale/100) · T(−anchor)`. Paths: `badge.contents.ring.rotation`.

All shapes: `direction` `cw` (default) | `ccw` (matters for trim start, `evenodd` holes with `nonzero`, merge).

| Item | Fields (default) | Notes |
|---|---|---|
| `rect` | `size` `[100, 100]` A (negative clamps to 0); `position` `[0, 0]` A spatial (the centre); `roundness` 0 A (px, clamped to half the shorter side); `fitTo` (§8.4) | path starts at the top-right corner, clockwise |
| `ellipse` | `size` `[100, 100]` A (diameters); `position` `[0, 0]` A | four cubics (kappa 0.5523), starts at the top, clockwise |
| `polystar` | `kind` `star` \| `polygon`; `points` 5 A (3–100; fractions truncate); `outerRadius` 100 A; `innerRadius` 50 A (stars); `outerRoundness` 0 A (−100–100); `innerRoundness` 0 A; `rotation` 0 A; `position` `[0, 0]` A | the first point is straight up |
| `path` | `path` (path value) A **or** `d` (SVG path data); `morph` (`{ "match": "auto" }`, §5); `points` + `pointTransform` + `closed` + `smooth` (data binding, §8.5) | a `d` with several subpaths expands into one `path` item per subpath in a group (`<id>.0`, `<id>.1`, …) |

## 4. The path value

```jsonc
{ "v": [[x0, y0], [x1, y1], …], "in": [[dx, dy], …], "out": [[dx, dy], …], "closed": true }
"path": "M0 0 L200 0 Q260 0 260 60 Z"        // SVG path data, wherever a path is accepted
"path": { "d": "M0 0 L200 0 Z" }
```

| Field | Default | Notes |
|---|---|---|
| `v` | required | ≥ 1 vertex, ≤ 100,000 |
| `in` | all `[0, 0]` | incoming tangent of each vertex, relative to the vertex (control point `v[i] + in[i]`); same length as `v` |
| `out` | all `[0, 0]` | outgoing tangent (`v[i] + out[i]`) |
| `closed` | `false` | adds a segment from the last vertex to the first |

Segment *i* is the cubic `v[i], v[i]+out[i], v[i+1]+in[i+1], v[i+1]`; zero tangents give straight segments. SVG data: every SVG 1.1 command, absolute and relative (`M m L l H h V v C c S s Q q T t A a Z z`); quadratics are elevated exactly, arcs converted to cubics (≤ 90° per segment). Several subpaths where one path is expected (a mask, a key) is `path.multiple_subpaths`; mismatched array lengths or a malformed string is `path.invalid`. Canonical form always stores `{ v, in, out, closed }`. Used by shape `path` items, masks, text on a path, point-list effect parameters.

## 5. Path morphing

Path keys with different vertex counts are matched automatically (After Effects requires equal counts).

```jsonc
{ "type": "path", "morph": { "match": "auto", "samples": 0 },
  "path": { "keys": [ { "t": 0, "v": "M0 -100 L87 50 L-87 50 Z", "ease": "expo.inOut" },
                      { "t": 1, "v": { "d": "M100 0 A100 100 0 1 1 -100 0 A100 100 0 1 1 100 0 Z" }, "firstVertex": 2 } ] } }
```

| `morph` field | Values | Default | Meaning |
|---|---|---|---|
| `match` | `auto` \| `index` | `auto` | `index`: vertex *i* → vertex *i* (After Effects); mismatched counts are `path.morph_count` |
| `samples` | integer | `0` | with `auto`: resample both paths to this many evenly spaced vertices (smooths corners; higher is smoother between very different shapes) |
| key `firstVertex` | integer or `auto` | `auto` | on the **incoming** key: which of its vertices matches vertex 0 of the previous key; `auto` minimises travel; authored only (the normalizer rotates the key and drops the field) |

The `auto` algorithm: an open/closed mismatch closes the open path by duplicating its first vertex (`lint.morph_open_closed`); opposite orientations reverse B; the target count is `samples` or max(|A|, |B|); the smaller path is split at its longest segments' midpoints (shape unchanged; with `samples` both are resampled evenly, which smooths corners); for closed paths the cyclic shift minimising Σ|A[i] − B[i+k]|² is chosen; chains settle at the chain's largest count. Canonical form carries equal counts, so exporters never see a mismatch.

## 6. Paints and gradients

| Item | Fields (default) |
|---|---|
| `fill` | `color` `#FF0000` A (HDR allowed); `opacity` 100 A; `rule` `nonzero` \| `evenodd`; `blend` `normal`; `composite` `below` \| `above` (`above` draws over the paints earlier in the array) |
| `stroke` | `color` `#FFFFFF` A; `width` 2 A (px; 0 paints nothing); `opacity` 100 A; `lineCap` `butt` \| `round` \| `square`; `lineJoin` `miter` \| `round` \| `bevel`; `miterLimit` 4 A (≥ 1); `dashes` (list of px, each entry animatable; an odd count repeats); `dashOffset` 0 A (SVG semantics: animating upward moves dashes backwards); `taper`; `wave`; `blend`; `composite` |
| `gradientFill` | as `fill` with `gradient` instead of `color` |
| `gradientStroke` | as `stroke` with `gradient` instead of `color` |

`taper`: `startLength`, `endLength` (0; percent of the path or px per `lengthUnits`), `startWidth`, `endWidth` (0; percent of `width` at the ends), `startEase`, `endEase` (0–100; width curve `f(x) = x^(1 + 3·ease/100)`), `lengthUnits` `percent` | `pixels`. `wave`: `amount` (0; percent of `width`, 0–1000), `units` `pixels` | `cycles`, `wavelength` (40), `phase` (0, degrees; animate to travel). `wave` modulates the stroke **width** along the path (a waving centreline is `zigzag` with `points: "smooth"`). Strokes become filled outlines (taper and wave applied) rasterized with analytic coverage; a non-uniform group scale scales the stroke non-uniformly, as in After Effects.

**The gradient value** (also used by effects and `gradientOverlay`):

```jsonc
{ "type": "linear", "from": [-200, 0], "to": [200, 0], "highlightLength": 0, "highlightAngle": 0,
  "stops": [[0, "#3A1C71"], [0.5, "#D76D77"], [1, "#FFAF7B"]], "opacityStops": [[0, 1], [1, 1]], "midpoints": [0.5, 0.5],
  "interpolation": "oklab", "spread": "pad", "dither": true }
```

| Field | Default | Notes |
|---|---|---|
| `type` | `linear` | `linear`; `radial` (`from` = centre, the distance to `to` = radius); `angular` (conic, clockwise from the `to` direction, 0 → 1 over a turn); `diamond` (concentric diamonds with the vertex on the axis at `to`); `freeform` (`points: [{ at, color, spread }]`: each point's color weighted by `exp(−(d/spread)²)` and normalized, a soft mesh or aurora blend; `spread` in px, default 200; at most 64 points; `points` required (`doc.required`); points and colors animate through whole-gradient keys with the same point count; `stops` are still read by layer-style glows and overlays). `angular`/`diamond`/`freeform` export as linear ramps with a warning. A degenerate placement (`from` = `to`) paints the last stop everywhere. |
| `from`, `to` | `[0, 0]`, `[100, 0]` | animatable, spatial; group/layer space |
| `highlightLength` | 0 | radial focal offset, percent of the radius, −100–100 |
| `highlightAngle` | 0 | degrees |
| `stops` | black → white | `[position 0–1, colour]`, 2–64, non-decreasing; the whole array animates |
| `opacityStops` | fully opaque | `[position, alpha 0–1]`; independent ramp |
| `midpoints` | 0.5 each | the 50 % blend point between consecutive colour stops (one per gap) |
| `interpolation` | the comp's `color.interpolation` | `oklab`, `srgb`, `linear` |
| `spread` | `pad` | `pad`, `repeat`, `reflect` (beyond the ends) |
| `dither` | true | blue-noise dither at 8-bit output, per gradient |

Animating gradients: keys with different stop counts are resampled by the normalizer to the union of positions (a midpoint off 0.5 becomes a knee stop, `midpoints` dropped), info `gradient.stops_resampled`; more than 64 positions fall back to 64 even positions. Stop colours between keys mix in the comp's `color.interpolation`; between stops in the gradient's own `interpolation`.

## 7. Operators

Operators modify every path above them in the same group (nested groups' paths included).

| Item | Fields (default) | Notes |
|---|---|---|
| `trim` | `start` 0 A, `end` 100 A (percent of length), `offset` 0 A (degrees; 360 = one length), `mode` `simultaneously` \| `individually` | `start` > `end` wraps through the path start on closed paths (both spans on open ones); `individually` treats all paths as one long path in list order. The `drawOn`/`drawOff` presets and the `trimStart`/`trimEnd`/`trimOffset` shorthands target the first trim item, adding one as the last item if missing (also on shape-preset layers) |
| `repeater` | `copies` 3 A (0–1000; fractions fade the last copy), `offset` 0 A (shifts the progression; fractional interpolates), `composite` `below` \| `above`, `transform` `{ anchor [0,0], position [100,0], scale [100,100], rotation 0, startOpacity 100, endOpacity 100 }` A | copy *k* is transformed by `M^(k + offset)` (cumulative position/scale/rotation); opacity interpolates from start to end; duplicates paths too |
| `roundCorners` | `radius` 10 A | rounds corner vertices (zero tangents) only, clamped to half the adjacent segments |
| `offset` | `amount` 10 A (px; negative insets), `lineJoin` `miter` \| `round` \| `bevel`, `miterLimit` 4 A, `copies` 1 A (1–100), `copyOffset` 0 A | copy *k* is the input offset by `amount · (k + 1 + copyOffset)`; the original is not kept; self-intersections removed |
| `zigzag` | `size` 10 A (px amplitude), `ridges` 5 A, `per` `segment` \| `path`, `points` `corner` \| `smooth` | |
| `puckerBloat` | `amount` 0 A (−100–100: negative puckers, positive bloats) | one centre: the bounding box of all the group's live paths at the operator |
| `twist` | `angle` 0 A, `center` `[0, 0]` A | rotation proportional to the distance from `center`, the farthest bounding-box corner turning by `angle` |
| `wigglePaths` | `size` 10 A (−4096–4096), `detail` 3 A (0–10 subdivisions per segment), `points` `smooth` \| `corner`, `wigglesPerSecond` 2 A (0–1000; 0 = static), `correlation` 50 A (percent: 0 independent jitter, 100 rigid drift), `temporalPhase` 0 A, `spatialPhase` 0 A (degrees), `seed` 0 | deterministic seeded noise; baked per frame on export |
| `merge` | `mode` `merge` \| `add` \| `subtract` \| `intersect` \| `exclude` | `merge` = one compound path (the fill rule decides holes); the others are booleans in list order (the first path is the base); inputs read `nonzero`, open inputs closed; the result starts near the first input's start and runs in its direction; replaces the paths above |
| `feather` | `amount` 0 A (px, 0–1000), `direction` `outer` \| `inner` \| `both` | the coverage of every paint above it in the same group (earlier in the array, nested groups included) is convolved with a Gaussian of σ = `amount` / 2: `outer` keeps the shape solid and fades outside it, `inner` fades inward from the edge and paints nothing outside, `both` crosses half coverage on the edge. Group and repeater scale scale it; two feathers on one paint combine (σ² adds). Lottie drops it with a warning |

## 8. Authoring sugar

### 8.1 Shape presets

A shape layer with `shape` instead of `contents` builds a one-group `contents` from the preset plus paint shorthands.

```jsonc
{ "id": "pill", "type": "shape", "shape": "roundedRect", "size": [360, 96], "radius": 48, "fill": "$theme.color.surface" }
{ "id": "rule", "type": "shape", "shape": "line", "from": [-300, 0], "to": [300, 0], "stroke": { "color": "#FFF", "width": 4 } }
{ "id": "arrow", "type": "shape", "shape": "arrow", "from": [0, 0], "to": [240, 0], "head": 24, "stroke": { "width": 6, "color": "#FFF" } }
```

| `shape` | Fields (default) | Expands to |
|---|---|---|
| `rect` | `size`, `radius` (0), `position` | `rect` |
| `roundedRect` | `size`, `radius` (min side / 4), `position` | `rect` with `roundness` |
| `circle` | `radius`, `position` | `ellipse` |
| `ellipse` | `size`, `position` | `ellipse` |
| `polygon` | `sides`, `radius`, `roundness` | `polystar` polygon |
| `star` | `points`, `outer`, `inner`, `roundness` | `polystar` star |
| `line` | `from`, `to` | open `path` |
| `polyline` | `points` (array of `[x, y]`, or a `$data` list with `pointTransform`), `closed` (false), `smooth` (false; true = Catmull-Rom tangents) | `path` |
| `arrow` | `from`, `to`, `head` (px), `headAngle` (40) | shaft `path` plus a two-segment head, grouped |
| `arc` | `radius`, `startAngle`, `endAngle` | open cubic `path` |
| `ring` | `radius`, `thickness` | `ellipse` + `stroke` of width `thickness` |

Paint shorthands: `"fill": "#FFF"` → a fill item; `"stroke": { "color", "width", "lineCap", "lineJoin", "dashes", … }` → a stroke item (on top of the fill); `"gradient": { … }` → a `gradientFill`.

### 8.2 SVG import

```jsonc
{ "id": "logo", "type": "shape", "fromSvg": "logoAsset", "fit": { "width": 600 }, "origin": "center" }
{ "id": "logoDraw", "type": "shape", "fromSvg": "logoAsset", "fill": null, "stroke": { "color": "#FFF", "width": 4 } }
```

`fromSvg` names an `svg` asset parsed with usvg and converted: `<g>` → `group` (transform, opacity); `<path>`/`<rect>`/`<circle>`/`<ellipse>`/`<line>`/`<polyline>`/`<polygon>` → items (untransformed rect/circle/ellipse stay editable items); `fill`/`fill-opacity`/`fill-rule` → `fill`; stroke attributes incl. dashes → `stroke`; linear/radial gradients (transform baked) → gradient paints; `clipPath` → a `merge` intersect or a layer mask; `<mask>`, filters, `<pattern>`, `<image>`, `<text>` are dropped with a warning (`convert.svg_*`; convert text to outlines first). Ids derive from the SVG ids (sanitized) or indexes, so parts are targetable (`"target": "logo.contents.leaf"`). `fit`: `width`, `height`, or `box: [w, h]`, aspect kept. Paint overrides: `stroke` replaces every stroke (added where none); `fill` replaces every fill; `"fill": null` removes the fills (a draw-on logo). `"svg": "<svg …>…</svg>"` inlines art (≤ 64 KB) as an anonymous asset.

### 8.3 `fitTo`: auto-sizing boxes

```jsonc
{ "id": "bar", "type": "shape", "contents": [
    { "type": "rect", "roundness": 12, "fitTo": { "layer": "name", "padding": [28, 14] } },
    { "type": "fill", "color": "$theme.color.accent" } ] }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `layer` | layer id | — | the layer whose bounds to fit (any layer with content bounds); exactly one of `layer` / `layers` |
| `layers` | list of ids | — | the union of several layers' bounds |
| `span` | span id | none | with a text `layer`: only that span's bounds |
| `padding` | number, `[x, y]`, or `[top, right, bottom, left]` | `0` | px around the bounds |
| `includeExtents` | boolean | `false` | include stroke widths and descenders beyond the glyph box |
| `live` | boolean | `true` | measured every frame (follows text that types on); `false`: measured once at the first frame where every fitted layer is fully visible, written as static `size`/`position` |
| `minSize` | `[w, h]` | `[0, 0]` | |
| `fit` | `both` \| `width` \| `height` | `both` | which axes follow; the others keep the rect's own `size`/`position` |

The only auto-sizing construct (no layer-level `fitTo`, none on solids). The rect's own `size`/`position` are ignored on fitted axes (`lint.fitto_overrides_size`). The shape layer and the fitted layers may differ in parent, scale and rotation (evaluated through both world transforms). Canonical form keeps a live `fitTo` (evaluated by the renderer; exported as `sourceRectAtTime()` expressions).

### 8.4 `points` from data

`"points": "$data.series"` on a `polyline` preset or a `path` item takes `[x, y]` rows (longer rows use the first two values); `pointTransform` is a template per row with `$item` (the row) and `$index` (`"pointTransform": ["{{200 + $index * 60}}", "{{900 - $item[1] * 8}}"]`); `closed`, `smooth` apply. A row that is not two numbers is `data.bad_point`. The aliases `pointsTransform` and `transform` on the binding are accepted (deprecated).

## 9. Rendering notes

Exact analytic coverage (no supersampling, so thin lines stay stable in slow motion); paths flattened in f64 at 0.05 px tolerance at final resolution (always "continuously rasterized"); paints blend in the comp's working space; conservative per-item bounds let the compositor skip empty tiles.

## 10. Examples

`examples/07-shapes.json`: every item kind in use (groups with transforms and blend, all four shapes, `path` from `d` with subpaths, every paint incl. `taper`/`wave`/`dashes`, linear/radial/angular/diamond gradients with opacity stops and midpoints, every operator incl. a repeater grid and a boolean `merge`, a path morph with `firstVertex`), every shape preset with paint shorthands, `fromSvg` from the library logo with a `fill: null` draw-on, `fitTo` with `layers` and `fit: "width"`, and `points` from data. Checks with 0 errors; a `lint.paint_above_merge` warning is included on purpose to show the rule. Note the `underline` layer: a shape layer's default `position` is the comp centre, so a rect whose fitted axis is `width` keeps its own `position` y in layer space; the layer is placed at `[0, 0]` to make that y a comp coordinate.
