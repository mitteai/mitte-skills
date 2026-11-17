# Transition: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-transition-1:start -->
### `transition.linearWipe`

After Effects: Linear Wipe · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `angle` | angle ° | 90 | — | A | Direction the front moves in (0 = up, 90 = right). |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Width of the soft edge in px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.radialWipe`

After Effects: Radial Wipe · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Clock wipes, pie-chart reveals.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `startAngle` | angle ° | 0 | — | A | Where the wipe starts (0 = up). |
| `center` | point `[x, y]` | `center` | — | A | Center of the wipe. |
| `wipe` | enum `clockwise` / `counterclockwise` / `both` | `clockwise` | — | — | Sweep direction. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Width of the soft edge in px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.venetianBlinds`

After Effects: Venetian Blinds · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Slats of `width` px perpendicular to `direction`, each closing over `completion` percent of its width, with a `feather` px soft edge.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `direction` | angle ° | 0 | — | A | Direction across the slats (0 = horizontal slats). |
| `width` | length px | 20 | ≥ 0 (clamped) | A | Slat period in px. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Width of the soft edge in px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.gradientWipe`

After Effects: Gradient Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Hides the pixels whose gradient luma (display-encoded, of the `gradient` layer placed by `placement`, or of the layer itself) is below `completion`, with a `softness` ramp; `invert` reverses the order.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `softness` | percent | 0 | 0–100 (soft) | A | Width of the ramp, percent of the luma range. |
| `gradient` | layer id | none | — | — | The layer whose luma orders the wipe (null = this layer). |
| `gradientSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `placement` | enum `tile` / `center` / `stretch` | `stretch` | — | — | How the gradient layer lines up with this one. |
| `invert` | boolean | false | — | — | Wipe from bright to dark instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.blockDissolve`

After Effects: Block Dissolve · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Blocks of `blockWidth` × `blockHeight` px (anchored at the layer origin) vanish in a hashed order as `completion` grows; `softEdges` anti-aliases block edges that fall between pixels (4 × 4 sub-samples), `feather` blurs the mask (Gaussian).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `blockWidth` | length px | 8 | ≥ 0 (clamped) | A | Block width in px. |
| `blockHeight` | length px | 8 | ≥ 0 (clamped) | A | Block height in px. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Gaussian softening of the mask in px. |
| `softEdges` | boolean | true | — | — | Anti-alias block edges between pixels. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `transition.iris`

After Effects: Iris Wipe / CC Shape Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

A `shape` (circle, square, diamond, star or regular polygon of `points`, heart, or the alpha of `shapeLayer`) about `center`, rotated by `rotation`, that covers the whole layer at `completion` 0 and shrinks to nothing at 100, with a `feather` px edge; pixels outside it are hidden.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `shape` | enum `circle` / `square` / `diamond` / `star` / `heart` / `polygon` / `layer` | `circle` | — | — | Shape of the iris. |
| `points` | integer | 5 | 3–64 (clamped) | A | Points of a polygon or star. |
| `center` | point `[x, y]` | `center` | — | A | Center of the iris. |
| `rotation` | angle ° | 0 | — | A | Rotation of the shape. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Width of the soft edge in px. |
| `shapeLayer` | layer id | none | — | — | The layer whose alpha is the shape (`layer`). |
| `shapeLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccGridWipe`

After Effects: CC Grid Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Grid of tiles closing from `center`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `center` | point `[x, y]` | `center` | — | A | Where the tiles vanish first. |
| `rotation` | angle ° | 0 | — | A | Rotation of the grid. |
| `border` | length px | 0 | ≥ 0 (clamped) | A | Soft edge of the shrinking tiles in px. |
| `tiles` | number | 10 | 1–500 (clamped) | A | Tiles across the layer's width. |
| `shape` | enum `doors` / `radial` / `rectangular` | `radial` | — | — | Order of vanishing about the center: a strip, a disc or a square. |
| `reverse` | boolean | false | — | — | Vanish from the outside in instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccRadialScaleWipe`

After Effects: CC Radial ScaleWipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Radial scale-away from `center`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `center` | point `[x, y]` | `center` | — | A | Center of the hole. |
| `reverse` | boolean | false | — | — | Shrink into the center instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccScaleWipe`

After Effects: CC Scale Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Stretches the layer away from `center` along `direction` (no `completion`: animate `stretch`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `stretch` | number | 0 | ≥ 0 (soft) | A | How far the content past the center line is stretched (0 = none). |
| `center` | point `[x, y]` | `center` | — | A | A point on the line the stretch starts from. |
| `direction` | angle ° | 90 | — | A | Direction of the stretch (90 = to the right). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccLightWipe`

After Effects: CC Light Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

A glowing edge of `color` that eats the layer from `center`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `center` | point `[x, y]` | `center` | — | A | Where the wipe starts. |
| `intensity` | percent | 100 | 0–1000 (soft) | A | Brightness of the glowing edge. |
| `shape` | enum `doors` / `round` / `square` | `round` | — | — | Shape of the wipe about the center. |
| `direction` | angle ° | 0 | — | A | Rotation of the shape (the strip of `doors` runs across it). |
| `colorFromSource` | boolean | false | — | — | Glow with the pixel's own color instead of `color`. |
| `color` | color | `#FFFFFF` | — | A | Color of the glow. |
| `reverse` | boolean | false | — | — | Hide the outside first instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccJaws`

After Effects: CC Jaws · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Two jagged halves opening from `center`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `center` | point `[x, y]` | `center` | — | A | A point on the cut. |
| `direction` | angle ° | 0 | — | A | Direction the halves move in (the cut runs across it). |
| `height` | percent | 50 | 0–100 (soft) | A | Tooth height, percent of the tooth width. |
| `width` | length px | 50 | ≥ 0 (clamped) | A | Tooth width in px. |
| `shape` | enum `spikes` / `roboJaw` / `block` / `waves` | `spikes` | — | — | Tooth profile. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccLineSweep`

After Effects: CC Line Sweep · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Staggered slanted lines sweeping across.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `direction` | angle ° | 0 | — | A | Direction of the sweep (0 = up, 90 = right). |
| `thickness` | length px | 20 | ≥ 0 (clamped) | A | Stripe thickness in px. |
| `slant` | length px, signed | 20 | any | A | Stagger between stripes in px (sign picks the leading end). |
| `flipDirection` | boolean | false | — | — | Reverse the stagger order. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccImageWipe`

After Effects: CC Image Wipe · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Wipe ordered by a layer's `property` (`transition.gradientWipe` is the luma-only After Effects one).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully hidden. |
| `borderSoftness` | percent | 0 | 0–100 (soft) | A | Width of the ramp, percent of the gradient range. |
| `autoSoftness` | boolean | true | — | — | Keep at least a slight ramp. |
| `layer` | layer id | none | — | — | The layer whose property orders the wipe (null = this layer). |
| `layerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `property` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `lightness` / `saturation` | `luminance` | — | — | Which value of the layer orders the wipe. |
| `blur` | length px | 0 | ≥ 0 (clamped) | A | Gaussian smoothing of the gradient in px. |
| `inverseGradient` | boolean | false | — | — | Wipe from bright to dark instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccGlassWipe`

After Effects: CC Glass Wipe · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Gradient-driven wipe that refracts the edge; needs a second layer to reveal ([7.6](#76-reading-other-layers)).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully replaced by `layerToReveal`. |
| `layerToReveal` | layer id | none | — | — | The layer shown where the wipe has passed, stretched to this one (null = nothing). |
| `layerToRevealSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `gradientLayer` | layer id | none | — | — | The layer whose luma orders the wipe, stretched to this one (null = this layer). |
| `gradientLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `softness` | percent | 10 | 0–100 (soft) | A | Width of the transition band, percent of the luma range (the gradient is also smoothed by a fifth of it in px). |
| `displacementAmount` | number | 10 | -100–100 (clamped) | A | Refraction in the band: how far its content is pushed along the gradient's slope (negative pulls). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccWarpoMatic`

After Effects: CC WarpoMatic · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Warps both layers by the reactor layer while cross-fading; needs a second layer ([7.6](#76-reading-other-layers)).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = fully replaced by `layerToReveal`. |
| `layerToReveal` | layer id | none | — | — | The layer shown where the warp has passed, stretched to this one (null = nothing). |
| `layerToRevealSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `reactorLayer` | layer id | none | — | — | The layer whose `reactor` map drives the warp, stretched to this one (null = this layer). |
| `reactorLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `reactor` | enum `brightness` / `contrastDifferences` / `localDifferences` | `brightness` | — | — | What drives the warp: the luma, its distance from the local mean, or its slope. |
| `smoothness` | number | 10 | 0–200 (clamped) | A | Gaussian smoothing of the reactor map (half of it in px). |
| `warpAmount` | number | 50 | -1000–1000 (clamped) | A | How far the content is pushed along the reactor map's slope (negative pulls). |
| `warpDirection` | enum `joint` / `opposing` / `twisting` | `joint` | — | — | Whether the revealed layer is pushed the same way as the outgoing one, the opposite way or across. |
| `blendSpan` | percent | 10 | 0–100 (soft) | A | Width of the blend between the two layers, percent of the reactor range. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.ccTwister`

After Effects: CC Twister · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Ribbon twist about `axis` that reveals `backside`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = untwisted, 100 = fully turned over (the back side). |
| `backside` | layer id | none | — | — | The layer on the back of the ribbon, stretched to this one (null = this layer, mirrored). |
| `backsideSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `shading` | boolean | true | — | — | Darken the ribbon as it turns edge-on. |
| `center` | point `[x, y]` | `center` | — | A | A point on the twist axis. |
| `axis` | angle ° | 45 | — | A | Direction of the twist axis. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.pageTurn`

After Effects: CC Page Turn · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Page curl from `fold`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `fold` | point `[x, y]` | `["0.7%", "0.7%"]` | — | A | Where the fold is; the page ahead of it along `foldDirection` is lifted. |
| `foldDirection` | angle ° | 315 | — | A | Direction the fold has travelled in (the lifted part lies ahead of it). |
| `foldRadius` | length px | 20 | ≥ 0 (clamped) | A | Radius of the curl in px. |
| `lightDirection` | angle ° | -45 | — | A | Where the light shading the curl comes from. |
| `render` | enum `frontAndBack` / `backPage` / `frontPage` | `frontAndBack` | — | — | Which sides of the page to draw. |
| `backPage` | layer id | none | — | — | The layer printed on the back of the page, stretched to this one (null = the page itself, seen through the paper). |
| `backPageSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `backOpacity` | percent | 75 | 0–100 (soft) | A | How much of the back's picture shows through `paperColor`. |
| `paperColor` | color | `#FFFFFF` | — | A | Color of the paper's back. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `transition.cardWipe`

After Effects: Card Wipe · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

3D card flip of a grid, drawn by the effect's own per-card homographies (EffectCraft's `card3d`: camera system, lighting, material), not the comp's 3D renderer.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | 0 = fully visible, 100 = every card turned over. |
| `transitionWidth` | percent | 50 | 1–100 (soft) | A | How much of the order turns at once (100 = all cards together). |
| `backLayer` | layer id | none | — | — | The layer on the backs of the cards, stretched to this one (null = the backs are invisible). |
| `backLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `rows` | integer | 8 | 1–200 (clamped) | A | Rows of cards. |
| `columns` | integer | 8 | 1–200 (clamped) | A | Columns of cards. |
| `cardScale` | number | 1 | 0.01–4 (clamped) | A | Scale of each card about its center (below 1 leaves gaps, above 1 overlaps the neighbors). |
| `flipAxis` | enum `x` / `y` / `random` | `x` | — | — | The axis each card turns about (`random`: hashed per card). |
| `flipDirection` | enum `positive` / `negative` / `random` | `positive` | — | — | Which way each card turns (`random`: hashed per card). |
| `flipOrder` | enum `leftToRight` / `rightToLeft` / `topToBottom` / `bottomToTop` / `topLeftToBottomRight` / `topRightToBottomLeft` / `bottomLeftToTopRight` / `bottomRightToTopLeft` / `gradient` | `leftToRight` | — | — | The order the cards turn in (`gradient`: by the luma of `gradientLayer` at each card's center, darkest first). |
| `gradientLayer` | layer id | none | — | — | For `flipOrder: gradient`, stretched to this layer (null = this layer). |
| `gradientLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `timingRandomness` | number | 0 | 0–1 (clamped) | A | How far each card's place in the order is randomized (0–1). |
| `randomSeed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `shading` | boolean | true | — | — | Darken the cards as they tilt. |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

<!-- gen:catalogue-transition-1:end -->
