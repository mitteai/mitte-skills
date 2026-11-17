# Blur & sharpen

16 ids. Parameters: [91-catalogue-blur.md](91-catalogue-blur.md). All blurs work in linear light on premultiplied pixels, grow the layer's bounds by their reach, and take fractional radii that animate smoothly. `radius` is in layer pixels before the layer's scale.

| Effect | Use it for | Neutral |
|---|---|---|
| `blur.gaussian` | The default blur. True Gaussian, σ = `radius` / 3 (the visible extent is `radius`). `dims` `both`/`horizontal`/`vertical`; `repeatEdges` samples clamped edge pixels instead of transparency (no dark fringe on a full-frame plate). | `radius: 0` |
| `blur.fast` | Very large radii cheaply: a running-sum box, `iterations` 1–6 (3 ≈ Gaussian). | `radius: 0` |
| `blur.box` | A visible box kernel (one iteration by default). | `radius: 0` |
| `blur.directional` | Motion-like smear along `direction` (angle, 0 = up) over `length` px. | `length: 0` |
| `blur.radial` | `type: zoom` (streaks toward `center`, `amount` = percent of the distance, capped at 95) or `type: spin` (`amount` degrees of arc). `quality` `draft`/`best`. | `amount: 0` |
| `blur.camera` | Bokeh: an iris-shaped kernel (`iris.shape` triangle…decagon/circle, `roundness`, `rotation`, `aspect`, `diffraction`), highlights bloom into discs in linear light (`highlights.gain`/`threshold`/`saturation`); optional `depthMap` layer (`depthChannel`, `focus`, `invertDepth`). Radius capped at 128. | `radius: 0` |
| `blur.bilateral` | Edge-preserving smoothing (skin, painterly): `radius`, `threshold` percent, `colorize`. | — |
| `blur.channel` | A different Gaussian per channel: `red`, `green`, `blue`, `alpha` radii. | all 0 |
| `blur.compound` | Per-pixel radius from a `map` layer's luminance (`mapSource`, `maxRadius`, `invert`, `stretch`). | `maxRadius: 0` |
| `blur.tiltShift` | Miniature look: sharp band at `focusCenter`/`focusAngle` of `focusWidth`, blur growing over `falloff` to `radius`; `iris` as `blur.camera`. | `radius: 0` |
| `blur.smart` | Smooth flat areas, keep edges: `radius`, `threshold`, `mode` `normal`/`edgeOnly`/`edgeOverlay`. | — |
| `blur.ccCross` | A horizontal and a vertical blur (`radiusX`, `radiusY`) combined by `transferMode` `blend`/`add`/`screen`/`lighten`. | both 0 |
| `blur.ccVector` | Blur along the layer's own gradient field: `type` natural/constantLength/perpendicular/directionCenter/directionFading, `amount`, `angleOffset`, `mapSoftness`. | `amount: 0` |
| `blur.sharpen` | 3×3 Laplacian sharpen on display-encoded luma, `amount` 0–500. | `amount: 0` |
| `blur.unsharp` | Unsharp mask: `amount` percent, `radius`, `threshold` 0–255. | `amount: 0` |
| `blur.reduceInterlace` | Not implemented (P4): `effect.unavailable`. | — |

Device: `blur.gaussian`, `blur.fast`, `blur.box`, `blur.directional`, `blur.radial` and `blur.sharpen` lower to GPU passes; the rest run on the CPU ([01-effects-basics.md](01-effects-basics.md) *CPU and GPU*).

## Patterns

**Blur in, then sharp.** Key `radius` from a large value to 0 with an `expo.out` ease; at 0 the effect is skipped bit for bit. The tween shorthand `blur` does the same with an implicit `_blur` instance:

```json
{ "target": "title", "from": { "blur": 30, "opacity": 0 }, "dur": 0.8, "ease": "expo.out" }
```

**Edges.** A blur reads transparency past the layer's edge, so a full-frame photo darkens at its border; set `repeatEdges: true` (`blur.gaussian`, `blur.fast`, `blur.channel`) or blur on an adjustment layer over a plate larger than the comp.

**Depth of field without 3D.** `blur.camera` with a `depthMap` layer: a hidden gradient (`generate.gradient` on a solid) as the map, `focus` as the map value in focus, `radius` as the far blur.

```json
{ "id": "dof", "type": "blur.camera",
  "params": { "radius": 24, "depthMap": "depth", "depthMapSource": "effects", "depthChannel": "luminance",
              "focus": 35, "iris": { "shape": "hexagon", "roundness": 20 }, "highlights": { "gain": 1.5, "threshold": 0.9 } } }
```

**Zoom streaks.** `blur.radial` `type: zoom` from a logo's centre, `amount` keyed 0 → 60 → 0 on a hit. The centre defaults to the running rect's centre; write a number to pin it.

**Lens blur on a 3D camera** is the camera's own `depthOfField` (spec 8), not this family.

Full example: `examples/blur-family.motion.json` (gaussian reveal, tilt-shift on a plate, a zoom hit).
