# 32 · Lint: every rule, its threshold and its fix

Lint runs after validation on the canonical document (at most 60 sample times per comp plus every key time; a
coarse 1/8 frame for colour checks). It never blocks a render and never changes the document. Source:
`engine/crates/rexx-lint/src/{lib,rules_text,rules_motion,rules_misc,markers}.rs`, spec 14 §14.4. Every rule is
a `warning` unless marked (i) info. The `codes::ALL` table of `rexx-lint` is the authority on severity.

## Configuration

Document: `"lint": { "platform": "tiktok", "disable": ["lint.linear_spatial_ease"], "readingSpeed": 3, "contrast": 3 }`
(top level; never affects rendering). Per call: `motion.check`'s `lint: { platform, disable }` (platform replaces,
disable adds). `platform`: `none` (default: the comp's own title-safe box, inset 10 % of the shorter side), or a
safe-area preset `broadcast`, `youtube`, `reels`, `tiktok`, `shorts`, `story`, `square`, `linkedin`, `x` (a
portrait-only preset on a landscape comp uses `broadcast`). `disable` takes any warning or info code (a bare rule
name without `lint.` also matches); it silences the normalizer's `physics.*` and `track.*` warnings too, in
`check`, `frames` and `render`; errors are never silenced. `readingSpeed` words per second (3), `contrast` the
minimum ratio (3); non-finite or non-positive values are ignored.

Rules marked (m) are fed by markers the normalizer leaves in the canonical document's `x-lint` field (at most 1,000
read); lint re-emits them with the code's severity.

## The rules

| Code | Fires when | Threshold / detail | Fix |
|---|---|---|---|
| `lint.opacity_fraction` | an opacity in (0, 1], non-integer | CSS thinking | `fix` multiplies by 100 |
| `lint.text_too_short_on_screen` | a text layer is fully visible (≥ 90 % of its peak opacity, capped at 90; whole inside the frame) for less than its reading time | max(0.7 s, words / `readingSpeed`); CJK: 2 characters = 1 word; skipped for text inside component-sized comps, paged/word-timed text, crawls, text larger than the frame | hold longer, cut words, sequence exits later |
| `lint.text_outside_safe_area` | text bounds outside the title-safe box or the platform zone while visible | bounds through the layer's and parents' 2D transforms; text inside a component instance is checked in the frame, through the instance's transform, reported at the instance layer | `align: { "to": "safe" }`; set `safe` and `lint.platform` per variant |
| `lint.offscreen_while_visible` | a layer's bounds entirely outside the comp for > 0.5 s while in range with opacity > 0 | bounds inflated 0.5 px; matte sources and parents excluded; per-unit physics bodies tested where the bake puts them; a shadow-casting 3D layer under a shadow light skipped | check units and percent signs |
| `lint.linear_spatial_ease` | a position/anchor segment over 50 px with `linear`, outside loops and `rove` chains | (i) when every changing segment (≥ 2) is linear; crawl-shaped segments skipped | an ease, or disable for constant-speed designs |
| `lint.too_many_simultaneous_moves` | > 5 layers start a move within 100 ms | staggered starts do not count | stagger |
| `lint.tween_overlap` (m) | a tween cut an earlier animated span on the same property | both tweens reported | re-sequence; `at: ">"` |
| `lint.unused_layer` (i) | never visible in its span and not a matte, parent or expression source | | remove it |
| `lint.hidden_never_shown` | opacity 0 at every key, no drivers or expression | | add the entrance |
| `lint.low_contrast_text` | text contrast below `contrast` (3:1) at the middle of its visible span | WCAG ratio against the median of the coarse backdrop; stroke counts as the edge colour | a plate, a stroke, a darker grade, `$theme.color.accent.on` |
| `lint.tiny_text` | cap height below 2.5 % of the shorter side (portrait or square variants) or 1.8 % (landscape) | at the text's scale × parents | larger `size` |
| `lint.same_ease_everywhere` (i) | > 80 % of ≥ 10 animated segments share one ease | | theme ease tokens |
| `lint.enter_exit_same_curve` (i) | an entrance and exit with the identical (not mirrored) ease | | `.in` curves on exits |
| `lint.stagger_too_fast` | `each` < 0.012 s with > 4 targets | staggers inferred from animators and evenly offset layers | 0.02–0.08 s |
| `lint.stagger_too_slow` | spread > 2 s, or `each` > 0.25 s with > 6 targets | | shorter `each` |
| `lint.element_jitter` | thin text or lines moving < 0.5 px per frame for > 1 s at a non-integer scale | | motion blur or a faster move |
| `lint.motion_blur_off_fast_motion` | > 40 px per frame without motion blur | | `motionBlur: true` on the layer |
| `lint.motion_blur_nested_render` | `motionBlur: true` on a `collapse: true` comp layer or under a `time.*` effect (with comp motion blur on) | every shutter sample re-renders the nested image (an uncollapsed comp layer renders once and blurs only its transform) | blur inside the nested comp, drop `collapse`, or blur the source precomp |
| `lint.missing_exit` | a fully visible element is cut at its `out` while the comp continues, or at the comp's end when it is the only one ending there | comp layers count as exiting when their inner layers do (to 8 levels); a full-frame background may end with the comp | an exit preset, or end with a cut shared by other elements |
| `lint.duration_mismatch` | the comp is > 0.5 s longer or shorter than its longest audio layer, or a music bed (≥ 5 s) ends without a fade in its last 0.5 s | needs probed durations for audio without `out` | `fadeOut`; match lengths |
| `lint.loud_audio` | true peak > −1 dBTP or integrated loudness outside −14 ± 2 LUFS | measured on the mixdown | lower `volume`; `output.audio.loudness: -14` |
| `lint.font_fallback_used` | as `font.fallback_used`, once per layer | | expected for emoji and CJK |
| `lint.expensive_effect` | an effect or layer over 30 % of the frame budget (1000 / fps ms), or a frame estimated over 500 ms at 1080p | the message names the estimate and a cheaper alternative | smaller radius, fewer layers, `quality: "draft"` for previews |
| `lint.unbalanced_composition` (i) | the visual centre of mass at a held moment over 30 % off centre with nothing on the other side (emitted in 0.1.48, spec marks it P3) | | balance the frame or disable |
| `lint.beat_near_miss` (i) | a key within 2 frames of a detected beat but not on it | `fix` snaps it | `at: "@beatN"` |
| `lint.on_beat` (i) | keys landing on beats: `"<id>" has n of m keys on the beat: …` (also `beat_hits n/m` in the timing sheet) | positive evidence | — |
| `lint.fitto_overrides_size` | a rect with `fitTo` and its own `size`/`position` on a fitted axis | | drop them |
| `lint.paint_above_merge` | a fill or stroke above a merge-paths item in its group | it stops contributing | move the paint below |
| `lint.morph_open_closed` | a morph between an open and a closed path | | match them |
| `lint.ligatures_disabled` (i) | ligatures switched off for per-character animation | | expected |
| `lint.bitmap_emoji_scaled` | bitmap emoji scaled far above native | | smaller |
| `lint.paragraph_needs_box` (i) | justify or `verticalAlign` on point text (ignored) | | `box` text |
| `lint.blend_clamps_hdr` | a range-limited blend mode clamping values above 1 | | `add`/`screen` |
| `lint.matte_source_hidden` (i) | a matte source hidden by default | | `visible: true` if it should show |
| `lint.echo_static_source` | `time.echo` on a layer whose content does not change | | animate the source |
| `lint.lights_without_ambient` | enabled lights, no ambient/environment light, and a 3D layer to light (collapsed comps counted; skipped under a lit parent) | unlit sides render black | add an ambient light |
| `lint.material_field_unused` (i) | an advanced-renderer material field; a classic field on a 3D layer in an unlit, uncollapsed comp; `material` on a 2D, camera or light layer | | remove or add lights |
| `lint.media_past_end` | a media layer past its source with `loop: false` | needs the probed duration | `loop: true` or shorten `out` |
| `lint.media_reverse_long_gop` | reversed or remapped long-GOP video | slow decode | an intra-only proxy (ProRes) |
| `lint.beats_unstable` | low-confidence beat tracking | | give `tempo` |
| `lint.beats_none` (i, m), `lint.beats_grid` (i, m) | no beats found with `fallback: "none"`; a tempo grid emitted instead | speech has no beats | labels for VO; `tempo` |
| `lint.expr_implicit_var` (i, m) | a top-level assignment rewritten to `var` | | add `var` |
| `lint.expr_prefer_driver` (i) | an expression a driver expresses (`wiggle`, `loopOut`) | | the driver |
| `lint.expr_array_equality` | `==` between non-vector arrays or objects (identity, not value) | | compare components |
| `lint.expr_mb_cost` | an expensive expression evaluated per motion-blur sample | | simplify or `motionBlur: false` |
| `lint.chroma_text` | thin saturated text that 4:2:0 subsampling will smear | | larger or less saturated text, `yuv444p` |
| `lint.track_fast_motion` (m) | a tracked target over 40 px/frame with motion blur and `keysPerFrame: 1` | | `keysPerFrame: 2` |
| `lint.track_outside_range` (m) | the target's visible span extends beyond the track's range | | trim `in`/`out` or track more |
| `lint.crawl_fractional_speed` | scrolling text at a non-integer px per frame | jitter | the `crawl` field or `credits.crawl` |
| `lint.motion_blur_on_scroll_text` | motion blur on a crawl | legibility | `motionBlur: false` |
| `lint.crawl_too_fast` | a crawl faster than max(4 px, size / 6) · 24 / fps per frame | | slower |
| `lint.crawl_duration_mismatch` (m) | a crawl's requested `duration` rounded by over 5 % | | accept or change the text |
| `lint.credits_white_hot` | a credits `white` or crawl text fill with a channel over 235 | broadcast white | `#EBEBEB` |
| `lint.credits_kind_skipped` (i, m) | a credits section whose `kind` the component does not render | | another component or kind |
| `physics.idle_span` (i, m) | nothing moved for > 2 s before `end` | | shorten `end` |

Every lint warning with a mechanical fix carries `fix`. Rules that need engine data (`lint.tiny_text`,
`lint.low_contrast_text`, `lint.font_fallback_used`, `lint.bitmap_emoji_scaled`, `lint.loud_audio`,
`lint.media_past_end`) are silent when the sampler cannot supply it rather than guessing.

