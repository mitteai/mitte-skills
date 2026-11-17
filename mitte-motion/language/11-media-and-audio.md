# 11. Media and audio: interpretation, image and video layers, sequences, Lottie and SVG sources, audio layers, the mixdown, ducking, analysis, captions input

Scope: spec 10 in full. The layer field tables are in [05-layers.md](05-layers.md) §10; this page gives the semantics. Generated tables: `Asset`, `AssetType`, `ColorSpace`, `AlphaMode`, `FieldOrder`, `Orient`, `Sequence`, `Fit`, `FitMode`, `FrameBlend`, `HoldMode`, `Volume`, `Fade`, `FadeObject`, `FadeCurve`, `Channels`, `Duck`, `MarkerFrom`, `Detect`, `BeatFallback`, `FromAudio` in `92-schema-types-*.md`.

The engine never fetches: the service downloads every `https:` asset before a render. Still images, SVG and fonts decode in the engine; video and audio decode in a pinned `ffmpeg` subprocess.

## 1. Media interpretation (asset fields)

After Effects' "Interpret Footage": these live on the asset and apply to every layer using it ([01](01-document.md) §6 lists every asset field).

| Field | Applies to | Default | Notes |
|---|---|---|---|
| `colorSpace` | image, video, sequence | from file tags, else [14](14-color-and-output.md) §3 rules | overrides the file's own tags |
| `range` | video | from tags; `limited` for Y'CbCr, `full` for RGB codecs and MJPEG | |
| `alpha` | image, video, sequence | from file | `straight`, `premultiplied`, `ignore`, `stacked-bottom`, `stacked-right` |
| `fps` | video, sequence, animated image | the file's timestamps | conform to a rate (source frame *n* at `n / fps`; audio of a conformed video is muted) |
| `orient` | image, video | `auto` | EXIF / display-matrix rotation, or `ignore` |
| `pixelAspect` | image, video | from file (SAR), else 1 | non-square sources are resampled to square pixels at decode |
| `field` | video | from file, else `progressive` | `upper` / `lower`: deinterlaced at decode (`bwdif`); interlaced output is not supported |
| `loop` | video, sequence | `1` | After Effects loop count: the source becomes *n* times longer |
| `sequence` | sequence | — | §4 |
| `audioTrack`, `videoTrack` | video, audio | `0` | stream selection |

A declared `type` that does not match the file is `asset.type_mismatch`; `fps` overrides silently.

## 2. Image layers

`asset`, `fit`, `box`, `crop`, `frame`, `focus` ([05](05-layers.md) §10). `fit`, `box`, `crop` and `focus` are applied at render time (the renderer places the oriented, cropped source into its box and cuts to it); normalization only fills `box` with the comp size when `fit` is given without `box`. The transform's `scale` multiplies on top.

| `fit` | Result | CSS |
|---|---|---|
| `none` | natural size (after `crop` and `pixelAspect`), placed in `box` by `focus` | — |
| `contain` | scaled uniformly inside `box`, transparent bars | `object-fit: contain` |
| `cover` | scaled uniformly to cover `box`, clipped to it; `focus` picks what stays in view | `object-fit: cover` |
| `fill` | stretched to exactly `box` | `object-fit: fill` |

Formats: PNG (1–16 bit; ICC, `sRGB`, `gAMA`/`cHRM`, `cICP` HDR), JPEG (8-bit; ICC incl. CMYK), WebP and GIF (still and animated), BMP/TGA/QOI, SVG (vector), AVIF (via ffmpeg), TIFF (8/16/32f), OpenEXR (half/float, premultiplied, scene-linear), PSD/PSB (flattened composite only), HEIC/HEIF. Decoded pixels are converted once to the working space in premultiplied f32 and cached; premultiplied sources are clamped so colour ≤ alpha, except EXR. An SVG on an image layer is **vector footage**, re-rasterized at the drawn scale (cached per 1/64 octave); its SMIL/CSS animation is ignored (convert to shapes to animate parts, [07](07-shapes.md) §8.2). Raster sources below 50 % scale sample a mip pyramid (trilinear) so zoom-outs do not shimmer; `sampling` (`nearest`, `bilinear`, `bicubic` default, `lanczos`) picks the filter.

## 3. Video layers

`asset`, timing (`in`, `out`, `dur`, `offset`, `stretch`, `timeRemap`), `sourceIn`, `sourceOut`, `speed`, `reverse`, `loop`, `hold`, `freeze`, `frameBlend`, `fit`/`box`/`crop`/`focus`, `audio`, `volume`, `pan`, `fadeIn`, `fadeOut`, `mute`, `audioTrack` ([05](05-layers.md) §10). **Layer time is source time**: layer time 3.2 s shows the source at 3.2 s (before `loop`). Without `out`, the layer ends where its source ends (or the comp's end); an `out` past a non-looping source holds the last frame (`lint.media_past_end`).

### 3.1 Containers and codecs

Anything the pinned ffmpeg decodes; promised and tested: MP4/MOV/M4V (H.264 8/10-bit, HEVC 8/10-bit incl. alpha, AV1, ProRes all profiles incl. 4444/XQ alpha, MJPEG, PNG/QTRLE alpha, DNxHR; AAC, ALAC, PCM, MP3, Opus), WebM/MKV (VP8, VP9 incl. alpha, AV1, H.264, HEVC; Opus, Vorbis, AAC, FLAC, PCM), AVI/MXF/MPEG-TS as decoded, animated GIF/WebP/AVIF/APNG. Variable-frame-rate sources are placed by their presentation timestamps.

### 3.2 Which frame shows

Given source time *s* (after `stretch`, `timeRemap`, `loop`): before the first frame, frame 0; otherwise the frame with the largest `pts ≤ s + one tick`; past the last frame's end, the last frame. For constant-rate sources this is exactly `floor(s · fps_src)` in rationals (no drift). With motion blur every shutter sample picks its own frame (real frame steps inside the blur; use `frameBlend` to smooth).

### 3.3 Frame blending

| `frameBlend` | Between frames *k* and *k+1* |
|---|---|
| `off` | frame *k* |
| `mix` | a linear-light crossfade weighted by the position between the two pts (After Effects "Frame Mix"); cheap, ghosts on fast motion |
| `flow` | motion-compensated interpolation (After Effects "Pixel Motion"): dense optical flow between the two frames (both directions, pyramid, Lucas–Kanade, analysed at ≤ 960 px on the long side), forward-splatted to the target time with occlusion-aware weights; degrades to `mix` where the flow fails; the flow pair is cached per (asset, frame); expensive (hundreds of ms per new frame pair) |

Blending only happens when *s* falls between frames (slowed, remapped, conformed, or a source slower than the comp); at 100 % with matching rates it costs nothing. Image sequences, a comp layer's two surrounding nested frames, and the `time.frameBlend` effect blend the same way. The browser preview shows frame *k* for both modes.

### 3.4 Looping, remapping, alpha

`loop: true` wraps source time (`s mod D`, *D* the source duration after the asset-level `loop`); negative `stretch` loops backwards; `timeRemap` with `loop` is `media.loop_and_remap`. `timeRemap` values are clamped to `[0, D]`; faster-than-source remaps skip frames (no blending unless `frameBlend`); the audio of a remapped video is varispeed-resampled and muted where the remap is held; `freeze: <time>` is the one-key hold sugar. Alpha comes from the codec (ProRes 4444, VP9 alpha, HEVC alpha, PNG/QTRLE, animated WebP/AVIF/GIF) or a stacked layout; `alpha: "ignore"` makes a source opaque. Green screen is a keying effect or, better, a segmentation matte as a separate video asset used as a track matte.

## 4. Image sequences

```jsonc
"explosion": { "src": "https://media.mitte.ai/u/abc/explosion.zip", "type": "video", "sequence": { "pattern": "boom_%04d.png", "start": 1, "fps": 24 } }
```

`pattern` (printf-style, one integer field) is matched against the zip's file names; `start` defaults to the lowest number (gaps hold the previous frame, `media.sequence_gap`); `fps` defaults to 30. All frames one still format and size; EXR and 16-bit sequences keep their precision. Behaves exactly like video (timing, looping, blending). ≤ 20,000 frames.

## 5. Lottie and SVG files as sources

A Lottie file (`.json`, `.lottie`) is **imported, not played**: a comp layer with `lottie: "<asset>"` instead of `comp` makes the normalizer import it into a generated comp `<layer id>.lottie` (sized and timed from the file's `w`, `h`, `fr`, `ip`, `op`; precomps become `<layer id>.lottie.<comp id>`), rendered by the same renderer as everything else, so it gets motion blur, linear blending, effects, 3D, and is editable by id. The layer then behaves like any comp layer (`timeRemap`, `loopMode`, `collapse`, blur). `lottieAnimation` picks an animation in a multi-animation dotLottie (default the manifest's first), `lottieTheme` applies one of its themes; the dotLottie 2.0 layout and the legacy folders are both read. Differences from `motion.convert` import: images and audio inside the file are dropped (one `convert.lottie_unsupported` warning), expressions that do not compile are dropped with `convert.lottie_expression` (keys kept), and a not-yet-fetched asset shows an empty comp of the probed size (`asset.unmaterialized`). Limits: 20 MB, 5,000 layers, precomp depth 16 (`limit.lottie`). SVG as footage: §2; SVG as shapes: [07](07-shapes.md) §8.2.

## 6. Audio layers

`asset` (`audio`, or `video` for its sound), timing as video (audio has no frames: source time maps to samples exactly; audible only inside `[in, out)`), `volume` (dB, keys interpolate in dB; `"-inf"` or ≤ −96 mutes), `pan` (−100–100: constant-power for mono sources, `L = cos θ`, `R = sin θ`; stereo sources are balanced, the far side attenuated and centre bit-exact), `fadeIn`/`fadeOut` (a time, or `{ "dur", "curve": "sine" | "linear" | "exp" }`: equal-power quarter-sine, linear amplitude, or a −60 dB → 0 dB ramp in dB; compile to volume keys from `in` / to `out`), `mute`, `solo` (previews; `media.solo_in_render` unless `output.allowSolo`), `duck` (§7.3), `channels` (`stereo`, `mono`, `left`, `right`: downmix or select before panning). Playback speed (`100/|stretch|` × the remap slope) must stay within 0.01–16× (`media.audio_track_invalid`). Audio layers draw nothing, may be parents with no effect, and are not readable by expressions (use the `audio` driver or markers).

Audio from a **video** layer follows the video layer's timing, `audio` switch and `volume`/`pan`/`fade*`/`mute`. Audio inside a **comp** layer is mixed into the parent as a submix following the comp layer's time mapping (`offset`, `stretch`, `timeRemap`, `loopMode`); comp layers have no `volume` or `pan` of their own (give the nested audio layers the gain).

## 7. The mixdown

Computed once per render for the rendered range, independent of frames, handed to the encoder as one stream.

### 7.1 Signal path

1. Decode every audible source to 32-bit float at **48 kHz** (soxr very-high quality when the rate differs).
2. Time-map each source by its layer's timing (`stretch` varispeed: pitch follows speed; `loop`; `timeRemap`), sample-exact.
3. Channel: apply `channels`, downmix beyond stereo with ITU-R BS.775.
4. Gain per sample: `volume(t)` (dB → linear per 1 ms block, interpolated), fades, pan.
5. Sum all layers and nested submixes in f32; no implicit normalization (two full-scale sources clip, as in any mixer).
6. Master (`output.audio`): `loudness` (optional; EBU R128 integrated loudness to the target, default −14 LUFS when enabled, one static gain capped at +12 dB, none when the gating leaves nothing to measure) and `limiter` (default on: true-peak look-ahead at −1.0 dBTP, 4× oversampled, 5 ms look-ahead, 50 ms release; passes a mix below −1 dBTP bit-identically).
7. Dither and quantize (TPDF) only for integer PCM; AAC and Opus take f32.

### 7.2 Silence and length

The stream covers exactly the rendered range. A document with no audible layer produces a video **without an audio track** unless `output.audio.always: true` (silence, for platforms that reject audio-less uploads).

### 7.3 Ducking

```jsonc
"duck": { "under": ["vo", "vo2"], "by": 9, "threshold": -36, "attack": 0.08, "release": 0.45, "hold": 0.15 }
```

| Field | Default | Meaning |
|---|---|---|
| `under` | required | layer ids whose audio triggers the duck |
| `by` | 9 | reduction in dB while triggered |
| `threshold` | −36 | dBFS above which a trigger counts as active (RMS of a 50 ms window centred on each 1 ms block: 25 ms of look-ahead) |
| `attack`, `release` | 0.08, 0.45 s | ramps into and out of the ducked level, linear in dB |
| `hold` | 0.15 s | minimum time ducked after the trigger falls below threshold |

Resolved in normalization and **baked into `volume` keyframes** on the ducked layer (within 0.5 dB of the exact envelope), so the canonical document shows the dips. A muted or non-solo trigger does not trigger. A rule naming no audible layer or with negative values is `media.duck_invalid`.

## 8. Audio analysis

Deterministic (f64, pinned FFT, versioned, cached by file hash + kind + parameters). STFT: Hann 2048 samples (42.7 ms), hop 240 (5 ms, 200 frames/s), 1025 bins; envelopes are produced at 5 ms and interpolated.

- **Level envelope** (the `audio` driver): band energy per frame (bins weighted by overlap with `[lo, hi]`), normalized so the band's loudest 50 ms = 1, floored by the driver's `floor`, smoothed with attack `smooth/4` and release `smooth`. `mode: "onset"`: a pulse per onset at its strength, decaying with the driver's `decay`.
- **Onsets**: SuperFlux spectral flux (log-compressed 24-band filterbank 30 Hz–17 kHz, rectified difference against a ±1-band max of the previous frame, frame 0 measured against silence), adaptive threshold (local maximum within ±30 ms, above the 100 ms moving mean + 0.07, ≥ 30 ms apart); times are event times (+10.7 ms).
- **Tempo and beats** (Ellis dynamic programming): autocorrelation of the onset envelope over 60–200 BPM with a log-Gaussian prior at 120 BPM (a `tempo` hint replaces it); DP beat placement with tightness 100; beats before the first strong onset and after the last are dropped; `fallback: "grid"` emits a metronome grid when nothing is found. **Downbeats**: among `meter` phases, the one maximizing low-frequency (30–150 Hz) flux at its beats.

| Use | How | Result |
|---|---|---|
| markers | `"markers": [{ "from": { "audio", "detect": "beats" \| "onsets" \| "downbeats", "prefix", "tempo", "meter", "min", "fallback" } }]` | plain markers in the canonical comp, clipped to its duration ([01](01-document.md) §7.3) |
| driver | `"scale": { "value": [100, 100], "audio": { "asset", "band", "gain" } }` | evaluated at render time ([04](04-presets-and-drivers.md) §4) |
| baked keys | `"keys": { "fromAudio": { "asset", "band", "gain", "rate": 30 } }` | authored: keys at `rate`/s, simplified within 1 % |
| ducking | `duck` | volume keys |
| lint | automatic | integrated loudness, true peak, clipped samples in `motion.check` metrics (`lint.loud_audio`) |

Beat tracking is good on produced, percussive music and unreliable on speech, ambient and classical audio (`lint.beats_unstable`).

## 9. Captions input

Word timings come from a transcription tool; the engine does not transcribe. The one word-timing shape, accepted as a `data` asset (`$data.@transcript.words`), inline under `data`, on a text layer's `words` ([08](08-text.md) §8), and as the `caption.*` components' `words` param:

```jsonc
{ "language": "en", "words": [
  { "text": "Ship", "start": 0.42, "end": 0.71, "speaker": "A" },
  { "text": "faster", "start": 0.71, "end": 1.18, "speaker": "A", "emphasis": true },
  { "text": "mitte.", "start": 1.44, "end": 1.95, "confidence": 0.93 } ] }
```

`text` (one word with its punctuation), `start`, `end` (seconds; sorted by `start`, overlaps clipped) are required; `speaker`, `emphasis`, `confidence` optional; `language` selects line breaking and shaping. SRT and WebVTT data assets are converted with each cue's words spread evenly (`media.captions_cue_level`). ≤ 50,000 words. Timings are in the media's time: give the caption layer or component an `in` equal to the voice layer's.

## 10. Limits and costs

Images ≤ 16,384 px per side and 64 MP (`media.image_too_large`); video ≤ 7680 × 4320 (`media.video_too_large`); 32 distinct video sources and 64 audio sources per render; sequences ≤ 20,000 frames; archives ≤ 2 GB unpacked, ratio ≤ 100, ≤ 1,000 entries; SVG ≤ 50,000 nodes, `use` depth 16; Lottie 20 MB / 5,000 layers / depth 16; caption words ≤ 50,000. Every decoder checks declared sizes before allocating. Decoding is often the largest render cost: one decoder per (source, direction), frames decoded sequentially and shared between layers; reverse playback of long-GOP video costs about 2× (`lint.media_reverse_long_gop` suggests an intra-only proxy); `flow` blending costs hundreds of ms per new frame pair, reused by every comp frame between the two source frames.

## 11. Examples

`examples/05-media-layers.json` ([05](05-layers.md)) covers the layer fields; `examples/11-media-audio.json` adds every asset interpretation field, a conformed sequence, a video-as-still, a Lottie comp layer with `loopMode`, beat markers from audio with a `grid` fallback, `audio` drivers in `level` and `onset` mode, a comp-layer submix with its own audio layer, and a caption component fed by inline word timings. Media assets are `https:` URLs, so `check` reports `asset.unmaterialized` infos; a **`data` asset** that has not been fetched is reported the same way, and its `$data.@<id>` references read an empty table until it is (the example keeps its transcript inline so the captions show in a local check). `keys.fromAudio` is not in the example: with an unfetched audio asset the property holds its default and `check` reports the info `asset.unmaterialized` until the asset is fetched ([04](04-presets-and-drivers.md) §5). Checks with 0 errors.

