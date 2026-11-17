# 14. Colour and output: writing colours, working colour, input colour, output transforms, the whole `output` block

Scope: spec 13 in full, checked against `rexx-doc/src/output.rs`, `rexx-color` and `rexx-encode` (engine 0.1.48: `aces2` and HDR are built). Generated tables: `ColorValue`, `ColorObject`, `ColorSettings`, `WorkingSpace`, `BlendingSpace`, `InterpolationSpace`, `Output`, `OutputFormat`, `Codec`, `OutputQuality`, `OutputEncoder`, `PixelFormat`, `AlphaOutput`, `ToneMap`, `GamutMap`, `TransferTag`, `SignalRange`, `Hdr`, `AudioOutput`, `AudioCodec`, `Poster`, `GifOutput`, `GifPalette`, `GifDither` in `92-schema-types-*.md`.

The engine computes in scene-linear float and converts exactly once on the way in and once on the way out.

## 1. Writing colours

| Form | Example | Space |
|---|---|---|
| hex | `"#F36"`, `"#F368"`, `"#FF3366"`, `"#FF336680"` (the last pair is alpha; case-insensitive) | sRGB (encoded) |
| `rgb()` / `rgba()` | `"rgb(255 51 102)"`, `"rgb(255, 51, 102, 0.5)"`, `"rgb(100% 20% 40% / 50%)"` | sRGB |
| `hsl()` / `hsla()` | `"hsl(340 100% 60%)"` (hue in degrees, `deg`, `turn`, `rad`) | sRGB |
| `oklch()` | `"oklch(0.68 0.21 12)"`, `"oklch(68% 0.21 12 / 0.8)"` | OKLCh (the best form for palettes: vary H at fixed L and C) |
| `oklab()` | `"oklab(0.68 0.19 0.08)"` | OKLab |
| `color()` | `"color(display-p3 1 0.2 0.4)"`, `"color(srgb-linear 4 2 1)"`, `"color(rec2020 …)"`, `"color(xyz-d65 …)"`, `"color(acescg 0.9 0.1 0.2)"` | as named; linear spaces take values above 1 (HDR) |
| named | `"white"`, `"rebeccapurple"`, `"transparent"` (the 148 CSS names) | sRGB |
| object | `{ "r": 1.0, "g": 0.2, "b": 0.4, "a": 1 }` | the comp's working space, **linear**, not premultiplied; components may exceed 1 (glow cores, HDR); the canonical form (rounded to 1e-7) |
| reference | `"$theme.color.accent"`, `"$theme.color.accent.a40"` | authored |

Expressions see colours as **sRGB-encoded** `[r, g, b, a]` arrays (After Effects' convention; values above 1 pass through the extended curve). Out-of-gamut colours (a P3 red in a Rec.709 working space) are kept as negative or > 1 components through the computation and gamut-mapped only at output.

## 2. Working colour (per comp)

```jsonc
"color": { "working": "linear-srgb", "blending": "linear", "interpolation": "oklab" }
```

| Field | Values | Default | Notes |
|---|---|---|---|
| `working` | `linear-srgb` \| `acescg` | `linear-srgb` | the primaries the engine computes in; both scene-linear. `acescg` has AP1 primaries (holds P3 and most of Rec.2020 with positive components) |
| `blending` | `linear` \| `display` | `linear` | `linear`: opacity, blend modes, blurs, glows, scaling and motion blur average light (a 50 % white over black is brighter than mid-grey; glows and streaks keep energy). `display`: all compositing on sRGB-encoded values, reproducing After Effects with "Linearize Working Space" off, for parity with an existing look |
| `interpolation` | `oklab` \| `srgb` | `oklab` | the space colour keys and gradient stops mix in: perceptually even (blue → yellow through a clean light tone) or After Effects/CSS (muddy midpoints). Alpha always linear |

Always 32-bit float per channel, premultiplied; no 8/16-bit project modes. Nested comps inherit unless they set their own; pixels crossing a boundary are converted. 3D lighting is always computed on linear values.

## 3. Input colour

Every source is converted once at decode to the working space and cached.

| Source | Colour space from | Conversion |
|---|---|---|
| document colours | the written form | exact |
| images with an ICC profile (v2/v4, RGB, grey, CMYK) | the profile | through the CMS (moxcms), relative colorimetric with black-point compensation |
| PNG `cICP` (incl. PQ/HLG HDR PNG), `sRGB`, `gAMA`+`cHRM` | the chunks | as video / sRGB / stated gamma and primaries |
| images with no colour information | assumed sRGB | |
| OpenEXR | `chromaticities`, else linear Rec.709 | primaries matrix only |
| SVG, Lottie | sRGB | as document colours |
| video | container and bitstream tags (primaries, transfer, matrix, range) | Y'CbCr → R'G'B' → decode the transfer → primaries matrix |
| untagged video | `yuvj*` formats are full range; height < 720: BT.601 with the size-implied primaries, else BT.709; limited range for Y'CbCr, full for RGB codecs and MJPEG; BT.709 decoded with the sRGB EOTF (so a screen recording round-trips exactly with the default output) | |
| asset `colorSpace` | the override | |

Supported transfers: BT.709/601/2020 SDR, sRGB, linear, gamma 2.2/2.8, PQ, HLG, camera logs (S-Log3, LogC3/4, V-Log, C-Log3, Apple Log). HDR sources become scene-linear with **1.0 = 203 cd/m²** (BT.2408): a PQ highlight at 1,000 cd/m² is ≈ 4.9; SDR outputs tone-map them, HDR outputs preserve them up to the peak.

## 4. Output transforms

### 4.1 SDR encoding

Every SDR output is Rec.709/sRGB primaries, D65 (an `acescg` root is converted first). PNG/JPEG/WebP/GIF/AVIF stills and PNG sequences: the sRGB transfer (PNG with `sRGB` + `cICP` 1/13/0/1; JPEG/WebP an sRGB ICC). TIFF sequences: sRGB with an embedded ICC, **unassociated** (straight) alpha. EXR sequences: scene-linear, Rec.709 chromaticities, premultiplied, no tone mapping. Video: pixels encoded with the sRGB curve and tagged `bt709`/`bt709`/`bt709`, range `tv` (`pc` for full range); `transferTag: "srgb"` writes `iec61966-2-1` instead (Apple's players display BT.709-tagged video slightly lighter). 8-bit outputs use a two-segment lookup table that reproduces the 8-bit codes exactly; deeper outputs use the exact function.

### 4.2 Tone mapping (`output.toneMap`)

| Value | Behaviour | Use |
|---|---|---|
| `clip` (default) | each channel clamped to [0, 1] after gamut mapping | After Effects parity; saturated overexposure skews hue |
| `soft` | a luminance-preserving shoulder: untouched below a knee of 0.8; above it extended Reinhard on max(R, G, B) with white point 4.0, chroma reduced toward neutral by `(m − 0.8)/(4 − 0.8)` so highlights go to white | glow-heavy and HDR-sourced work (recommended with bloom) |
| `aces2` | the ACES 2.0 tonescale for an SDR 100 cd/m² display (After Effects 26.5's OCIO curve), applied to luminance with a luminance-preserving chroma fit (neutrals exact, saturated highlights differ from the JMh reference); 18 % grey shows at 10 %, white at 46 %, so never a default | cinematic grading, footage-heavy work |

### 4.3 Gamut mapping, dithering, chroma

`gamutMap`: `clip` (default; clamp per channel) or `compress` (CSS Color 4: reduce OKLCh chroma at constant lightness and hue until in gamut). `dither` (default `true`): a 64 × 64 blue-noise texture at ±1 LSB (TPDF) at every quantization to 8 or 10 bits, applied after the transfer and matrix, offset per frame by a hash (deterministic), skipped for values that already sit exactly on a code (flat hex colours stay flat), alpha only for 8-bit outputs with partial transparency. Video Y'CbCr is produced by the engine: BT.709 matrix (BT.2020 NCL for HDR), limited range by default (`signalRange: "full"` otherwise), 4:4:4 / 4:2:2 (cosited [1, 2, 1]/4) / 4:2:0 (left-sited, vertical 2-tap average). Thin saturated text at 4:2:0 loses edge sharpness (`lint.chroma_text`; use `pixelFormat: "yuv444p"` where the destination accepts it). Subsampled outputs need even sides: a computed odd size rounds **up** to even; an explicit odd `size` with a subsampled format is `output.size_odd`.

### 4.4 HDR outputs

`"hdr": "hlg"` or `"pq"`: values above 1 are kept, the root comp is converted to Rec.2020 primaries, encoded with HLG or PQ (1.0 = 203 cd/m²) into 10-bit HEVC Main10 or AV1 with BT.2100 tags; PQ adds mastering-display metadata and MaxCLL/MaxFALL **measured from the render** (so a PQ encode spools its frames and runs ffmpeg once at the end). `toneMap` then works on cd/m²: `clip` is `203·v` clamped to the peak; `soft` has its knee at 0.8 × peak; `aces2` the ACES 2.0 tonescale for the peak. Peak: `hdrPeak` 100–10,000 cd/m² (default 1,000) for PQ (clip level, tone-map peak, mastering maximum); HLG is fixed to the BT.2100 1,000 cd/m² display (`hdrPeak` with `hlg` is `output.value`). Codecs: `hevc` (the default in `mp4`/`mov`, tag `hvc1`) or `av1` (the default in `webm`); `h264`, `vp9`, `prores`, profile `main`, an 8-bit `pixelFormat`, `alpha`, image and sequence formats are `output.hdr_unsupported` (`output.pixel_format` for the 8-bit format). HLG is the recommended HDR target for social platforms (Instagram plays HLG as HDR). Posters and `motion.frames` are SDR. Not built: HDR stills, dynamic metadata, inverse tone mapping from SDR.

## 5. The `output` block

At the document's top level (defaults) and in a `motion.render` call (field-by-field overrides).

```jsonc
"output": {
  "format": "mp4", "codec": "h264", "profile": null, "quality": "standard",
  "crf": null, "bitrate": null, "preset": null, "encoder": "cpu",
  "fps": null, "scale": null, "size": null, "range": null,
  "alpha": false, "pixelFormat": null,
  "toneMap": "clip", "gamutMap": "clip", "dither": true, "transferTag": "bt709", "signalRange": "limited",
  "hdr": null, "hdrPeak": 1000,
  "audio": { "codec": "aac", "bitrate": 192, "limiter": true, "loudness": null, "always": false },
  "allowSolo": false, "locale": "en-US", "poster": null, "faststart": true,
  "gif": { "fps": null, "palette": "global", "dither": "blue-noise", "colors": 256, "transparency": null }, "loop": 0
}
```

| Field | Values | Default | Notes |
|---|---|---|---|
| `format` | `mp4`, `mov`, `webm`, `gif`, `webp`, `png`, `png-seq`, `tiff-seq`, `exr-seq`, `jpg`, `avif` | `mp4` | `png`, `jpg`, `avif` are single stills (the frame at `poster`, else `range[0]`); `*-seq` are zips (`tiff-seq` 16-bit sRGB straight alpha; `exr-seq` half-float scene-linear premultiplied, `alpha: false` writes RGB); `gif`/`webp` animations. Lottie, After Effects scripts and canonical JSON come from `motion.convert`, not `output`. Which rows a build offers is probed from the pinned ffmpeg (`rexx-engine version --outputs`); a missing one is `output.format_unavailable` |
| `codec` | `h264`, `hevc`, `av1`, `vp9`, `prores` | mp4 → `h264`, mov → `prores`, webm → `vp9` (with `hdr`: `hevc` in mp4/mov, `av1` in webm) | must fit the container (`output.codec_container`) |
| `profile` | ProRes `proxy`, `lt`, `422`, `hq`, `4444`, `4444xq`; H.264 `high`, `high444`; HEVC `main`, `main10` (default), `rext` | from `quality` | `rext` picks the x265 profile by `pixelFormat` |
| `quality` | `draft`, `standard`, `high`, `master` | `standard` | §6 |
| `crf`, `bitrate`, `preset` | number; kbit/s; encoder preset string | from `quality` | expert overrides. `bitrate` replaces CRF with **two-pass VBR** (maxrate 1.5×, bufsize 2×; AV1 stays single-pass; per segment for long renders) |
| `encoder` | `cpu` \| `nvenc` | `cpu` | NVENC on a GPU box for `h264`, `hevc`, `av1` (presets `p1`–`p7`, `crf` as its `cq`, `bitrate` with multipass); refused with `output.encoder_unsupported` for `prores`, `vp9`, `alpha: true`, `hdr: "pq"`, `yuv422p10`, 4:4:4 AV1, image/sequence formats, outputs below 160 × 90, or a box without NVENC; never a silent CPU fallback |
| `fps` | a rate (number 1–240 or `"num/den"`) | the comp's | render at another rate: every output frame is sampled at its exact time (a 60 fps output of a 30 fps comp has 60 distinct frames; footage shows its own frames unless `frameBlend`) |
| `scale` | 0.25–2 | `null` (1; `draft` → 0.5) | output size = comp size × scale; vectors and text re-rasterize, footage resamples; exclusive with `size` |
| `size` | `[w, h]` | none | must keep the comp's aspect within 1 px (`output.size_aspect`); variants for other aspects |
| `range` | `[in, out]` | the whole comp | comp seconds only (frame forms are `doc.time_needs_comp`) |
| `alpha` | `false`, `true`, `"stacked"` | `false` | `true`: `mov`+`prores` (4444/XQ), `mov`+`hevc` (8-bit `yuva420p`, profile `main`, two-layer bitstream for Apple players), `webm`+`vp9`, `png`, `png-seq`, `webp`, `gif` (1-bit), `avif`, `tiff-seq`, `exr-seq`; `"stacked"`: colour on top (premultiplied over black) and alpha as luma below in an opaque video of twice the height, for `h264`/`hevc`/`vp9` in `mp4`/`mov`/`webm` (stacked AV1 is P3); otherwise `output.alpha_unsupported`. With alpha the comp `background` is ignored |
| `pixelFormat` | `yuv420p`, `yuv420p10`, `yuv422p10`, `yuv444p`, `yuv444p10`, `yuva420p`, `yuva420p10` (P3), `yuva444p10`, `rgba64` | from codec, quality and alpha | `rgba64` = 16-bit PNG; invalid for the codec is `output.pixel_format` |
| `toneMap` | `clip`, `soft`, `aces2` | `clip` | §4.2 |
| `gamutMap` | `clip`, `compress` | `clip` | §4.3 |
| `dither` | boolean | `true` | §4.3 |
| `transferTag` | `bt709`, `srgb` | `bt709` | §4.1 |
| `signalRange` | `limited`, `full` | `limited` | video signal range (named to avoid confusion with the time `range`) |
| `hdr` | `null`, `hlg`, `pq` | `null` | §4.4 |
| `hdrPeak` | 100–10,000 | `1000` | PQ only (`output.value` otherwise) |
| `audio.codec` | `aac`, `opus`, `pcm`, `none` | `aac` (mp4/mov), `opus` (webm) | `pcm` (24-bit) only in `mov` |
| `audio.bitrate` | kbit/s | 192 (AAC), 160 (Opus) | |
| `audio.limiter` | boolean | `true` | the true-peak limiter at −1 dBTP ([11](11-media-and-audio.md) §7) |
| `audio.loudness` | LUFS or `null` | `null` | e.g. `-14` (EBU R128 integrated, gain capped +12 dB) |
| `audio.always` | boolean | `false` | write a silent track when nothing is audible |
| `allowSolo` | boolean | `false` | let a render proceed with `solo` audio layers |
| `locale` | BCP-47 | `en-US` | template formatting when `data.locale` is absent |
| `poster` | `true`, a time, or `null` | `null` | also produce a PNG poster: `true` picks the latest layer `in` clamped to the range (an approximation, not entrance detection); a time picks that frame |
| `faststart` | boolean | `true` | MP4/MOV index at the front |
| `gif.fps` | 1–50 | `min(comp fps, 25)` | GIF timing is in 1/100 s; 25 and 50 divide it, 30 alternates 3 and 4 cs |
| `gif.palette` | `global`, `per-frame` | `global` | one 256-colour palette for all frames (stable, smaller) or one per frame (footage) |
| `gif.dither` | `none`, `bayer`, `blue-noise`, `floyd-steinberg` | `blue-noise` | ordered dithers animate better than error diffusion |
| `gif.colors` | 2–256 | 256 | |
| `gif.transparency` | boolean | follows `alpha` | 1-bit: pixels below 50 % alpha become transparent |
| `loop` | integer | `0` (forever) | GIF and animated WebP loop count |

Container × codec validity: `mp4`: `h264`, `hevc` (tag `hvc1`), `av1`; `mov`: `prores`, `h264`, `hevc`; `webm`: `vp9`, `av1`. Animated WebP: libwebp lossy 75 (`standard`), 90 (`high`), lossless (`master`), full alpha. GIF: two ffmpeg passes (`palettegen`, `paletteuse`).

## 6. Quality presets

| Codec | `draft` | `standard` | `high` | `master` |
|---|---|---|---|---|
| H.264 (libx264, 8-bit 4:2:0, High) | ultrafast, CRF 23, rendered at scale 0.5 | veryfast, CRF 18, `-tune animation` when the document has no footage | medium, CRF 16 | slow, CRF 14 (`high444` + `yuv444p` on request) |
| HEVC (libx265, Main10) | fast 28 | medium 23 | slow 20 | slow 16 |
| AV1 (SVT-AV1, 10-bit) | preset 10, CRF 38 | 8 / 32 | 6 / 27 | 4 / 20 |
| VP9 (libvpx, row-mt, constant quality) | realtime / cpu-used 8, CRF 38 | good / 4, 32 | good / 2, 28 | good / 1, 24 |
| ProRes | 422 LT (4444 with alpha), `prores` | 422 (4444) | 422 HQ (4444) | 4444 10-bit (4444 XQ with alpha), `prores_ks` |
| AVIF stills (libaom, 10-bit) | cpu-used 8, CRF 40, 4:2:0 | 6 / 30 / 4:2:0 | 4 / 22 / 4:4:4 | 2 / 12 / 4:4:4 (4:4:4 whenever alpha) |
| JPEG | | quality 90 | 95, 4:4:4 | 100, 4:4:4 |
| NVENC (`encoder: "nvenc"`) | p1; cq 23 / 34 / 42 (H.264 / HEVC / AV1); no B-frames, no AQ | p4; 26 / 27 / 33; 3 B-frames, spatial AQ | p5; 21 / 22 / 29 | p7; 20 / 18 / 24 |

**Deterministic files**: the same canonical document, assets, engine, ffmpeg build and settings give the same bytes (`-fflags +bitexact` on input and output, pinned encoder threads: x264 `sliced-threads` under VBV, x265 fixed pools, SVT-AV1 `--lp`, libaom `-threads 1`; no timestamps). Videos over 60 s are encoded as 10-second segments by independent encoders (closed GOPs) and concatenated without re-encoding, so chunked renders assemble to the one-box bytes (two-layer alpha streams are never segmented). Container metadata: colour tags, `rexx_version`, `motion_doc_sha256`, `comment` (`meta.title`), `rexx_backend=gpu` and `rexx_encoder=nvenc` when they apply.

## 7. Recommended outputs by destination

| Destination | Size and rate | `output` |
|---|---|---|
| TikTok | 1080 × 1920, 30 | `mp4` `h264` `standard`, `audio.loudness: -14`; comp `safe: "tiktok"` |
| Instagram / Facebook Reels | 1080 × 1920, 30 | `mp4` `h264` `standard`; `safe: "reels"`; HDR: HLG only |
| YouTube Shorts | 1080 × 1920, 30 or 60 | `mp4` `h264` `high` |
| YouTube | 1920 × 1080 or 3840 × 2160, 24–60 | `mp4` `h264` or `hevc` `high`; HDR `hdr: "pq"` or `"hlg"` with `hevc` |
| LinkedIn | 1080 × 1080, 1080 × 1350, 1920 × 1080, 30 | `mp4` `h264` `standard` (under 200 MB) |
| X | 1920 × 1080, 1080 × 1080, 1080 × 1920, 30 or 60 | `mp4` `h264` `standard` |
| web, opaque | as designed | `mp4` `h264` `standard` (plus `webm` `av1` where supported), `faststart` |
| web overlay with transparency | as designed | Chrome/Firefox `webm` `vp9` `alpha: true`; Safari `mov` `hevc` `alpha: true`; everywhere `alpha: "stacked"` with a small shader |
| editor hand-off (Premiere, Resolve, Final Cut, After Effects) | comp size and rate | `mov` `prores` `high` (422 HQ); `alpha: true` for 4444 |
| chat, email | ≤ 720 px, short | `gif` (`global`, `blue-noise`) or `webp`; Outlook shows only frame 1 |
| product / UI loops in apps | — | Lottie or dotLottie via `motion.convert` |
| broadcast / master archive | comp size and rate | `mov` `prores` `master` (4444 10-bit) |
| streaming-platform graphics delivery | UHD width at the finishing aspect | `tiff-seq` (16-bit) or `exr-seq` |

## 8. Examples

`examples/14-color-output.json`: every colour form in one document (hex, rgb, hsl, oklch, oklab, `color()` with P3, linear sRGB above 1, named, the object form, a theme reference with a modifier), an `acescg` nested comp inside a `display`-blended root with `srgb` interpolation keys, and an `output` block that sets every field (a ProRes 4444 master with alpha, `soft` tone mapping, `compress` gamut mapping, PCM audio with loudness, a poster, a GIF block carried for a later re-render). `examples/14-output-hdr.json`: an HLG `mp4`/`hevc` output with `aces2` and a PQ variant of the settings in `meta.notes`. Both check with 0 errors.
