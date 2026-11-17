# Utility and expression controls

26 ids (`control.*` and `utility.*`). Parameters: [91-catalogue-utility.md](91-catalogue-utility.md). `utility.shader` has its own pages: [30-shader.md](30-shader.md).

## Expression controls

Eight effects that carry a value and touch no pixels. They are the only effects allowed on `null`, `camera` and `light` layers. Expressions read them as `effect("id")("value")` (also by `name`, and After Effects' display names `"Slider"`, `"Angle"`, `"Point"`, `"3D Point"`, `"Color"`, `"Checkbox"`, `"Layer"`, `"Menu"` as aliases, spec 11); components expose them as parameters (spec 12).

| Effect | `value` | Extra |
|---|---|---|
| `control.slider` | number (0), animatable | `min`, `max`: UI hints only |
| `control.angle` | angle ° (0), animatable | |
| `control.point` | point `[x, y]`, animatable | |
| `control.point3d` | point3d `[x, y, z]`, animatable | |
| `control.color` | color, animatable | |
| `control.checkbox` | boolean (false), hold-animatable | |
| `control.layer` | layer id or null, static | |
| `control.dropdown` | integer, 1-based (1), hold-animatable | `items`: list of strings |

```json
{ "id": "rig", "type": "null", "position": [960, 540],
  "effects": [ { "id": "speed", "type": "control.slider", "params": { "value": { "keys": [ { "t": 0, "v": 0 }, { "t": 2, "v": 100 } ] } } } ] }
```
and on another layer: `"rotation": { "expr": "thisComp.layer('rig').effect('speed')('value') * 3.6" }`.

## Utility effects

| Effect | Use it for | Neutral |
|---|---|---|
| `utility.growBounds` | `pixels` of extra buffer. Rarely needed (bounds grow automatically); kept for After Effects import. | — |
| `utility.applyLut` | Alias of `color.lut` (same parameters). | `amount: 0` |
| `utility.colorProfile` | Convert `inputSpace` → `outputSpace` inside the stack with `intent`. | same spaces |
| `utility.hdrCompander` | `mode` compress/expand, `gain`, `gamma` (invertible pair). | — |
| `utility.hdrHighlightCompression` | Roll values above 1.0 into range by `amount`. | `amount: 0` |
| `utility.removeColorMatting` | Un-matte footage premultiplied against `backgroundColor`; `clipHdr`. | — |
| `utility.channelCombiner` | `source` rgbToHls/hlsToRgb/rgbToYuv/yuvToRgb/lightness/hue/saturation/luminance/maxRgb/minRgb/red/green/blue/alpha/straightAlpha/gray, `useSecondLayer`, `from`/`to`, `invert`. | — |
| `utility.setChannels` | Per output channel a `source` layer + `channel`. | — |
| `utility.shiftChannels` | `takeAlphaFrom`, `takeRedFrom`, `takeGreenFrom`, `takeBlueFrom` enums. | identity |
| `utility.minMax` | `operation` minimum/maximum/minThenMax/maxThenMin over `radius`, `channel`, `direction`. | `radius: 0` |
| `utility.arithmetic` | Per-channel `operator` (and/or/xor/add/subtract/difference/min/max/blockAbove/blockBelow/slice/multiply/screen) with `redValue`/`greenValue`/`blueValue` 0–255, `clip`. | add 0 |
| `utility.blend` | Blend with `blendWithLayer` by `mode` crossfade/colorOnly/tintOnly/darkenOnly/lightenOnly, `blendWithOriginal`, `ifLayerSizesDiffer`. | `blendWithOriginal: 100` |
| `utility.calculations` | Photoshop Calculations: `inputChannel`, `invertInput`, `secondLayer` + `secondLayerChannel`/`Opacity`/`invertSecondLayer`/`stretchSecondLayerToFit`, `blendingMode`, `preserveTransparency`. | — |
| `utility.ccComposite` | Composite the layer's unprocessed source (`original` layer, default the effect's own input) back over the chain by `compositeOriginal` (16 modes), `opacity`, `rgbOnly`. | — |
| `utility.compoundArithmetic` | Layer-to-layer arithmetic with `secondSource`: `operator` (15), `operateOnChannels` rgb/argb/alpha, `overflowBehavior` clip/wrap/scale, `stretchSecondSourceToFit`, `blendWithOriginal`. | copy |
| `utility.solidComposite` | Composite over a solid `color`: `sourceOpacity`, `opacity`, `blendingMode`. | `opacity: 0` |
| `utility.ccOverbrights` | Paint pixels above 1.0 in `highlightColor` by `channel` (a diagnostic). | — |
| `utility.shader` | Custom WGSL kernel, GPU only: [30-shader.md](30-shader.md). | — |

Device: `utility.arithmetic`, `utility.solidComposite` and `utility.applyLut` lower to the device; `utility.shader` is GPU only; the rest are CPU.

## The 38 blend modes

Used by the `mode`/`blend`/`blendingMode` parameters of kind *blend mode* and by an instance's `blend.mode`: `normal`, `dissolve`, `dancingDissolve`, `darken`, `multiply`, `colorBurn`, `classicColorBurn`, `linearBurn`, `darkerColor`, `add`, `lighten`, `screen`, `colorDodge`, `classicColorDodge`, `linearDodge`, `lighterColor`, `overlay`, `softLight`, `hardLight`, `linearLight`, `vividLight`, `pinLight`, `hardMix`, `difference`, `classicDifference`, `exclusion`, `subtract`, `divide`, `hue`, `saturation`, `color`, `luminosity`, `stencilAlpha`, `stencilLuma`, `silhouetteAlpha`, `silhouetteLuma`, `alphaAdd`, `luminescentPremul`. Rows whose enum is narrower (`utility.solidComposite` 12 modes, `color.colorLink` 13) list their own values in the catalogue.

Full example: `examples/utility-family.motion.json`.
