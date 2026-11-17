# Transition

18 ids. Parameters: [91-catalogue-transition.md](91-catalogue-transition.md). Transition effects hide a layer by `completion`: **0 = fully visible, 100 = fully hidden** (After Effects' convention). Key `completion` 100 → 0 to reveal, 0 → 100 to take a layer out. The scene-level transitions of spec 3 (`transition` on a layer, with presets) compile to these; use them when you want a preset and these when you want control.

| Effect | Use it for | Extra parameters |
|---|---|---|
| `transition.linearWipe` | A straight wipe at `angle` (90 = from the left), `feather` px. | |
| `transition.radialWipe` | Clock wipe: `startAngle`, `center`, `wipe` clockwise/counterclockwise/both, `feather`. | |
| `transition.venetianBlinds` | Slats of `width` perpendicular to `direction`, `feather`. | |
| `transition.gradientWipe` | Wipe through a luma pattern: the layer's own luma, or a `gradient` layer (`gradientSource`, `placement` tile/center/stretch), `softness` percent, `invert`. A hidden `generate.fractalNoise` solid as the gradient gives an organic dissolve. | |
| `transition.blockDissolve` | Blocks of `blockWidth` × `blockHeight` vanish in hashed order; `feather`, `softEdges`, `seed`. | |
| `transition.iris` | A `shape` (circle/square/diamond/star/heart/polygon/layer) about `center` shrinking to nothing; `points` (polygon, star), `rotation`, `feather`, `shapeLayer` + `shapeLayerSource` for `layer`. | |
| `transition.cardWipe` | 3D card flip grid: `transitionWidth`, `backLayer`, `rows`/`columns`, `cardScale`, `flipAxis`, `flipDirection`, `flipOrder`, `gradientLayer`, `timingRandomness`, `randomSeed`, camera, lighting, material and jitter groups (44 parameters, see the catalogue page). Drawn by the effect, not the comp's 3D. | |
| `transition.ccGlassWipe` | Refracting wipe toward `layerToReveal`: `gradientLayer`, `softness`, `displacementAmount`. | |
| `transition.ccTwister` | Ribbon twist about `axis` from `center` revealing `backside`, `shading`. | |
| `transition.pageTurn` | Page curl from `fold` in `foldDirection`: `foldRadius`, `lightDirection`, `render` frontAndBack/back/front, `backPage`, `backOpacity`, `paperColor`. No `completion`: animate `fold`. | |
| `transition.ccGridWipe` | Tiles closing from `center`: `rotation`, `border`, `tiles`, `shape` doors/radial/rectangular, `reverse`. | |
| `transition.ccImageWipe` | Ordered by a `layer`'s `property` (red…saturation): `borderSoftness`, `autoSoftness`, `blur`, `inverseGradient`. | |
| `transition.ccJaws` | Two jagged halves (`shape` spikes/roboJaw/block/waves) opening from `center` along `direction`: `height`, `width`. | |
| `transition.ccLightWipe` | A glowing edge of `color` (or `colorFromSource`) eating the layer from `center`: `intensity`, `shape` doors/round/square, `direction`, `reverse`. | |
| `transition.ccLineSweep` | Staggered slanted lines: `direction`, `thickness`, `slant`, `flipDirection`. | |
| `transition.ccRadialScaleWipe` | Radial scale-away from `center`, `reverse`. | |
| `transition.ccScaleWipe` | Stretches the layer away from `center` along `direction` by `stretch` 0–1000 (no `completion`). | |
| `transition.ccWarpoMatic` | Warps both layers by a `reactorLayer` while cross-fading to `layerToReveal`: `reactor`, `smoothness`, `warpAmount`, `warpDirection`, `blendSpan`. | |

Device: all CPU. `transition.ccGlassWipe` and `transition.ccWarpoMatic` reveal a second layer through `layerToReveal` (a hidden layer of the comp); the others only hide the layer they are on, so the layer below shows through.

## Patterns

**Reveal a title with a soft wipe.**

```json
{ "id": "wipe", "type": "transition.linearWipe",
  "params": { "completion": { "keys": [ { "t": 0.2, "v": 100, "ease": "expo.out" }, { "t": 1.0, "v": 0 } ] }, "angle": 90, "feather": 40 } }
```

**Organic dissolve.** A hidden solid `noise` with `generate.fractalNoise` (`scale` 40, `contrast` 150) and on the outgoing layer `transition.gradientWipe` `gradient: "noise"`, `softness` 20, `completion` 0 → 100.

**Iris on a logo.** `transition.iris` `shape: "circle"`, `feather` 30, `completion` 100 → 0 with `back.out`; for a custom silhouette `shape: "layer"` with `shapeLayer` a hidden shape layer.

**Scene cut with cards.** `transition.cardWipe` `rows` 4, `columns` 8, `flipAxis`, `backLayer` the incoming scene's comp layer (hidden), `completion` 0 → 100 over 0.8 s.

Full example: `examples/transition-family.motion.json`.
