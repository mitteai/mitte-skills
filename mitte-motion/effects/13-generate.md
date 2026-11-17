# Generate (and the noise and audio-driven generators)

27 ids. Parameters: [91-catalogue-generate-1.md](91-catalogue-generate-1.md), [91-catalogue-generate-2.md](91-catalogue-generate-2.md). Generators draw new pixels over the layer's **raster rect** (content rect plus the 1 px halo). The field generators (`gradient`, `gradient4`, `fractalNoise`, `turbulentNoise`, `grid`, `checkerboard`, `circle`, `ellipse`, `beam`, `cells`, `meshGradient`, `curlNoise`, `scribble`) have `composite`: `replace` (the generator's pixels only), `over`, `under`, `inside` (only where the layer is opaque); the engine's own default is `replace` and the host layer fills the per-kind default when `composite` is absent (`replace` on solids, `over` on shape, text and footage layers). The path, contour, audio and paint generators (`stroke`, `vegas`, `radioWaves`, `writeOn`, `fill`, `paintBucket`, `eyedropperFill`, `ccThreads`, `ccGlueGun`, `fractal`, `lensFlareSimple`, `audioSpectrum`, `audioWaveform`, `advancedLightning`) always draw over the layer and take no `composite` (`effect.unknown_param`); their own `opacity`, `blend` or `compositeOnOriginal` say how. Most also take `opacity` and a `mode` (blend mode of the generated pixels over the layer); `opacity: 0` with a non-replace composite is the neutral value.

| Effect | Use it for |
|---|---|
| `generate.fill` | Recolour the layer's alpha with `color` at `opacity`, optionally only inside `masks` (list of mask ids, default all). The standard way to colour a logo or a matte. |
| `generate.gradient` | Gradient Ramp: `type` linear/radial/angular/diamond/reflected, `start`/`end` points, `gradient` (stops + `interpolation`), `dither` (on; ±½ LSB blue noise in linear light), `scatter`. |
| `generate.gradient4` | Four-colour "mesh" background: `points` list of 4 `{ position, color }`, `blend` ≥ 1 (100 = inverse square), `jitter`, `opacity`, `mode`. |
| `generate.meshGradient` | Freeform gradient: `points` (3–16 `{ position, color, radius }`), `smoothness`, `warp.amount`/`scale`/`speed` (the animated aurora blob). |
| `generate.fractalNoise` | The most used generator: `fractal` (16 kinds: basic, turbulentBasic, turbulentSmooth, turbulentSharp, dynamic, dynamicProgressive, dynamicTwist, max, rocky, smeary, swirly, threads, turbulentSmear, cloudy, strands, smoky), `type` block/linear/softLinear/spline, `invert`, `contrast`, `brightness`, `overflow` clip/softClamp/wrapBack/allowHdr, transform (`rotation`, `uniformScaling`, `scale`, `scaleWidth`/`scaleHeight`, `offset`, `perspectiveOffset`), `complexity` 1–20, `subInfluence`/`subScale`/`subRotation`/`subOffset`/`centerSubscale`, `evolution` °, `cycleEvolution` + `cycle`, `randomSeed`, `opacity`, `mode`. The lattice cell is 2 · `scale` px. |
| `generate.turbulentNoise` | The same engine with `fractalType` default `turbulentBasic`, `overflow` default `clip`, plus `evolutionOptions.turbulenceFactor`. |
| `generate.curlNoise` | Divergence-free noise: `output` vectorField (a red/green displacement map) / flowLines (silky streaks) / magnitude; `scale`, `complexity`, `evolution`, `speed`, `lineLength`, `color` gradient. |
| `generate.cells` | Worley cells: `pattern` (14 kinds incl. the `…Hq` ones), `size`, `disperse`, `evolution` + `cycleEvolution`/`cycle`, `tiling.enable`/`cellsHorizontal`/`cellsVertical`, `contrast`, `overflow`, `invert`, `randomSeed`. |
| `generate.checkerboard` | `anchor`, `size [w, h]`, `feather`, `color`, `opacity`, `mode`. |
| `generate.grid` | `anchor`, `size` point, `border` px, `feather`, `invert`, `color`, `opacity`, `mode`. |
| `generate.circle` | A disc or ring: `center`, `radius`, `edge` none/edgeRadius/thickness/thicknessRadius/thicknessFeatherRadius, `edgeRadius`, `thickness`, `feather.outer`/`inner`, `invert`, `color`. Prefer shape layers. |
| `generate.ellipse` | A ring on an ellipse: `center`, `width`, `height`, `thickness`, `softness`, `inside`/`outside` colours. |
| `generate.beam` | A laser segment from `start` to `end`: `length` percent, `time` percent along, `startThickness`/`endThickness`, `softness`, `inside`/`outside`, `3dPerspective`. |
| `generate.stroke` | Strokes the layer's masks: `path` mask id or `all`, `color`, `size`, `hardness`, `opacity`, `start`/`end` (draw-on), `spacing`, `paintStyle` onOriginal/onTransparent/revealOriginal. |
| `generate.writeOn` | A brush following the keyed `brushPosition` (`color`, `size`, `hardness`, `opacity`, `length` s of trail, `spacing` s, `paintTime`, `paintStyle`); at most 512 dabs per frame. |
| `generate.scribble` | Hand-drawn scribble fill of `path` masks: `fillType`, `color`, `opacity`, `angle`, `strokeWidth`, `curviness`, `spacing`, `wiggleType` static/jumpy/smooth, `wigglesPerSecond`, `start`/`end`. Time-dependent. |
| `generate.vegas` | Chasing lights along `path` (mask id or `imageContours`): `segments`, `length`, `segmentDistribution`, `rotation`, `randomPhase`, `blend`, `width`, `hardness`, `startOpacity`/`midOpacity`/`endOpacity`, `color`. |
| `generate.radioWaves` | Concentric ripples from `producer`: `frequency`, `expansion`, `orientation`, `direction`, `velocity`, `spin`, `lifespan`, `reflection`, `shape` polygon/imageContours/mask, `sides`, `curvature`, `starDepth`, `color`, `opacity`, `fadeIn`/`fadeOut`, `startWidth`/`endWidth`. Time-dependent. |
| `generate.lensFlareSimple` | After Effects' built-in flare (`center`, `brightness`, `lens` 50-300zoom/35prime/105prime); `light.flare` is the better one. |
| `generate.paintBucket` | Flood fill from `fillPoint` (`selector`, `tolerance` 0–255, `strokeType` antialias/feather/spread/choke, `featherSoftness`, `spreadRadius`, `color`, `opacity`). |
| `generate.advancedLightning` | Seeded lightning: `lightningType` (8 kinds), `origin`, `direction`, `conductivityState` (animate it), `core.*`, `glow.*`, `turbulence`, `forking`, `decay`, `decayMainCore`, `alphaObstacle`, `compositeOnOriginal`, `expert.*`. |
| `generate.ccGlueGun` | Glue blobs along the animated `brushPosition` over `timeSpan` s (`strokeWidth`, `density`, `reflection`, `strength`, `style`). Reads the parameter's history. |
| `generate.ccThreads` | Woven-thread texture: `width`, `height`, `overlaps`, `direction`, `center`, `coverage`, `shadowing`, `texture`. |
| `generate.eyedropperFill` | Fill with the colour sampled at `samplePoint` (`sampleRadius`, `averagePixelColors`, `maintainOriginalAlpha`, `blendWithOriginal`). |
| `generate.fractal` | Mandelbrot/Julia: `set`, `equation` z2/z3/z4, `mandelbrot.*`/`julia.*` (x, y, magnification, escapeLimit), `postInversionOffset`, `color.*`, `oversample.*`. |
| `generate.audioSpectrum` | Spectrum bars/lines from an `audio` layer's analysis (`path` mask or `start`/`end`, `startFrequency`/`endFrequency`, `bands`, `maxHeight`, `duration`, `offset`, `thickness`, `softness`, `insideColor`/`outsideColor`, `blend`, `hueInterpolation`, `dynamicHue`, `side`, `durationAveraging`, `display` digital/analogLines/analogDots/bars, `roundCaps`, `mirror`, `smoothing`). |
| `generate.audioWaveform` | The waveform of an `audio` layer (`samples`, `displayedSamples`, `maxHeight`, `duration`, `thickness`, `softness`, colours, `display`, `mirror`). |

Device: `generate.fill`, `gradient`, `gradient4`, `grid`, `fractalNoise`, `turbulentNoise` lower to the device.

## Noise

`generate.fractalNoise` is the base of most organic looks. Rules: `evolution` is degrees (one revolution per `cycle` when `cycleEvolution` is on, for a seamless loop), `randomSeed` picks the lattice, `scale` 100 = 200 px cells, `complexity` octaves, `subInfluence` the octave gain. For a displacement source render it on a hidden solid and point `distort.displacement` (`horizontal: "red"`, `vertical: "green"`) or `distort.turbulent` at it. For a vector field use `generate.curlNoise` `output: "vectorField"`. The grain look is `stylize.grain`, per-pixel noise `stylize.noise` ([15-stylize.md](15-stylize.md)).

```json
{ "id": "smoke", "type": "generate.fractalNoise",
  "params": { "fractal": "turbulentSmooth", "scale": 180, "complexity": 5, "contrast": 130, "brightness": -10,
              "evolution": { "keys": [ { "t": 0, "v": 0 }, { "t": 6, "v": 360 } ] }, "cycleEvolution": true, "cycle": 1,
              "composite": "replace" } }
```

## Audio-driven

`generate.audioSpectrum` and `generate.audioWaveform` read the `audio` layer's analysis (an `audio` or `video` layer of the comp; the FFT is computed once per render, deterministic). The simpler alternative for bars is a `repeat` of shapes with one `audio` driver per bar on its own `band` (spec 2 §2.9).

```json
{ "id": "spectrum", "type": "generate.audioSpectrum",
  "params": { "audio": "music", "start": ["5%", "80%"], "end": ["95%", "80%"], "bands": 48, "maxHeight": 260,
              "startFrequency": 40, "endFrequency": 8000, "display": "bars", "thickness": 10, "roundCaps": true,
              "insideColor": "#7CF2FF", "outsideColor": "#7C5CFF" } }
```

Full example: `examples/generate-family.motion.json`.
