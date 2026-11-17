# Light & glow

11 ids. Parameters: [91-catalogue-light.md](91-catalogue-light.md). Glows are physically based blooms in linear light: a bright core, a long soft tail, saturated colour. They read HDR values, so a particle layer or a text with `fill` above 1 glows more than one at 1.

| Effect | Use it for | Neutral |
|---|---|---|
| `light.glow` | The glow. `threshold` (working-space luminance; > 1 allowed) with a soft `knee`, `radius` px, `intensity`, `exposure` stops, `falloff` `inverseSquare`/`gaussian`/`exponential`, `tint` + `tintMode` `multiply`/`colorize`/`gradient` (with `gradient` from core to edge), `chromatic` −1…1 (red wider, blue tighter), `source` `layer`/`alpha`/`colorKey` (+ `keyColor`, `keyTolerance`), `composite` `add`/`screen`/`over`/`glowOnly`, `tonemap` (soft-clip above 0.8), `preserveColor`, `dirt.amount`/`dirt.scale` (accepted; the texture is P2). | `intensity: 0` |
| `light.bloom` | A whole-frame cinematic bloom on an adjustment layer: only values above `threshold` 1.0 bloom (`knee`, `radius`, `intensity`). | `intensity: 0` |
| `light.rays` | God rays / Shine: radial streaks of the thresholded source toward `center` (`length` percent of each pixel's distance, capped 95), `intensity`, `threshold`, `tint`, `colorize` gradient, `boost` stops, `shimmer.amount`/`detail`/`phase`, `composite`, `sourceAlpha`. | `intensity: 0` |
| `light.godrays3d` | `light.rays` plus `center3d`: on a 3D layer projected through the camera onto the layer's plane; on a 2D layer its x, y. | `intensity: 0` |
| `light.flare` | Procedural lens flare: `center` (or `center3d`), `preset` `prime50`/`zoom105`/`anamorphic`/`spotlight`/`sun`/`custom`, `brightness`, `scale`, `color`, `elements` (custom: `{ kind: glow/ring/streak/ghost/iris/starburst/hoop, position −1…2, size, color, intensity, shape, softness }`), `occlusion` layer dims it, `blend` (add). | `brightness: 0` |
| `light.leak` | Drifting overexposed light blotches (procedural, seeded): `speed`, `colors` gradient, `intensity`, `scale`, `position`, `softness`; animates with time. | `intensity: 0` |
| `light.energy` | Saber-style stroke of a path with a hot core and a big glow: `path` = a mask id, `"layerAlpha"` (the alpha's edge) or `"textOutlines"`; `coreColor`/`glowColor`, `coreSize`/`glowSize`, `glowIntensity`, `start`/`end`/`offset` percent (animate `end` for a draw-on), `distortion.amount`/`size`/`speed`/`octaves`, `flicker`, `taper.start`/`end`, `composite` `add`/`over`/`energyOnly`. | — |
| `light.neon` | Neon tube on the layer's outline: `color`, `tubeWidth`, `glow`, `flicker.amount`/`rate`, `off` (hold-animatable: blink the sign). | — |
| `light.ccLightBurst` | Radial burst of the layer's own pixels from `center`: `intensity`, `rayLength`, `burst` `straight`/`fade`/`center`, `setColor` + `color`. | `intensity: 0` |
| `light.ccLightSweep` | A light band swept across the layer with an edge highlight (logo sheens): `center`, `direction`, `shape` `linear`/`smooth`/`sharp`, `width`, `sweepIntensity`, `edgeIntensity`, `edgeThickness`, `lightColor`, `lightReception` `add`/`composite`/`cutout`. Animate `center` across the logo. | `sweepIntensity: 0` + `edgeIntensity: 0` |
| `light.ccSpotlight` | A 2D spotlight from `from` toward `to` (`height`, `coneAngle` 0.1–89.9, `edgeSoftness`, `color`, `intensity`, `render` `light`/`lightOnly`). | — |

Device: `light.glow` and `light.bloom` lower to GPU passes; the rest are CPU.

## Patterns

**Glow a title in.** Key `intensity` from 0 (skipped) to its value; keep `threshold` below the fill's luminance or nothing glows (a `#FFFFFF` fill is luminance 1.0; `threshold: 0.6` glows it, `1.0` does not). For a coloured halo on white text use `tintMode: "colorize"` with `tint`.

```json
{ "id": "glow", "type": "light.glow",
  "params": { "threshold": 0.5, "knee": 0.3, "radius": 120, "falloff": "inverseSquare", "tint": "#7C5CFF", "tintMode": "colorize",
              "intensity": { "keys": [ { "t": 0.3, "v": 0, "ease": "expo.out" }, { "t": 1.1, "v": 1.6 } ] } } }
```

**Bloom the whole frame.** An adjustment layer at the top with `light.bloom`; only HDR values (particles with `add` blend, a `color.exposure` push, fills above 1) bloom, so the body of the design stays crisp.

**Rays behind a logo.** `light.rays` with `center` pinned to the logo's centre (a number, not `"center"`, when the layer's bounds grow), `length` 60–80, `boost` 1–2 stops, `shimmer.amount` 30 with `shimmer.phase` keyed for animated streaks; `composite: "add"`.

**Draw-on energy outline.** `light.energy` with `path: "textOutlines"` on a text layer, `end` keyed 0 → 100, `composite: "energyOnly"` and the text's own fill faded in afterwards.

**Sheen across a logo.** `light.ccLightSweep` with `center` keyed from `["-20%", "50%"]` to `["120%", "50%"]` over 0.6 s, `direction` −30, `width` 60.

Full example: `examples/light-family.motion.json`.
