# Perspective: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-perspective-1:start -->
### `perspective.sphere`

After Effects: CC Sphere · Phase: P3 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Wraps the layer onto a sphere (planets, globes, spinning logo balls); ray-cast per pixel with antialiasing.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `rotation` | angle3d `[x°, y°, z°]` | `[0, 0, 0]` | — | A | Rotation of the texture on the sphere about x, y and z (degrees). |
| `radius` | length px | 120 | ≥ 0 (clamped) | A | Radius of the sphere (px). |
| `offset` | point `[x, y]` | `center` | — | A | Center of the sphere. |
| `render` | enum `full` / `outside` / `inside` | `full` | — | — | The front, the inside of the back, or both. |
| `light` | object (group of the dotted parameters below) | none | — | — | The light: `intensity`, `color`, `height`, `direction`. |
| `light.intensity` | percent | 100 | 0–400 (soft) | A | Light intensity. |
| `light.color` | color | `#FFFFFF` | — | A | Light color. |
| `light.height` | number | 50 | -90–90 (clamped) | A | Light elevation above the layer plane (degrees). |
| `light.direction` | angle ° | -45 | — | A | Direction the light comes from (0 = up, clockwise). |
| `shading` | object (group of the dotted parameters below) | none | — | — | The surface: `ambient`, `diffuse`, `specular`, `roughness`, `metal`, `reflective`, `reflectionMap`. |
| `shading.ambient` | percent | 20 | 0–200 (soft) | A | Unlit share of the texture's color. |
| `shading.diffuse` | percent | 80 | 0–200 (soft) | A | Lit share of the texture's color. |
| `shading.specular` | percent | 20 | 0–200 (soft) | A | Strength of the highlight. |
| `shading.roughness` | number | 0.05 | 0.001–0.5 (clamped) | A | Spread of the highlight. |
| `shading.metal` | percent | 100 | 0–100 (soft) | A | How much the highlight takes the texture's color (0 = the light's). |
| `shading.reflective` | percent | 0 | 0–100 (soft) | A | How much of the reflection map the surface mirrors. |
| `shading.reflectionMap` | layer id | none | — | — | An equirectangular environment the surface mirrors (null = none). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.cylinder`

After Effects: CC Cylinder · Phase: P3 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Implemented: ray-cast against the rotated cylinder, seen orthographically; `position`'s z does not show; the cylinder is open (no end caps).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | percent | 100 | 0–1000 (soft) | A | Circumference of the cylinder in percent of the layer's width. |
| `position` | point3d `[x, y, z]` | `center` | — | A | Center of the cylinder (x, y in layer pixels; z, the depth, does not show in the orthographic view). |
| `rotation` | angle3d `[x°, y°, z°]` | `[0, 0, 0]` | — | A | Rotation of the cylinder about x, y (its spin) and z (degrees). |
| `render` | enum `full` / `outside` / `inside` | `full` | — | — | The front, the inside of the back, or both. |
| `light` | object (group of the dotted parameters below) | none | — | — | The light: `intensity`, `color`, `height`, `direction`. |
| `light.intensity` | percent | 100 | 0–400 (soft) | A | Light intensity. |
| `light.color` | color | `#FFFFFF` | — | A | Light color. |
| `light.height` | number | 50 | -90–90 (clamped) | A | Light elevation above the layer plane (degrees). |
| `light.direction` | angle ° | -45 | — | A | Direction the light comes from (0 = up, clockwise). |
| `shading` | object (group of the dotted parameters below) | none | — | — | The surface: `ambient`, `diffuse`, `specular`, `roughness`, `metal`, `reflective`, `reflectionMap`. |
| `shading.ambient` | percent | 20 | 0–200 (soft) | A | Unlit share of the texture's color. |
| `shading.diffuse` | percent | 80 | 0–200 (soft) | A | Lit share of the texture's color. |
| `shading.specular` | percent | 20 | 0–200 (soft) | A | Strength of the highlight. |
| `shading.roughness` | number | 0.05 | 0.001–0.5 (clamped) | A | Spread of the highlight. |
| `shading.metal` | percent | 100 | 0–100 (soft) | A | How much the highlight takes the texture's color (0 = the light's). |
| `shading.reflective` | percent | 0 | 0–100 (soft) | A | How much of the reflection map the surface mirrors. |
| `shading.reflectionMap` | layer id | none | — | — | An equirectangular environment the surface mirrors (null = none). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.bevelAlpha`

After Effects: Bevel Alpha · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Signed-distance-based bevel (smooth on any shape).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `edgeThickness` | length px | 2 | ≥ 0 (clamped) | A | Width of the bevel in px. |
| `lightAngle` | angle ° | -60 | — | A | Direction the light comes from (0 = up, clockwise). |
| `lightColor` | color | `#FFFFFF` | — | A | Color of the highlight. |
| `lightIntensity` | number | 0.4 | 0–1 (clamped) | A | Strength of the highlight and shadow. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.bevelEdges`

After Effects: Bevel Edges · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `edgeThickness` | number | 0.1 | 0–0.5 (clamped) | A | Bevel width as a fraction of the shorter layer side. |
| `lightAngle` | angle ° | -60 | — | A | Direction the light comes from (0 = up, clockwise). |
| `lightColor` | color | `#FFFFFF` | — | A | Color of the highlight. |
| `lightIntensity` | number | 0.25 | 0–1 (clamped) | A | Strength of the highlight and shadow. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.dropShadow3d`

After Effects: Radial Shadow / Drop Shadow in 3D · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#000000` | — | A | Shadow color. |
| `opacity` | percent | 50 | 0–100 (soft) | A | Shadow opacity. |
| `lightSource` | point3d `[x, y, z]` | `["30%", "20%"]` | — | A | The light the shadow is cast from (z ignored in 2D). |
| `projectionDistance` | number | 10 | 0–1000 (clamped) | A | How far the shadow is thrown (percent of the distance to the light). |
| `softness` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent in px (σ = softness / 3). |
| `render` | enum `regular` / `glassEdge` | `regular` | — | — | The whole alpha, or its edge band. |
| `colorInfluence` | percent | 0 | 0–100 (soft) | A | How much of the layer's own color the shadow takes. |
| `shadowOnly` | boolean | false | — | — | Output only the shadow. |
| `resizeLayer` | boolean | false | — | — | Let the shadow extend past the layer rect. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.ccEnvironment`

After Effects: CC Environment · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Reflection-maps the environment layer onto the layer's luminance/alpha relief (EffectCraft's construction; no comp camera).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `environment` | layer id | none | — | — | The environment layer (null = this layer). |
| `environmentSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `mapping` | enum `spherical` / `probe` / `verticalCross` | `spherical` | — | — | How the map wraps the sphere of directions. |
| `filterEnvironment` | boolean | true | — | — | Soften the environment map. |
| `height` | number | 10 | 0–100 (clamped) | A | Relief height. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `perspective.3dGlasses`

After Effects: 3D Glasses · Phase: P4 · Status: not implemented (P4: `effect.unavailable`)

Anaglyph; kept for parity only.

No parameters are registered: the engine answers `effect.unavailable` (the message names the phase).

<!-- gen:catalogue-perspective-1:end -->
