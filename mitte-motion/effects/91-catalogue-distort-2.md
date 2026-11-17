# Distort: every parameter (part 2 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-distort-2:start -->
### `distort.ccRipplePulse`

After Effects: CC Ripple Pulse · Phase: P2 · Status: implemented · Tiling: tiled · Reads: parameter history · Reads time: no · Device: CPU

Rings emitted by the history of `pulseLevel` over the last `timeSpan` seconds (`Deps::param_samples`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Where rings start. |
| `pulseLevel` | number | 0 | — | A | Animate it: each change emits a ring. |
| `timeSpan` | number | 1 | ≥ 0.01 (clamped) | A | Seconds a ring lives (and crosses half the layer). |
| `amplitude` | number | 100 | — | A | Displacement strength, percent. |
| `renderBump` | boolean | false | — | — | Shade the ring's slopes. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.reshape`

After Effects: Reshape · Phase: P2 · Status: implemented · Tiling: tiled · Reads: mask paths · Reads time: no · Device: CPU

Warps the source mask's region onto the destination mask; needs mask paths as parameters, like `generate.stroke`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `sourceMask` | mask id | none | — | — | Mask id of the outline that moves. |
| `destinationMask` | mask id | none | — | — | Mask id of the outline it moves onto. |
| `boundaryMask` | mask id | none | — | — | Mask id of a closed outline outside which nothing moves (none = the whole layer). |
| `percent` | percent | 100 | 0–100 (soft) | A | How far the source outline moves toward the destination. |
| `elasticity` | enum `stiff` / `lessStiff` / `belowNormal` / `normal` / `aboveAverage` / `loose` / `liquid` / `superFluid` | `stiff` | — | — | How quickly the warp falls off away from the outlines. |
| `interpolation` | enum `discrete` / `linear` / `smooth` | `linear` | — | — | The fade toward the boundary: discrete and linear fade linearly, smooth eases. |
| `correspondencePoints` | list of `[[sx, sy], [dx, dy]]` | `[]` | — | A | Pairs pinning a point of the source outline to a point of the destination outline. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-distort-2:end -->
