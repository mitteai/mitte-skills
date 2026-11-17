# Distort (including glass and the backdrop rules)

35 ids. Parameters: [91-catalogue-distort-1.md](91-catalogue-distort-1.md), [91-catalogue-distort-2.md](91-catalogue-distort-2.md). Distortions resample the input: bicubic at `best` quality (Lanczos 3 when the layer sets `sampling: "lanczos"`), bilinear at `antialiasing: "low"` or in draft, with mip prefiltering when they minify.

| Effect | Use it for | Neutral |
|---|---|---|
| `distort.transform` | A transform inside the stack (before a glow, say) with its own motion blur: `anchor`, `position`, `uniformScale` + `scale` or `scaleX`/`scaleY`, `skew`, `skewAxis`, `rotation`, `opacity`, `useCompShutterAngle`, `shutterAngle`. Its blur samples its own parameters at shutter sub-times. | defaults |
| `distort.cornerPin` | Homography to four `topLeft`/`topRight`/`bottomLeft`/`bottomRight` points (screen replacements; tracking writes these, [62-tracking-documents.md](62-tracking-documents.md)). | the layer's corners |
| `distort.meshWarp` | Bezier patch mesh: `rows`, `columns`, `quality`, `vertices` list of points (keyed per item), `tangents`. | the grid |
| `distort.bezierWarp` | Four corner vertices + 8 tangents, `quality`. | — |
| `distort.displacement` | Displace by a `map` layer: `mapSource`, `horizontal`/`vertical` channel (red/green/blue/alpha/luminance/hue/lightness/saturation/full/half/off), `maxHorizontal`/`maxVertical` px, `fit` center/stretch/tile, `wrap`, `expandOutput`. Map value 0.5 = no displacement. | max 0 |
| `distort.turbulent` | Turbulent Displace: `type` turbulent/bulge/twist/…Smoother/vertical/horizontal/cross, `amount`, `size`, `offset`, `complexity`, `evolution` + `cycleEvolution`/`cycle`, `randomSeed`, `pinning` (none/all/horizontal/vertical/…/…Locked), `resizeLayer`. | `amount: 0` |
| `distort.waveWarp` | `waveType` sine/square/triangle/sawtooth/circle/semicircle/uncircle/noise/smoothNoise, `height`, `width`, `direction`, `speed` cycles/s (time-dependent), `pinning`, `phase`. | `height: 0` |
| `distort.ripple` | Concentric waves from `center`: `radius` percent, `type` asymmetric/symmetric, `speed`, `width`, `height`, `phase`. | `height: 0` |
| `distort.bulge` | `center`, `radiusX`/`radiusY`, `height` −4…4, `taper`, `pinEdges`. | `height: 0` |
| `distort.twirl` | `angle`, `radius` percent (50 reaches the edges), `center`. | `angle: 0` |
| `distort.spherize` | Sphere of `radius` px about `center`. | `radius: 0` |
| `distort.polar` | `conversion` rectToPolar/polarToRect, `interpolation` percent. | `interpolation: 0` |
| `distort.offset` | Wrapping `shift` (seamless scrolling), `blend`. | `shift: [0, 0]` |
| `distort.motionTile` | Tile the layer: `center`, `tileWidth`/`tileHeight`, `outputWidth`/`outputHeight` (grows the output), `mirrorEdges`, `phase`, `horizontalPhaseShift`. | defaults |
| `distort.mirror` | Reflect across the line through `center` at `angle`. | — |
| `distort.kaleidoscope` | `mirroring` dia/octo/cross/wheel/tri, `size`, `rotation`, `center` (`floatingCenter` accepted, ignored). | — |
| `distort.magnify` | A `circle`/`square` lens of `size` at `center`, `magnification` percent, `link`, `feather`, `opacity`, `scaling` standard/softSharp/scatter, `blending` (or `none`). | `magnification: 100` |
| `distort.lens` | Barrel/pincushion: `fov` 0–179, `reverse`, `center`, `fovOrientation`, `resizing` off/max2x/max4x/unlimited. | `fov: 0` |
| `distort.liquify` | `strokes` list `{ points, size, pressure, mode push/twirl/pucker/bloat }` in layer px, `distortion` percent; at most 64 strokes of 1,024 points. | no strokes |
| `distort.smear` | Drag `sourceMask` within `boundaryMask` by `offset`, `rotation`, `scale`, `stretch`. | either mask unset |
| `distort.reshape` | Warp `sourceMask` onto `destinationMask` inside `boundaryMask`: `percent`, `elasticity`, `interpolation`, `correspondencePoints`. | `percent: 0` |
| `distort.warp` | Photoshop warp `style` (arc…twist), `axis`, `bend`, `horizontalDistortion`, `verticalDistortion`. | `bend: 0` |
| `distort.ccFlo` | Two knots (`knot1`/`knot2`, `amount1`/`amount2`), `tileEdges`, `falloff`. | amounts 0 |
| `distort.ccBend` | `bend`, `start`/`end`, `renderPrestart`, `distort`. | `bend: 0` |
| `distort.ccBender` | `amount` −200…200, `style` bend/marilyn/sharp/boxer, `adjustToDistance`, `top`, `base`. | `amount: 0` |
| `distort.ccBlobbylize` | Lit blobs from `blobLayer`'s `property`: `softness`, `cutAway`, `light.*`, `shading.*`. | — |
| `distort.ccGriddler` | `horizontalScale`, `verticalScale`, `tileSize` px, `rotation`, `cutTiles`. | defaults |
| `distort.ccRipplePulse` | Rings emitted when `pulseLevel` changes (keyed), over `timeSpan`, `amplitude`, `renderBump`. Reads the parameter's history. | constant `pulseLevel` |
| `distort.ccScatterize` | `scatter`, `rightTwist`, `leftTwist`, `transferMode`. | `scatter: 0` |
| `distort.ccSlant` | `slant`, `stretching`, `height`, `floor`. | `slant: 0` |
| `distort.ccSmear` | Drag pixels from `from` toward `to`: `reach`, `radius`. | `reach: 0` |
| `distort.ccSplit` / `distort.ccSplit2` | A slit between `pointA` and `pointB`: `split` (or `split1`/`split2`). | `split: 0` |
| `distort.ccTiler` | Scaled copies: `scale`, `center`, `blendWithOriginal`. | `scale: 100` |
| `distort.glass` | The backdrop refraction effect, below. | — |

Device: `distort.offset` and `distort.waveWarp` lower to the device; the rest are CPU. `distort.glass` makes the job CPU.

## Glass and the backdrop rules

`distort.glass` is the one **backdrop** effect: it reads what is composited **below** the layer in the comp, refracts it through a pane shaped by the layer's alpha (normalized to its largest value, so a translucent fill still makes a whole pane), with a rounded bevel (`normalSource: bevel`: `bevelSize`, `bevelProfile` round/linear/smooth/squircle), or a `normalLayer` height map (gray: luma × `thickness`) or tangent-space normal map (coloured; x right in red, y up in green; the pane is flat where the map is transparent), or `flat`; `normalKind` (`auto` | `normal` | `height`) says which the layer is (`auto`: a normal map when at least half its opaque pixels are coloured). Parameters: `refraction` 1–3, `thickness` px (how deep the refracted ray travels; the bevel's own height is its `bevelSize`, so `thickness: 0` is an unbent pane that keeps its highlight and rim), `dispersion` 0–0.5 (red's index down, blue's up), `frost` px (a Gaussian radius like `blur.gaussian`), `backdrop` `below` or `layer` + `backdropLayer`, `tint` (its alpha is the strength), `saturation`, `specular` group (`intensity`, `angle`, `size`, `rim`), `shadow` group (`opacity`, `softness`, `offset`). The layer's colour is not used.

Rules the renderer enforces:

- It must be the **last** effect of the layer (`effect.backdrop_not_last`, error). Normalization moves generated effects (a tween's `_blur`) in front of it.
- The layer must be **2D**, not in a 3D run, not an adjustment layer (`effect.backdrop_not_2d`, warning: skipped).
- It runs in **comp space** at the compositing step: lengths (`bevelSize`, `frost`, `shadow.softness`, `thickness`) arrive in comp pixels (layer px × the layer's mean scale); the layer's `opacity` and matte apply to its output; under motion blur its parameters are the frame sample's.
- Its `layer` parameters (`normalLayer`, `backdropLayer`) are read as comp-space images through their full pipeline. One its settings need but cannot read (unset, a missing id, the glass's own layer) is `effect.param_value` at that parameter, and the pane renders without it.
- A layer read as an input elsewhere (a matte source, a displacement map) is read without its glass effect.
- The backdrop is read over the effect's input region; past the frame it repeats the frame's edge pixels.
- A document with a glass effect renders on the CPU (the GPU walk declines it).
- A failing glass effect is `effect.param_value` and the layer composites without it.

```json
{ "id": "pill", "type": "shape", "shape": "roundedRect", "size": [520, 160], "radius": 80, "fill": "#FFFFFF80",
  "position": { "keys": [ { "t": 0, "v": [300, 360], "ease": "power2.inOut" }, { "t": 3, "v": [980, 360] } ] },
  "effects": [ { "id": "glass", "type": "distort.glass",
    "params": { "bevelSize": 32, "bevelProfile": "squircle", "refraction": 1.45, "dispersion": 0.03, "frost": 6,
                "thickness": 30, "tint": "#FFFFFF14", "saturation": 115,
                "specular": { "intensity": 0.7, "angle": -45, "size": 0.3, "rim": 40 },
                "shadow": { "opacity": 25, "softness": 16, "offset": [0, 8] } } } ] }
```

The library component `mitte/transition.glass-swipe@1` wraps this for scene transitions.

## Patterns

**Organic wobble on text.** `distort.turbulent` `amount` 12, `size` 80, `evolution` keyed 0 → 360 over the duration with `cycleEvolution` for a loop; `pinning: "all"` keeps the edges still.

**Displacement by a hidden map.** A hidden solid with `generate.fractalNoise` (or `generate.curlNoise` `output: "vectorField"`) and `distort.displacement` reading it with `fit: "stretch"`; `mapSource: "effects"` reads the map after its own effects.

**Heat haze / flag.** `distort.waveWarp` `waveType: "smoothNoise"`, `height` 6, `width` 120, `speed` 0.5.

**Screen replacement.** `distort.cornerPin` with the four points keyed per frame; the tracking sugar `pin` writes them for you from a planar track.

**Spin with blur.** `distort.transform` `rotation` keyed with `useCompShutterAngle: true` on a comp with motion blur, when the layer itself must stay static for a glow after it.

Full example: `examples/distort-family.motion.json` (the glass pill, turbulent text, a displacement map, a corner pin, a kaleidoscope).
