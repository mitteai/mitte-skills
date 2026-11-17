# Keying & matte

20 ids (`key.*` and `matte.*`). Parameters: [91-catalogue-keying.md](91-catalogue-keying.md). Keyers turn colour into alpha; matte effects shape alpha that is already there. Most have no neutral value: disable them rather than zeroing them.

| Effect | Use it for | Neutral |
|---|---|---|
| `key.unmult` | Alpha from brightness, divided out: fire, flares, light leaks shot on black over anything. `threshold`. | — |
| `key.color` | Pixels within `tolerance` of `color` (encoded, per channel) go transparent; `edgeThin` (signed), `edgeFeather`. | — |
| `key.chroma` | The Keylight-class keyer: `screenColor`, `screenGain`, `screenBalance`, `despillBias`/`alphaBias`, `clipBlack`/`clipWhite`/`clipRollback`, `screenShrinkGrow` (signed), `screenSoftness`, `screenDespotBlack`/`White`, `replaceMethod` none/source/hardColor/softColor + `replaceColor`, `view` final/screenMatte/statusView. | — |
| `key.luma` | By encoded luma: `type` keyOutBrighter/keyOutDarker/keyOutSimilar/keyOutDissimilar, `threshold`, `tolerance`, `edgeThin`, `edgeFeather`. | — |
| `key.linearColor` | Distance to `color` in `match` rgb/hue/chroma, `tolerance`, `softness`, `keyOperation` keyColors/keepColors. | — |
| `key.difference` | Difference matte against a `layer` (`layerSource`): `tolerance`, `softness`, `blurBeforeDifference`. | `layer: null` |
| `key.colorDifference` | Two partial mattes (`partialA.*`, `partialB.*`, `matte.*`), `keyColor`, `colorMatchingAccuracy`, `view`. | — |
| `key.colorRange` | A box in `colorSpace` lab/yuv/rgb: `min`/`max` per axis, `fuzziness`. | — |
| `key.extract` | A `channel`'s range: `blackPoint`/`whitePoint` 0–255, `blackSoftness`/`whiteSoftness`, `invert`. | 0 / 255 |
| `key.innerOuter` | A matte from an inner (`foreground`) and an outer (`background`) mask path, `additionalForeground`/`Background` lists, `cleanupForeground`/`Background` strokes, `singleMaskHighlightRadius`, `edgeThin`, `edgeFeather`, `edgeThreshold`, `invertExtraction`, `blendWithOriginal`. | no `foreground` |
| `key.screen` | The small screen keyer: `screenColor`, `screenGain`, `screenBalance`, `despill`, `clipBlack`/`clipWhite`, `screenPreblur`, `screenShrinkGrow`, `screenSoftness`, `edgeColor`, `view`. | — |
| `key.ccWireRemoval` | Paint out the line `pointA`–`pointB`: `removalStyle` fade/frameOffset/displace/displaceHorizontal, `thickness`, `slope`, `mirrorBlend`, `frameOffset` (reads another frame). | — |
| `matte.set` | Alpha from another layer inside the stack: `source` layer (null = the layer itself), `sourceSource`, `channel` red/green/blue/alpha/luminance/hue/lightness/saturation/full/off, `invert`, `stretch`, `composite`, `premultiply`. | — |
| `matte.simpleChoker` | Distance-field `choke` (positive shrinks, negative grows). | `choke: 0` |
| `matte.choker` | Two stages of `geometricSoftness`/`choke` (−127…127)/`grayLevelSoftness`, `iterations`. | all 0 |
| `matte.spill` | Despill: `method` standard/ultra, `keyColor`, `suppression`. | `suppression: 0` |
| `matte.alphaLevels` | Levels on alpha only: `inBlack`, `inWhite`, `gamma`. | defaults |
| `matte.refine` | Soft-matte refinement (hair): `smooth`, `feather`, `choke`, `shiftEdge`, `reduceChatter` (reads neighbouring frames), `decontaminate` + `decontaminationAmount`, `motionBlur`, `radius` ≤ 64. | — |
| `matte.refineHard` | Hard-matte sibling: `smooth`, `feather`, `choke`, `reduceChatter`, `useMotionBlur` + `motionBlur.*`, `decontaminate` + `decontamination.*`. | — |
| `matte.keyCleaner` | After a keyer: `additionalEdgeRadius`, `reduceChatter`, `alphaContrast` 100–500, `strength`. | — |

Device: `key.unmult`, `key.color`, `key.luma`, `key.linearColor`, `matte.spill`, `matte.alphaLevels` lower to the device.

## Patterns

**Green screen.** In order: `key.chroma` (`screenColor` sampled from the plate, `clipBlack` 10, `clipWhite` 90, `screenShrinkGrow` −1), `matte.keyCleaner`, `matte.spill` (`keyColor` the same green). Check the matte with `view: "screenMatte"` in a `motion.frames` still, then switch back to `final`.

```json
"effects": [
  { "id": "key", "type": "key.chroma", "params": { "screenColor": "#2AA84A", "clipBlack": 12, "clipWhite": 88, "screenSoftness": 1 } },
  { "id": "clean", "type": "matte.keyCleaner", "params": { "additionalEdgeRadius": 2 } },
  { "id": "spill", "type": "matte.spill", "params": { "method": "ultra", "keyColor": "#2AA84A", "suppression": 100 } }
]
```

**Stock on black (fire, sparks, leaks).** `key.unmult` and the layer's `blend: "add"` or `"screen"`; `threshold` lifts the noise floor.

**A matte before a glow.** `matte.set` with `source` a hidden shape layer, then `light.glow`: the glow blooms from the matted content, which a track matte (applied after effects) cannot do.

**Choke an AI matte.** `matte.simpleChoker` `choke` 1.5 then `matte.refine` `feather` 20, `decontaminate: true`.

Full example: `examples/keying-family.motion.json` (keys on generated plates; no footage needed).
