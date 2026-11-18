# 02 — Higgsfield playbook: which model, mode and settings for each shot

For the Kiwi Go brand Reel (9:16, 15–25 s, silent export, no text or logos in AI frames).
Research date: 2026-11-18. No images or videos were generated for this document. Every price below is a **real quote** from `estimate_video_cost` / `estimate_image_cost` on this account: 9:16, sound off unless the model has no sound switch.

---

## 0. TL;DR

1. **The default pipeline stays the same:** a still start frame from `gpt_image_2_6` → image-to-video with **Kling 3.0 Pro** (`kling3_0`, `mode:"pro"`, `sound:"off"`) at **7.5 cr per 5 s**. The look comes from the still. The video model only adds motion.
2. **For transitions, use `kling_o3_flf` (Kling 3.0 Omni Frames).** It takes a start and an end frame, has `multi_shots`, and costs **6.25 cr per 5 s in Pro**, which is cheaper than `kling3_0` Pro. Use it for every end-frame-matched transition and for short multi-shot sequences.
3. **Premium models are the exception.** Cinema Studio 3.0 costs 65 cr at 1080p, Seedance 2.5 costs 80 cr at 1080p and Cinema Studio 4.0 costs 80 cr at 1080p. That is 9–13× the Kling price. With 489 credits, spend at most one premium shot, at 720p (25–35 cr), and only where Kling has failed twice.
4. **Consistency comes from images, not from words.** Make one approved character or object sheet, then build every start frame by editing from that sheet (`image_references`). No Higgsfield video model exposes a `seed`.
5. **The cheapest place to iterate is the still.** A start frame costs 0.25–2.75 cr; a video costs 6–80 cr. Never animate a still you would not ship as a poster.

---

## 1. Model capability map (from `models_explore`)

| Model id | Start / end frame | References | Multi-shot | Duration | Resolution / mode | Notes for us |
|---|---|---|---|---|---|---|
| `kling3_0` | start + end | — | not exposed here | 3–15 s | `std` / `pro` / `4k` | Proven workhorse. Pro gives 1076×1924 at 24 fps. `multi_shots` is **not** in this model's schema on Higgsfield; use `kling_o3_flf` for that. |
| `kling_o3_flf` (Kling 3.0 Omni Frames) | start + optional end | — | **yes** (`multi_shots` + `multi_prompt` [{prompt, duration}]) | 3–15 s | std / pro / 4k | **Best value for transitions and morphs.** |
| `kling_o3_image_reference` (Kling 3.0 Omni) | — | up to 7 images | yes | 3–15 s | std / pro / 4k | Reference-to-video. Locks the character or object from a sheet without a fixed first frame. |
| `kling3_0_turbo` | start only | — | — | 3–15 s | 720p / 1080p | Not cheaper than Pro (7.5 at 720p), so skip it. |
| `kling4_0` | start + end + **up to 10 ordered middle keyframes** | image refs, Kling elements | — | 3–30 s | 720p / 1080p | Keyframe "storyboard" moves. Has no sound switch. |
| `kling_4_0_flash` | start only | refs | — | 3–20 s | 720p only | It quoted 15 cr per 5 s, more than Kling 4.0 at 720p. Skip it. |
| `seedance_2_5` | start + end (**only in `omni_reference` mode**) | 30 images, 10 videos, 10 audio | — | 4–30 s | 480p / 720p / 1080p / 4k; **`draft`** → 480p, finalise within 7 days via `draft_job_id` | Best identity and reference handling, plus video_edit and extension. Expensive. |
| `seedance_2_5_flash` | start + end (omni) | 10 / 5 / 5 | — | 4–30 s | 480p / 720p | Not cheap (25 cr per 5 s at 720p). |
| `seedance_2_0` | start + end | 9 total | — | 4–15 s | `fast` (480/720p) / `std` (up to 4k) | `fast` 720p costs 12.5. It is a mid-price option for reference-driven people shots. |
| `cinematic_studio_3_0` | image / start / end | — | — | 4–15 s | 480p–4k, `genre` | The "most advanced cinema-grade" model. 25 cr at 720p, 65 at 1080p. |
| `cinematic_studio_video_4_0` | start + end (omni_reference only) | 30 images, 10 videos, 10 audio | (pacing control) | 4–30 s | 480p / 720p / 1080p | Director controls: `era_id`, `camera_model_id`, `camera_lens_id`, `camera_aperture_id`, `pacing_id`, `genre_id`, `light`/`light_id`/`light_custom` rig, `color_palette`. 35 cr at 720p. |
| `cinematic_studio_video_3_5` | start + end | 15 media | yes (max 6, custom/auto) | ≥4 s | 480–1080p | Has named presets: `camera_style` (e.g. `one_take`, `dreamy_flow`, `epic_scale`), `light_scheme` (e.g. `contre_jour`), `color_grading`, and a free `style_prompt`. 65 cr at 1080p. |
| `cinematic_studio_video_v2` | image / start / end | — | `multi_shots` with `multi_shot_mode` (the cost API **drops `multi_prompt`**, so only `auto` is reliable) | 3–12 s | `std` / `pro`, `speedramp` (slowmo, speedup, impact…), `genre`, `cfg_scale` | Very cheap (5 / 7.5 cr). Useful for a speed-ramped hero beat. |
| `minimax_h3_max` | start + end | 12 images, 12 videos | — | 5–15 s | 480p / **768p max** | 12.5 cr. The 768p ceiling is too low for finals. |
| `gemini_omni_flash_1_2` | start + end (i2v) | 7 images, 3 videos | — | 3–15 s (3–10 with end frame) | 360p–4k | Mid-price, 16.25 cr at 1080p. Has edit and extend modes. Always generates audio. |
| `grok_video_v15` | start only | 7 images | — | 2–15 s | 480–1080p | Strong physics and camera, but 40 cr at 1080p. |
| `flux_3_video` | start + end + 10 ordered middle frames | — | — | 5–20 s | 720p–4k | Storyboard-style. 40 cr at 1080p. |
| `wan2_6` | **no start frame** (one image ref only) | 1 image, 3 videos | — | 5 / 10 / 15 s | 720p / 1080p | Stylised and experimental. It cannot lock a frame, so do not use it for brand shots. |
| `wan3_0` | start + end (not combinable with refs) | 10 images | — | 2–30 s | up to 1080p, `enable_thinking` | 17.5 cr at 1080p. A reasonable fallback. |

**Start-frame and still models** (from `models_explore`, image):

| Model | Strength | Notes |
|---|---|---|
| `gpt_image_2_6` | Best prompt adherence. Edits from up to 16 `image_references`. `background:"transparent"` | Default for start and end frames. `quality` auto/low/medium/high/xhigh/max; `resolution` 1k/2k/4k. |
| `seedream_5_5` | Instruction editing, 2K, transparent PNG | The character-sheet workflow uses it for "drawn" styles (Classic 3D). Use it for sheets of the toy courier and the kiwi truck. |
| `seedream_v4_5` | 4K, up to 14 refs | Good for re-posing a locked object. |
| `nano_banana_pro` / `nano_banana_2` / `nano_banana_2_1` | Photoreal, up to 14 refs; **`nano_banana_2_1` has a `seed`** | The only seedable option. Use it for repeatable variants of a still. |
| `soul_2`, `soul_cinematic`, `soul_cast` | Realistic people with Soul-ID identity; cinematic stills | Use for photoreal humans if we go photoreal. Off-style for a miniature world. |
| `3d_jutsu_angles` | New camera angles of the same object or scene | Turnarounds of the truck or parcel without redrawing. |

**Bundled workflows** (`get_workflow_instructions`): the only one relevant to us is **`character-sheet`** (v2.0). Its "Classic 3D" or "CGI" drawn route makes a reusable sheet with `seedream_5_5` at 16:9 2K. Use it for the toy-like courier, seller and customer, and as a "creature/object" sheet for the kiwi truck. `product-photoshoot` covers stills only (packshots). Nothing bundled covers multi-shot video consistency, which is why section 5 exists.

---

## 2. Main table: shot type → model, mode and settings

All rows use 9:16, silent, with a `gpt_image_2_6` start frame unless the row says otherwise. Prices are the real quotes.

| # | Shot type | **Primary** (model + mode + settings) | Cost per clip | Why | Fallback / premium |
|---|---|---|---|---|---|
| a | **Stylised 3D or miniature hero object in motion** (kiwi-slice wheel rolling, parcel landing, kiwi-wheel truck driving) | Still: `gpt_image_2_6`, quality `high`, 2k (2.75; drafts at `medium` 2k = 1.0). Video: **`kling3_0`**, `mode:"pro"`, `duration:5`, `sound:"off"`, `medias:[start_image]` | **7.5** (5 s) / 15 (10 s) | Kling holds rigid-body shape well from a start frame and handles rolling and driving physics. The design is fixed in the still, so the wheel seeds stay in the still. Keep the wheel at small scale with motion blur so its seeds are not re-drawn frame by frame. | Speed-ramp "hero beat": `cinematic_studio_video_v2` `pro`, `speedramp:"impact"` or `"slowmo"`, 7.5 cr. Hard physics: `grok_video_v15` 720p, 22.5 cr. |
| b | **Tilt-shift miniature diorama aerial** (city in front of mountains, valley road), slow drone move | Still: `gpt_image_2_6` high 2k carrying the **whole** tilt-shift look: a narrow sharp band, blur top and bottom, golden backlight, toy scale. Video: **`kling3_0` pro 5 s** with one slow move ("slow forward drone drift, gentle descent"). | **7.5** | The miniature look is an image property. If the video model must invent it, it drifts back to "real". Kling keeps the start frame's depth of field. One slow move = no warping of buildings. | Premium hero aerial: `cinematic_studio_3_0` **720p**, `genre:"epic"`, start_image, 25 cr (1080p is 65). |
| c1 | **Continuous camera move** (crane up into golden clouds, push through a scene) | **`kling_o3_flf`** `mode:"pro"`, start_image **+ end_image**, 5 s (or 8–10 s for the crane), `sound:"off"` | **6.25** (5 s) / 12.5 (10 s) | The end frame forces the move to land exactly on the composition of the next shot, so the camera move becomes the transition. Cheaper than `kling3_0` Pro. | Many-keyframe crane (ground → rooftops → clouds): `kling4_0` `mode:"image-to-video"` 720p with start, end and 1–3 `image_references` as ordered middle frames, 11.25 cr per 5 s (16.25 at 1080p). Premium: `cinematic_studio_video_4_0` `omni_reference` 720p with start+end and pacing "Single Shot", 35 cr. |
| c2 | **Start/end-frame morph transition** between two scenes (parcel → truck, wheel → logo-free kiwi sun, city → clouds) | `kling_o3_flf` pro, 5 s, start = last frame of clip N, end = first frame of clip N+1 | **6.25** | Built for this case. Kling's own guidance is two related images plus the start–end function. | `kling3_0` pro with start+end also works (7.5). |
| d | **People**: seller packing a parcel, courier at a door, customer smiling. No hand or face distortion. | Still: `gpt_image_2_6` high 2k, edited from the approved **character sheet** (`image_references`). Video: **`kling3_0` pro 5 s**, micro-motion only. | **7.5** | A clean, sharp start frame with hands in a simple, readable pose is the biggest single fix. Kling Pro keeps faces stable when motion is small. The miniature or toy style (Classic 3D) also hides human-hand artefacts far better than photoreal. | When the face must hold through a turn or hands must manipulate: `seedance_2_5` `omni_reference` **720p** with start_image + sheet as `image_references`, 35 cr (or `seedance_2_0` `fast` 720p, 12.5 cr). Photoreal stills: `soul_2` (≈0.12 cr). |
| e | **Product-style macro** (parcel label, phone screen). The screen must be BLANK or green for compositing UI later. | Still: `gpt_image_2_6` high 2k. The screen is a **flat, evenly lit chroma green (#00B140)** or a matte black glass, with no reflections or UI. The label is a **blank cream sticker** with no print. Video: **`kling3_0` pro 5 s**, almost locked camera ("very slow push-in"). | **7.5** | Minimal camera motion = a stable planar track in compositing. Putting the blank or green screen in the still is the only reliable way, because video models tend to "invent" UI if asked to show a phone in use. | If the screen picks up glare or UI appears, cut the phone screen as a 2.5D layer: track the 4 corners and replace the whole screen area. `video_background_remover` is available for isolating the hand and phone. |
| f | **Multi-shot sequence with the same character or object** | 1) `character-sheet` workflow (Classic 3D route, `seedream_5_5` 2K 16:9, 3.5 cr). 2) Every start frame is a `gpt_image_2_6` edit with the sheet attached. 3) Each shot through `kling3_0` pro, **or** 2–3 shots in one generation through **`kling_o3_flf` pro `multi_shots:true`** + `multi_prompt` | 7.5 per shot / **12.5 per 10 s multi-shot** | The sheet is the identity anchor. Multi-shot in one call shares identity, grade and light inside the model. | `kling_o3_image_reference` pro (up to 7 refs, 7.5 cr per 5 s) when there is no fixed first frame. Premium: `seedance_2_5` omni_reference 720p (up to 30 refs), 35 cr. |

### Real price sheet (credits, 9:16, silent)

| Model / config | 5 s | 10 s |
|---|---|---|
| `kling3_0` std | 6.25 | 12.5 |
| **`kling3_0` pro** | **7.5** | **15** |
| `kling3_0` 4k | 30 | — |
| `kling3_0` std **with sound on** | 8.75 | — |
| `kling_o3_flf` std | 5 | 10 |
| **`kling_o3_flf` pro** | **6.25** | **12.5** (also 12.5 as a 2-shot `multi_shots`) |
| `kling_o3_image_reference` pro | 7.5 | — |
| `kling3_0_turbo` 720p / 1080p | 7.5 / 10 | — |
| `kling4_0` i2v 720p / 1080p | 11.25 / 16.25 | — / 32.5 |
| `kling_4_0_flash` 720p | 15 | — |
| `seedance_2_5` omni 480p (draft or not) | 15 | 30 (draft) |
| `seedance_2_5` omni 720p | 35 | 70 |
| `seedance_2_5` omni 1080p | 80 | — |
| `seedance_2_5_flash` 720p | 25 | — |
| `seedance_2_0` fast 720p / std 1080p | 12.5 / 60 | — |
| `cinematic_studio_3_0` 480p / 720p / 1080p | 17.5 / 25 / 65 | — / 50 / — |
| `cinematic_studio_video_4_0` omni 480p / 720p / 1080p | 15 / 35 / 80 | — |
| `cinematic_studio_video_3_5` 1080p | 65 | — |
| `cinematic_studio_video_v2` std / pro | 5 / 7.5 | — / 15 (pro) |
| `minimax_h3_max` 768p | 12.5 | 25 |
| `gemini_omni_flash_1_2` 720p / 1080p | 11.25 / 16.25 | — |
| `grok_video_v15` 720p / 1080p | 22.5 / 40 | — |
| `flux_3_video` 1080p | 40 | — |
| `wan2_6` 1080p | 10 | — |
| `wan3_0` 1080p | 17.5 | — |
| `veo3_1_lite` 8 s | 12 (8 s) | — |

| Image model / config | Credits |
|---|---|
| `gpt_image_2_6` default (auto quality) | 0.25 |
| `gpt_image_2_6` medium 2k | 1.0 |
| `gpt_image_2_6` high 1k | 1.5 |
| `gpt_image_2_6` high 2k | 2.75 |
| `seedream_v4_5` high | 1.0 |
| `seedream_5_5` 2k | 3.5 |
| `nano_banana` | 1.0 |
| `nano_banana_pro` 2k / `nano_banana_2` 2k / `nano_banana_2_1` 2k | 2.0 each |
| `soul_2` 2k / `soul_cinematic` 2k | 0.12 (billed as 1 in the rounded field) |

Price notes: the Seedance **finalise** price could not be quoted, because it needs a real `draft_job_id`. The catalog says the final is "billed for the draft's full duration at the selected resolution", so expect roughly the 720p or 1080p price on top of the 15 cr draft. Kling 4.0 and Gemini have no sound switch; strip the audio in ffmpeg.

---

## 3. Prompt-writing rules per model

### 3.1 Universal rules (all models, this Reel)
- **Image-to-video prompts describe motion, not the picture.** The still already defines subject, style and grade. Repeating the whole description makes the model "re-render" it and drift.
- **One camera move per clip, named with one cinematography verb:** dolly in, push in, pull back, crane up, pedestal up, orbit left, truck right, tilt up, slow drone drift, locked-off. Add speed ("slow", "very slow") and the end state ("…until the clouds fill the frame").
- **Order the prompt:** subject action → camera move → pace or end state → constraints.
- **Avoiding text is a still-stage job.** No video prompt phrase reliably removes signage, so the start frame must have none. In stills write: "unbranded, blank panels, no lettering, no signage, no numbers, no logos". In video add: "keep all surfaces blank".
- **Keep motion small for people.** Use micro-motions (breath, blink, a 5–10° head turn, a smile spreading, hands pressing tape down). Avoid big gestures (hand-to-face, waving, fingers counting).
- **Use the same "style anchor" sentence in every still,** word for word (see §4).
- Use a 5–8 term negative list where the model accepts one. On Higgsfield's MCP only the prompt is exposed, so put the constraints as a short sentence at the end: "No morphing, no warping, no extra fingers, no text."

### 3.2 Kling 3.0 / Kling 3.0 Omni (`kling3_0`, `kling_o3_flf`, `kling_o3_image_reference`)
Structure: *[what moves] + [camera move + speed] + [end state] + [physics or constraint]*. Keep it to 1–3 sentences. Kling infers a lot from the frame, so prompt sparingly.

- GOOD (a): `The toy delivery truck rolls forward along the mountain road, its kiwi-slice wheels turning steadily; low tracking shot following alongside at the same speed; dust puffs behind the wheels. Body shape and wheel design stay exactly as in the first frame, all panels stay blank.`
- BAD (a): `Kiwi Go truck with logo driving fast, epic cinematic 8k masterpiece, amazing, camera flies around` (it asks for a logo, gives no single move, uses quality buzzwords and invites a spinning orbit that warps the body).
- GOOD (c, with end frame): `One continuous crane up: the camera rises from the miniature rooftops past the courier waving, up into warm golden clouds, ending exactly on the cloudscape of the last frame. Smooth, slow, no cuts.`
- BAD (c): `transition to clouds` (no path is given, so Kling may cross-dissolve or morph the rooftops into clouds).
- GOOD (multi-shot `multi_prompt`): `[{"prompt":"Shot 1, close-up: the seller's hands press tape across the cream parcel, slow push in","duration":3},{"prompt":"Shot 2, medium: the same seller slides the parcel across the counter toward camera, locked-off","duration":3}]`. Label shot size and move on each shot, and keep the character description identical in each.

### 3.3 Seedance 2.5 / Seedance 2.0 (`omni_reference`)
Structure (a six-part formula is widely quoted; only subject and action are required): **Subject → Action → Scene → Style → Camera → (Sound: omit, we're silent)**. Address references by position: **`@image1`, `@image2`…** (`@video1`, `@audio1`), give each a role once, and then use the role name.

- GOOD (d): `@image1 is the first frame. @image2 is the character sheet for the courier. The courier from @image2 knocks twice on the wooden door, then smiles as it opens; hands stay relaxed at chest height holding the parcel. Warm late-afternoon miniature world, shallow depth of field. Camera: locked-off medium shot, very slow push in. Keep his face, cap and jacket identical to @image2; no text anywhere.`
- BAD (d): `courier delivers package to happy customer, realistic, cinematic` (no reference roles, no camera, and an undefined "realistic" style that conflicts with the miniature world).
- Seedance writes long timelines well ("0–2 s: …; 2–4 s: …"). Use that for a 6–8 s people beat instead of multi-shot.
- Draft rule: **write the final prompt for the draft.** The final renders the draft (`draft_job_id`), so the prompt cannot change between them.

### 3.4 Cinema Studio (`cinematic_studio_3_0`, `cinematic_studio_video_4_0`, `_3_5`, `_v2`)
- Put **look and lens in the controls, not in the prompt.** 4.0: set `camera_lens_id`, `camera_aperture_id` (f/1.4 for strong miniature blur), `genre_id`, `era_id`, `light`. Set **pacing to "Single Shot"**: one tutorial found Auto pacing split 5 of 6 five-second clips into cuts. The control ids are not listed in the catalog; read them in the Higgsfield UI or by trial `estimate_video_cost` calls.
- 3.5: `camera_style:"one_take"` or `"dreamy_flow"` for the crane, `light_scheme:"contre_jour"` for golden backlight, `color_grading:"bleached_warm"`, plus a `style_prompt` holding the style anchor. Set `prompt_language:"en"` (the default is `zh`).
- 3.0: only `genre` is available, so the prompt carries the move. Use `genre:"epic"` for aerials and `"drama"` or `"auto"` for people.
- v2: `speedramp:"impact"` or `"slowmo"` for one hero beat on the beat drop. Keep `cfg_scale` 0.5–0.7.
- GOOD: `Slow helicopter drift over a tilt-shift miniature valley city toward the snowy mountains; sun flare low on the right; the camera eases forward and slightly down.` (with genre epic, f/1.4, Single Shot)
- BAD: `35mm anamorphic lens, f1.4, ARRI Alexa, 1970s film grain, cinematic` written into the prompt *while* the controls point elsewhere. Conflicting instructions lead to random results.

### 3.5 Other models (only if needed)
- `kling4_0` keyframes: list the middle frames in order in `image_references` and describe the path through them: "camera rises through frame 2 then frame 3".
- `gemini_omni_flash_1_2`: `mode` is **required**. With an end frame the duration is capped at 10 s.
- `wan3_0`: a start frame cannot be combined with references. Pick one or the other.
- `wan2_6`: it has no start frame, so do not use it for locked brand shots.

### 3.6 Start-frame prompts (`gpt_image_2_6`)
- Always 9:16, `quality:"high"`, `resolution:"2k"` for finals; `medium` for exploration.
- Compose for the move. For a crane up, leave sky headroom. For a push-in, the subject is centred with space around it. For a transition, the start and end frames share colour, light direction and horizon height.
- GOOD (e): `Extreme macro of a smartphone lying on a cream linen surface, screen facing camera, the screen is a perfectly flat, evenly lit solid chroma-green rectangle (#00B140) with no reflections, no icons, no text; a seller's fingertip rests at the lower edge; warm golden side light, shallow depth of field, [STYLE ANCHOR].`
- BAD (e): `phone showing the Kiwi Go app tracking screen` (the AI draws fake UI and fake text, which is exactly what we composite ourselves).

---

## 4. Consistency across shots

1. **Style anchor.** Paste one sentence verbatim into every still and every Seedance or Cinema Studio prompt:
   `Tilt-shift miniature diorama world, toy-like handcrafted 3D figures and vehicles, warm golden-hour backlight with soft bloom, shallow depth of field with a narrow sharp band, cream and lime accents (#F6F1E4, #B8F03C) against ink-dark details, clean unbranded surfaces with no text or logos.`
2. **One sheet per recurring subject, approved before any video.**
   - Courier, seller, customer: `character-sheet` workflow, **Classic 3D** route (seedream_5_5, 16:9, 2K, 3.5 cr each).
   - Kiwi-wheel truck, parcel: a "creature or object" sheet, or a `gpt_image_2_6` turnaround (front, ¾, side). Use `3d_jutsu_angles` for extra angles of the same object. The wheel is the logo motif, so the AI only draws a *generic* kiwi-slice wheel. The exact logo stays in compositing.
3. **Every start frame is an edit, not a fresh generation.** Use `gpt_image_2_6` with `image_references:[sheet, previous approved frame]` and "same character, same truck, same lighting as the references". This is the most reliable lock.
4. **No video seed exists** on any Higgsfield video model (checked in every schema). The only seed is on `nano_banana_2_1` (stills). Repeatability comes from reusing the approved frames and references.
5. **Chain frames.** Extract the last frame of an approved clip (ffmpeg) and use it as the next clip's `start_image`. This gives continuity across cuts and is needed for transitions.
6. **Inside-model consistency:** `kling_o3_flf` `multi_shots` for 2–3 beats of the same subject in one 10 s call (12.5 cr), or `seedance_2_5` / `kling_o3_image_reference` with the sheet in `image_references`.
7. **One grade in post.** Apply the same LUT or curves to every clip in ffmpeg. Do not depend on the AI for matched colour.

---

## 5. End-frame-matched transitions (the reference's "camera move IS the transition")

1. Generate the **destination frame first** (the first frame of the next shot, e.g. the golden-clouds frame where the mascot will be composited).
2. Generate the **origin frame** as an edit of the destination with matched colour temperature, light direction and horizon. Their difference should be *spatial* (where the camera is), not *stylistic*.
3. Animate with `kling_o3_flf` pro, `start_image` = origin and `end_image` = destination, 5–8 s. Name the camera path explicitly: "continuous crane up from X through Y, ending on the final frame".
4. In the edit, cut the next clip on its first frame, which is identical to the transition's last frame, so the cut is invisible.
5. For **morph transitions** (an object turning into another), keep the silhouette and position close (a round kiwi wheel → a round sun; a parcel → the truck's cargo box at the same screen spot). Prompt "the X smoothly transforms into Y in place, the camera holds steady". Very different frames fail to resolve.
6. To keep the first frames crisp before the move starts, add "hold the first frame still for half a second, then begin the move".
7. Cover any remaining seam with the orange **light-leak flash** from the reference (composited, about 8–12 frames), as the reference itself does at 4.3 s.
8. Constraint: on Kling Omni an end frame **cannot be combined with reference images**. If you need both, put the identity into the frames themselves.

---

## 6. Cheap test strategy

| Stage | What | Model and config | Cost |
|---|---|---|---|
| 0 | Concept stills, 2–4 variants per shot | `gpt_image_2_6` default (0.25) or `medium` 2k (1.0) | 0.25–1 each |
| 1 | Character and object sheets | `character-sheet` → `seedream_5_5` 2K | 3.5 each |
| 2 | Final start and end frames | `gpt_image_2_6` `high` 2k | 2.75 each |
| 3 | **Motion test** of risky shots (people, morphs) | `kling_o3_flf` **std** 5 s (5 cr) or `cinematic_studio_video_v2` std (5 cr) | 5 |
| 4 | Final | `kling3_0` pro (7.5) / `kling_o3_flf` pro (6.25) | 6.25–7.5 |
| 5 | Premium only if Kling failed twice | Cinema Studio 3.0 720p (25), or Seedance 2.5 **draft 480p (15) → finalise 720p** | 25–50 |

Key facts for this account:
- **Kling std vs pro is only 1.25 cr apart.** For simple shots (aerials, objects), skip the std test and go straight to Pro. Test only the risky shots on std.
- **Seedance draft is not a discount** (15 cr = the plain 480p price). It saves money only because you *reject* bad drafts before paying 35–80 for a final. Use it only if a Seedance shot is unavoidable.
- Never use 4k or 1080p premium modes. Reels are compressed to about 1080×1920 anyway; Kling Pro's 1076×1924 is already native.
- Review every still at 100 % for text, letters, logos, extra fingers and branded vans before spending video credits.

---

## 7. Realistic budget: a 15–25 s Reel of 4–6 clips

Assumed shot plan (5 AI clips plus composited end card): hero object (a), miniature aerial (b), people beat (d), macro phone/label (e), crane transition into clouds (c), with the same courier or truck across shots (f).

| Line | Qty | Unit | Credits |
|---|---|---|---|
| Character and object sheets (courier, seller/customer, truck) | 3 | 3.5 | 10.5 |
| Exploration stills (about 4 per shot × 5 shots) | 20 | 0.25–1 | ~12 |
| Final start frames (incl. 1 redo each) | 10 | 2.75 | 27.5 |
| End frames for 2 transitions (incl. redo) | 4 | 2.75 | 11 |
| Motion tests on std (people, morph) | 3 | 5 | 15 |
| Finals: 4 × `kling3_0` pro 5 s | 4 | 7.5 | 30 |
| Final: crane transition `kling_o3_flf` pro 8–10 s | 1 | 12.5 | 12.5 |
| **Retries**: Kling finals × 1.5 extra on average (people and macro need the most) | ~7 | 7.5 | 52.5 |
| **Subtotal (Kling-only plan)** | | | **≈ 171** |
| Optional premium shot: Cinema Studio 3.0 720p (aerial) or Seedance 2.5 720p (people), 1 try + 1 retry | 2 | 25–35 | 50–70 |
| **Total with one premium shot** | | | **≈ 220–240** |

- This leaves **about 250 of the 489 credits in reserve** for client revisions, a second version or a 6th clip.
- Do **not** plan a Reel around Seedance 1080p (80) or Cinema Studio 3.0 1080p (65). Six such clips with retries would be over 900 credits.
- Hard stop rule: if a shot fails Kling Pro **three** times, change the *still* (composition, less motion) before you change the model.

---

## 8. Shot-specific risk checklist

| Risk | Where | Mitigation |
|---|---|---|
| Wheel seeds or kiwi texture "boiling" | a | Fast rotation + motion blur, a small wheel in frame, no extreme close-up of a turning wheel. A hero close-up of the wheel is a composite of our SVG logo, not AI. |
| Buildings warp in the aerial | b | One slow move, no orbit, 5 s maximum, a busy but static city in the still. |
| Morph "melts" instead of moving | c | Matched frames, an explicit path, 5–8 s, a light-leak cover. |
| Extra fingers or face drift | d | Hands busy with one simple action, toy style, micro-motion, Seedance with a sheet as the fallback. |
| Fake UI or text on screen, glare on the green | e | The screen is solid green in the still, matte, angled away from the key light. If it still fails, do a 2.5D screen replacement. |
| Gibberish lettering on vans, boxes, doors | all | Blank panels in stills; check every still at 100 %. If text appears later, cover it with our composited brand panel. |

---

## Sources
- Higgsfield MCP: `models_explore` (list/get), `estimate_video_cost`, `estimate_image_cost`, `get_workflow_instructions` (catalog + `character-sheet` v2.0), queried 2026-11-18.
- [Atlabs — Kling 3.0 prompting guide](https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation)
- [fal.ai — How to use Kling 3.0 Pro](https://fal.ai/learn/tools/how-to-use-kling-3-0-pro)
- [Magic Hour — Kling 3.0 reference guide: Elements, Multi-Shot](https://magichour.ai/blog/kling-30-reference-guide)
- [Magic Hour — How to use Kling 3.0](https://magichour.ai/blog/how-to-use-kling-30)
- [Kling — Negative prompts: fix video distortion](https://kling.ai/blog/kling-ai-negative-prompts-fix-video-distortion)
- [Atlas Cloud — Kling 3.0 character consistency](https://www.atlascloud.ai/blog/guides/how-to-use-kling-3.0-for-character-consistency)
- [Kling — Start & end frames quickstart](https://kling.ai/quickstart/ai-video-start-end-frames)
- [Higgsfield — Kling Start End Frames](https://higgsfield.ai/blog/Kling-Start-End-Frames)
- [Artlist — Seamless AI transitions with first and last frames](https://www.artlist.io/blog/ai-video-transitions)
- [Dreamina — Plan first/last frames for a plausible transition](https://dreamina.capcut.com/ai-video/plan-first-last-frame-transition)
- [RunComfy — Kling 3.0 Omni First-Last-Frame node (limits)](https://www.runcomfy.com/comfyui-nodes/ComfyUI/kling-omni-pro-first-last-frame-node)
- [Segmind — Seedance 2.5 six-part formula](https://blog.segmind.com/the-official-seedance-2-5-prompt-guide-bytedances-six-part-formula-explained-with-examples/)
- [RunDiffusion — Seedance 2.5 prompt guide](https://www.rundiffusion.com/seedance-2-5-prompt-guide)
- [Scenario — Seedance 2.5 essentials (draft → finalise, @image tags)](https://help.scenario.com/articles/1651934064-seedance-2-5-the-essentials)
- [Muapi — Seedance 2.5 omni reference (draft flow, 7-day finalise)](https://muapi.ai/playground/seedance-2.5-omni-reference-4k)
- [Runware — Seedance 2.5 multi-reference production](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/multi-reference-production)
- [Higgsfield — Cinema Studio 4.0](https://higgsfield.ai/blog/cinema-studio-4-0) and [complete guide](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide)
- [Higgsfield — Cinema Studio 3.5 tutorial](https://higgsfield.ai/blog/cinema-studio-3.5-full-tutorial)
- [Wavespeed — Higgsfield Cinema Studio review](https://wavespeed.ai/blog/ai-workflows/higgsfield-cinema-studio-review/)
- [Carat — tilt-shift prompt gallery](https://carat.im/en/prompt-gallery/tilt-shift)
- [Atlas Cloud — AI miniature effect](https://www.atlascloud.ai/blog/tips/ai-miniature-effect)
- [Artlist — Troubleshooting AI image and video (text)](https://help.artlist.io/hc/en-us/articles/33156143103773-AI-Toolkit-Troubleshooting-AI-Image-and-Video)
- [HackerNoon — Adding text to AI video without it breaking](https://hackernoon.com/how-to-add-text-to-ai-generated-video-without-it-looking-broken)
- [Morphic — Green screen (keying limits)](https://morphic.com/id/ai-glossary/green-screen)

Caveat: most web sources are vendor or third-party blogs. The camera-control ids for Cinema Studio 4.0 are not listed in the MCP catalog, so look them up in the UI before using that model.

---

## Summary
- Default: `gpt_image_2_6` still (high 2k, 2.75 cr) → `kling3_0` Pro 5 s silent (7.5 cr). Use it for hero objects, aerials, people and macro shots.
- Transitions and morphs: `kling_o3_flf` Pro with start+end frames (6.25 cr per 5 s, 12.5 per 10 s). It is cheaper than Kling 3.0 Pro and also has `multi_shots`.
- Multi-keyframe crane: `kling4_0` i2v 720p (11.25 cr) with ordered middle frames.
- Premium is reserved for one shot at most: Cinema Studio 3.0 720p (25), Cinema Studio 4.0 or Seedance 2.5 at 720p (35). Their 1080p tiers cost 65–80 cr per clip.
- People: toy or Classic 3D style, a character sheet as the identity anchor, micro-motion only. Seedance 2.5 omni_reference 720p is the fallback.
- Phone or label: a solid chroma-green screen and a blank label in the still, near-locked camera, UI composited later.
- Consistency: a verbatim style anchor, a sheet per subject, every start frame edited from refs, last-frame chaining, one grade in post. No video model exposes a seed.
- Testing: iterate on stills (0.25–1 cr). Test only the risky shots on Kling std (5 cr). Kling std vs pro is just 1.25 cr apart. A Seedance draft (15 cr) saves money only by rejecting drafts.
- Budget: about 171 cr for a 5-clip Kling-only Reel with retries, or about 220–240 cr with one premium shot. That leaves about 250 of 489 cr in reserve.
