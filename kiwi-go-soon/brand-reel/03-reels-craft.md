# 03 — Reels craft: reference teardown, critique of our old film, research, and a publishing checklist

Author role: short-form video analyst (Instagram Reels for brands). Written 2026-11-18.
Inputs: `research/reference/reference.mp4` (360×640, 30 fps, 17.25 s, AAC stereo) and `../higgsfield/brand-film/kiwi-go-brand-film.mp4` (1080×1920, 30 fps, 17.0 s, no audio), plus `../higgsfield/brand-film/edit.py`.
Method: ffmpeg frame extraction (a 0.5 s contact sheet, plus 0.25 s strips around every transition), and a numpy pass over 90×160 luma/RGB frames. That pass measured mean absolute frame difference (motion and cuts), mean luma, saturation and RGB balance (grade), and Laplacian sharpness of the top, middle and bottom thirds (depth of field). Audio was measured as RMS per 0.5 s, energy onsets, a spectral-flux autocorrelation for tempo, and the spectral centroid.
Frames kept (small JPGs): `research/frames/ref/` and `research/frames/old/`. Each has `sheet_0p5s.jpg` plus the `t*_*.jpg` transition strips; the time range is in each file name, and the timecode burnt into each strip is relative to that range.

---

## 1. Teardown of the reference Reel

### 1.1 Measured timeline (seconds)

| # | Time | Duration | What is on screen | Measured evidence |
|---|---|---|---|---|
| A | 0.00–1.9 | (part of shot 1) | **Open from white.** The miniature walker is already visible *through* a creamy white haze, which clears over about 1.9 s. | Luma 225 → 172 by 1.87 s; saturation 0.08 → 0.34. The image is never fully blank, so the subject is readable from frame 1. |
| 1 | 0.0–5.0 | **≈5.0 s** | Tilt-shift miniature: a toy character with a backpack walks up a rocky path. Follow-cam from behind and slightly above, with a gentle handheld bob. City bokeh and blue mountains behind. | Motion 6–8 (steady walk-and-push). Sharpness profile top / mid / bottom ≈ 11 / 26 / 21, so the sharp band runs through the character and the foreground and top are soft. |
| T1 | 4.6–5.6 | ≈1.0 s | **Orange light leak / burn.** Warm yellow-orange blobs sweep in from the left over the walker, then everything burns out to cream. The hard cut hides inside the white. | Luma 140 → 220 (5.33 s), then a hard cut at **5.57 s** (biggest frame difference in the film, 31). Sharpness falls to about 1. |
| 2 | 5.6–≈8.5 | ≈3 s | Miniature city aerial in front of mountains. Slow forward drift, a soft lens-flare orb, autumn-red trees. Cooler, cleaner palette. | Motion only 1–3 (calm after the burst). DOF gradient: top 5, middle 24, bottom 39, which is a classic tilt-shift band with sharp foreground and soft distance. |
| 3 | ≈8.5–13.2 | ≈4.7 s | **Crane up into the clouds.** The same city shot continues as the camera tilts and rises: the skyline sinks, clouds roll in through mid-frame, and golden cumulus fills the top 2/3. | Motion rises to 5–7 at 9.0–10.0 s, the fastest camera move. Middle-third sharpness falls 24 → 5 as the frame fills with soft cloud. Possible hidden join at about 8.3 s (diff 4.4, luma dip 150 → 141); it reads as one move. |
| 4 | 11.75–13.2 | ≈1.5 s (overlaps 3) | **Logo in the sky.** The brand mark pops in at about 35 % of frame width, centred about 42 % from the top. It is screen-locked while the clouds keep moving under it. Then a sun flare blooms from the top edge. | 11.73 s: mid-third sharpness jumps 5 → 18 (a crisp vector mark appears on soft cloud). No fly-in: a 1–3 frame pop or scale-in. Flare from 12.8 s; luma 168 → 181. |
| T2 | 13.07–13.25 | ≈0.2 s | **White flash cut** to the end card. | Diff 29.5 at 13.20 s; luma jumps to 227 (warm off-white, RGB 230/224/218). |
| 5 | 13.2–15.6 | ≈2.4 s | **End card.** Off-white paper. The icon sits left-of-centre at the same height as the sky logo. The wordmark **types on letter by letter** (about 0.2 s per glyph, 13.2–14.0 s). A tiny grey descriptor line fades in at about 14.0–14.3 s. Hold. | Absolutely static: diff 0.0–0.3, saturation 0.05. Sharpness only in the middle third (≈25). |
| T3 | 15.6–16.2 | ≈0.6 s | **Outro flare.** A pink-peach anamorphic flare with a vertical string of bokeh orbs washes over the card, then the image dips to a dark teal-black. | Diff 20–22 for 6 frames; luma 225 → 39 → 0. |
| — | 16.2–17.25 | ≈1.0 s | Black (dead tail). | Luma 0. |

**Pacing:** effectively **3 shots plus 1 card in 17 s**: 5.0 s, then about 7.6 s (city plus crane as one continuous move), then 2.4 s for the card. Average shot length is 4–5 s, which is slow for Reels. It works only because *something is always moving* (walk, drift, crane, type-on, flare) and every shot change is disguised. There are no straight hard cuts on clear footage: each change of image is hidden in white (T1, T2) or by camera motion (shot 2 → 3).

**Audio (music bed only, no SFX):**

| Time | RMS dBFS | Role |
|---|---|---|
| 0–8.5 | −12 to −19, fluctuating | groove at **≈117 BPM** (beat period 0.51 s, spectral-flux autocorrelation) |
| 9.0–10.0 | **−9 to −11** | first swell, exactly as the crane starts rising; the spectral centroid also rises (music gets brighter) |
| 10.5–11.5 | −17 to −19 | **the breath**: a dip just before the reveal |
| 12.5–13.0 | **−8 (peak)** | logo-in-sky, flare and cut to card |
| 13.5–17 | −11 → −31 | long decay under the card and outro |

Energy onsets at 1.95, 3.1, 4.35, 6.0, 8.9, 9.7, 12.45, 13.05, **13.2** and 13.45 s. The card cut (13.2 s) sits exactly on an onset, and the light leak (4.35 s onset → 4.6 s leak start) arrives just after a beat. **The edit was cut to the music.**

### 1.2 How each transition and technique is built

1. **White open (light-leak in).** The footage sits under a cream layer (≈ #F2EBDD, not pure white) with a soft, slightly yellow edge glow. The overlay's opacity eases from about 85 % to 0 over 1.9 s, so the subject is visible immediately as a silhouette. This is a "fog lift", not a fade from white. Bloom is strong at first and settles to the base grade.
2. **Orange light leak (T1).** This is real light-leak *stock behaviour*: organic, warm-yellow-to-orange blobs that move laterally (left → right), composited with *screen/add*. Two layers: a saturated orange-yellow blob with a hot core, and a broad cream wash that drives the frame to near-white for about 6–8 frames. The cut happens at peak luminance, so the eye never sees it. A large soft circular bokeh orb (bottom-left at 4.75 s) sells "lens", not "filter".
3. **Crane move as transition (shot 2 → 3).** No editorial transition at all. The AI shot itself contains a tilt-up/rise: city → horizon → cloud layer → open sky. The cloud layer passes *in front of* the skyline (volumetric occlusion), which clears the frame for the logo. Speed curve: slow start, fastest at about 9–10 s (on the music swell), easing out by 11.5 s so the sky is calm when the logo lands.
4. **Logo in the sky.** A clean flat brand mark (no 3D, no rotation) is placed screen-locked in the upper-middle of the frame while the clouds keep drifting behind it. It reads as "the brand appears in its world". Light interaction: the sun flare and bloom from 12.8 s wash *over* the logo (the logo sits under the flare layer), which glues it into the scene. Note: **the mark is flat and opaque; integration comes from layer order (logo under flare/bloom), placement on calm sky, and motion contrast (static logo, moving clouds).** No fake 3D, no glow halo, no spinning.
5. **White flash cut to card (T2) plus position continuity.** The flare peaks, there is a white frame, then the card. On the card the icon stays at the same vertical position as in the sky and slides left to make room for the wordmark. That is a *match cut on the logo*.
6. **Type-on wordmark.** The wordmark (lowercase-feeling geometric sans) reveals glyph by glyph (≈0.2 s per glyph, no cursor, no fade per glyph). Then a *very small* descriptor in light grey, roughly 1/6 of the wordmark cap height, fades in. Lots of negative space; the brand block is centred at about 44 % of height (inside the Reels safe zone).
7. **Outro flare.** An anamorphic-style flare with chromatic bokeh orbs (pink, peach, teal) sweeps the card, then a quick dip to black. The last 1 s of black is wasted on Reels: it hurts the loop and is a frame where people swipe.

### 1.3 Colour grade and look (measured)

- **High-key and lifted.** Average luma ≈ 142–165 on footage (bright, airy). Blacks are never crushed until the outro; shadows are lifted, a faded film look.
- **Restrained saturation.** 0.45 on the warm path shot, **0.28 on the city**, **0.20 in the clouds**. Saturation *decreases* through the film toward the brand moment, and the card is 0.05. Colour calms down so the logo's red is the most saturated thing on screen.
- **Warm and teal split by scene, unified by a cream highlight.** Shot 1 is warm (R−B ≈ +35). The city and clouds are neutral to cool (R≈G≈B, slight teal in the sky). Every highlight rolls off to the same cream, and the card colour (#E6E0DA-ish) equals the highlight colour, so footage and card feel like one world.
- **Bloom and halation** on all highlights (sun, white buildings, cloud edges), plus a soft flare orb. These give a dreamy "shot through glass" softness. Fine detail is deliberately soft (top-third Laplacian only 2–11).
- **Depth of field = miniature cue.** Strong tilt-shift band: sharp foreground or middle, very soft top and bottom. The city shot is the textbook case (top 5 / middle 24 / bottom 39).

### 1.4 Recreation recipes (AI clips plus ffmpeg/Python)

General pipeline: Kling 3.0 Pro I2V clips (1076×1924, 24 fps), then a Python/numpy frame compositor (as in `edit.py`), then libx264. **Work on a 24 fps timeline end to end** (see the judder finding in §2). Grade *before* compositing the logo and text, and add flare/bloom *after* the logo so the logo sits under it.

**R1 — White "fog-lift" open**
- Prompt the first clip so the subject is already in frame and moving at frame 0 (no "camera reveals…").
- Composite: `out = lerp(frame, CREAM, k(t))`, with `CREAM = (246,241,228)` (brand cream #F6F1E4, already a brand colour), `k = 0.85·(1−easeOutCubic(t/1.6))`. Add a soft bloom whose strength follows `k`.
- Never start from 100 % white: frame 0 must show the subject at ≥15 % visibility. The hook needs pixels.

**R2 — Organic light leak with a hidden cut**
- Best option: free/licensed 4K light-leak stock (on-black, MOV/MP4), scaled to 1080×1920, blended with `screen`:
  `ffmpeg -i a.mp4 -i leak.mp4 -filter_complex "[1]scale=1080:1920,format=gbrp[l];[0]format=gbrp[b];[b][l]blend=all_mode=screen" ...`
- Procedural option (no stock): 2–3 Gaussian blobs (radius 0.6–1.0×W) on noise-perturbed paths moving left → right. Colours #FFB347 / #FFD27A / cream. Add-blend with `sin(π·p)` intensity, plus a global lift to luma ≈230 at the peak. Cut A → B at the peak frame (±1 frame). Add one large soft circular bokeh disc (alpha 0.5, blurred edge) to sell "lens".
- Duration 0.8–1.0 s (20–24 frames at 24 fps). Start it on a beat and put the cut on the next downbeat.

**R3 — Crane-up transition inside one AI clip**
- Do it in the generation, not in the edit: one I2V clip whose start frame is the miniature city with a big cloud bank above. Prompt: "camera cranes up and tilts up smoothly, city sinks below frame, rising through a layer of soft golden clouds into open sky, slow ease-in, ease-out".
- If one 5 s clip is not enough: generate clip B starting from the **last frame** of clip A (I2V chain), then cross-dissolve 6–8 frames only where the frame is mostly cloud (uniform texture hides ghosting).
- Speed ramp in post: resample time with an ease-in-out curve so the fastest motion lands on the music swell. Use `minterpolate` only for ≤1.3× speed-ups; otherwise use the raw frames.

**R4 — Logo in the sky**
- AI generates an *empty calm sky zone* (prompt "large area of clear sky in upper centre, no objects"). We composite the exact SVG/PNG logo.
- Placement: centre at x=540, y≈800 (inside the safe zone), width ≈ 380–420 px. **Screen-locked, no rotation.** Entry: scale 0.92 → 1.0 plus opacity 0 → 1 over 6 frames (easeOutBack, 5 % overshoot max), on a beat.
- Integration: (1) grade the logo a touch toward the scene (multiply by the highlight tint at 8–10 %); (2) add a soft *sky-coloured* drop haze, not a glow halo; (3) composite the sun flare and bloom **after** the logo, so light washes over it. Optional: matte a wisp of cloud *in front of* the logo's lower edge (luma key of the bright cloud from the plate) for true "inside the world".

**R5 — Flash match-cut to card plus type-on**
- Flash: 3–4 frames of a cream (#FFFDF7) peak on the music hit. The logo keeps the same y on the card, then slides left (easeInOut, 0.35 s) to open space for the wordmark.
- Type-on: reveal per glyph from a pre-rendered text layer (render the full line once, centred, then reveal with a left-to-right clip mask in glyph steps). Never draw the partial string re-centred or left-shifted. 0.06–0.09 s per glyph for "Kiwi Go"; pairs for Russian lines. Descriptor fades in (opacity plus 12 px rise) 0.2 s after.
- Render text with Pillow at 2× scale and downsample (or Playwright/HTML with Onest) for clean anti-aliasing.

**R6 — Grade, bloom and miniature DOF (apply to every clip)**
- Base grade (ffmpeg): `eq=saturation=0.85:gamma=1.05,curves=master='0/0.06 0.5/0.55 1/0.96'` (lift blacks, soft roll-off), `colorbalance=rs=.04:bs=-.03:rh=.03:bh=-.02` (warm), `vignette=PI/5`.
- Unify: a global "cream highlight" pass that pulls values above 0.8 toward #F6F1E4 with a soft-light blend at 20 %.
- Bloom: threshold luma >0.75 → Gaussian σ≈40 px at 1/4 res → screen at 15–25 %.
- Tilt-shift reinforcement (if the AI plate is too sharp): vertical gradient mask, 0 in the sharp band (subject height ±12 %) and 1 at the top and bottom, blending to a Gaussian-blurred copy (σ 6–10 px). Add +10 % saturation on the sharp band only, the classic miniature look.
- Grain: 2–3 % luma noise at 24 fps, so AI plastic-smoothness and banding disappear.

**R7 — Outro flare without dead air**
- Flare sweep 0.5 s, then go **straight back to frame 1's look** (cream fog) for a loop, rather than 1 s of black (see the loop rules in §3).

---

## 2. Critique of our previous brand film (`kiwi-go-brand-film.mp4`)

Measured timeline: white open 0–0.5 s → **shot 1** kiwi tyre rolling down a mountain path 0.5–4.1 s → light leak 4.0–5.0 s → **shot 2** tilt-shift avenue with one van 5.0–8.6 s → cross-dissolve 8.6–9.1 s → **shot 3** sunset sky over the city 9.1–13.0 s (logo rises and spins in 11.4–13.0 s) → flash 13.0–13.6 s → **end card** 13.6–16.3 s ("Kiwi Go / Доставка по всему Кыргызстану") → dip to grey/black 16.3–17 s. Silent.

| # | Problem (what we see / measured) | Why it reads as low-quality or "not marketed" | Fix |
|---|---|---|---|
| 1 | **Hook.** Frame 0 is about 95 % white (luma 245); the tyre only becomes readable at about 0.4 s, and then it is a static-feeling scene. | The scroll decision happens in the first 0.5–1.7 s. We showed a blank, then scenery. Nothing poses a question ("what is that?", "that's me!"). | Open on motion *in frame 0*, with a recognisable sender problem or a striking miniature image (e.g. a parcel that is clearly *ours* leaving a door at dusk). Fog-lift at most 85 % opacity. Put a 3–5 word Russian hook on screen by 0.3 s (e.g. «Отправить посылку — как написать сообщение»). |
| 2 | **No story.** Tyre on a mountain → a city → a sunset → a logo. Three unrelated postcards. | No protagonist, no journey A → B, no transformation. Viewers can't say what the company does after watching. | Use one through-line: **parcel from a sender's door (evening) → on the road through Kyrgyz mountains overnight → arrives at a recipient's door, phone shows SMS code**. The reference's power is *one character, one journey*. |
| 3 | **No benefit, no information.** The only copy is "Kiwi Go / Доставка по всему Кыргызстану" at 14 s. | Generic. No price, no "door to door", no "next day" idea (without exact times), no "for shops / COD", no tracking. That is the "no marketing" complaint. | 2–3 benefit beats as short Russian supers, one per shot: «Курьер заберёт от двери» → «Посылку видно на каждом шаге» → «от 350 сом за место». Honest, no exact times, no city names. |
| 4 | **No CTA.** The film ends on the tagline and then goes to black. | A Reel without a next step wastes paid reach. | The end card carries a CTA: «Оформить: kiwigo.kg» or «Скачайте Kiwi Go для магазинов», plus «от 350 сом». Hold it ≥1.5 s. Mirror the CTA in the caption and the ad button. |
| 5 | **The kiwi-tyre shot.** A lone tyre with a flat kiwi slice face rolls down a dirt path with dust. | It reads as "a wheel fell off a truck" (a failure image for a delivery brand). The kiwi face is flat and pasted-looking; the black tread surrounds it like a toy. It doesn't match the site's charming "truck with kiwi wheels" idea, and AI is drawing a brand element. | Drop the lone tyre. Either show an **unbranded miniature delivery van/truck** (wheels can carry a subtle kiwi-green hub, *composited* by us) driving the mountain road, or don't show the wheel motif at all and keep the kiwi = wheel idea for the logo moment. |
| 6 | **Pacing / motion.** Mean motion: shot 1 = 5.7, shot 2 = **2.2**, shot 3 = **1.7** (reference crane: 5–7). Shots 2–3 are nearly locked-off postcards for about 8 s. | Energy *falls* across the film; the reference's energy *rises* toward the logo. Long static shots with no new information = swipe. | Every shot needs motivated camera motion (push, follow, crane). Something new every 1.5–2.5 s: a new super, a new action, a camera beat. Build to a crescendo at the logo. |
| 7 | **Frame judder.** AI clips are 24 fps; `edit.py` resamples them to 30 fps by nearest frame, so 20 % or more of frames are duplicates. Measured 43 % duplicate frames in shot 1, 20 % in shot 2, 15 % in shot 3. | Visible stutter on pans and the rolling tyre. It reads "cheap / AI" instantly. | Build the timeline at **24 fps** and export 24 fps (Instagram accepts it), or interpolate properly. Never index frames by `round(t·30)` into a 24 fps source. Check that source clips have no frozen frames before editing. |
| 8 | **Transitions.** T1 is a procedural radial blob and a white wash, fine but synthetic. **T2 (8.6–9.1 s) is a plain cross-dissolve between two unrelated images**, and the strip shows buildings ghosted over the sunset clouds. | A ghosting dissolve between unrelated shots is the most "amateur" transition. The reference never dissolves; it hides cuts in light or in camera motion. | Replace T2 with a motivated move (crane up from the street into sky, generated as one clip, R3), or a whip/occlusion (a truck passes the lens). Light-leak only once or twice, and on the beat. |
| 9 | **Grade inconsistency.** Shot 1 is warm golden hour (R−B ≈ +75), shot 2 is morning (R−B ≈ +55), shot 3 is a pink sunset (R−B ≈ +40), each with its own sun direction. Saturation 0.47–0.53 (reference 0.20–0.45). The image is sharp edge to edge (top-third sharpness ≈ 18 vs 5–11 in the reference). | Three lighting setups means three different worlds. It is over-saturated and too crisp, so it looks like stock and AI rather than "crafted miniature". | One time of day for the whole Reel (or a deliberate evening → morning arc that matches the story: pickup in the evening, delivery the next morning). Apply R6: lower saturation, lifted blacks, cream highlights, bloom, grain, and a stronger tilt-shift falloff. |
| 10 | **Logo-in-sky compositing.** The logo fades in and **spins 270°** while rising from y≈1040 to 840 and growing 200 → 420 px over a static sunset. It is fully opaque and crisp with a yellowish glow halo; no light passes over it; it then jumps to a different position and size on the card (y 640, 380 px) through a white flash. | The spin + rise + grow + halo stack makes it a "PowerPoint sticker". No layer interacts with it. There is no match cut, so the brand moment has no continuity. | R4: screen-locked, no spin (or one *small* roll matching a wheel motif, ≤1 rotation, on a beat), placed on a calm sky zone, with flare and bloom **over** it and optional cloud wisps in front. Keep the same x/y into the card (match cut), then slide. |
| 11 | **End-card typography.** Inter Black 150 px wordmark and a 64 px Bold two-line tagline, all in the upper half; the bottom 50 % is empty. The partial type-on string is drawn left-anchored, so "Kiw" sits off to the left while typing, which looks unbalanced. Off-white page with no brand colour; it fades to a muddy grey before black. The site uses Onest, not Inter. | Weak hierarchy (logo, name and tagline all similar weight), off-brand font, the signature lime unused, nothing to read *after* the name, and the grey fade looks like a rendering error. | Onest (matches the site). Hierarchy: logo → «Kiwi Go» (Onest Bold, about 120 px) → one benefit line → **CTA pill in lime #B8F03C with ink #111410 text** («kiwigo.kg» / «от 350 сом»). Everything inside y 270–1250. Reveal with a mask on a pre-rendered centred line. End on ink or loop back, never grey. |
| 12 | **Sound plan.** The film is silent and the cuts weren't designed to a tempo grid. | Music added later won't land on cuts, and the film will feel off-beat. | Design to a tempo grid (e.g. 115–120 BPM, about 0.5 s per beat, like the reference). Document beat points (hook hit, transitions, logo hit, CTA) so the client's music can be fitted. |
| 13 | **Loop / tail.** About 0.7 s fade to grey/black plus black at the end. | Dead frames at the end cause swipes and kill the replay value. | End on the CTA card, then a 6–10 frame cream fog that matches frame 0, for a seamless loop. |
| 14 | **AI drawing brand-adjacent elements** (the kiwi tyre face). | Off-brand, uncontrollable, and it undercuts the exact logo. | AI footage contains *zero* brand marks. All kiwi/lime branding is composited by us (CONTEXT rule). |

**What was right and should be kept:** 9:16 at 1080×1920; logo-free AI plates with the exact logo composited; the miniature/tilt-shift avenue shot (shot 2) is the strongest image and is on-trend; the light-leak and type-on vocabulary matches the reference; and the end-card hold length (about 2.7 s) is about right.

---

## 3. Research: what makes high-performing brand and delivery Reels (2025–2026)

Caveat: most public sources are agency and vendor blogs, and the numbers are self-reported. Meta-attributed figures below come via trade press summaries of Meta research, not Meta's primary docs. Treat them as direction, not law.

**3.1 The first second / hook**
- Consensus: the hook lives in the first 3 s, and stricter guidance says 0.5–1.7 s for Reels ads. The first seconds should *feel native/organic*, not like a TV ad opener. ([twominutereports](https://twominutereports.com/blog/instagram-ads-best-practices), [smartsites](https://www.smartsites.com/blog/best-practices-for-high-performing-instagram-reels-ads-in-2026/), [exchange4media](https://www.exchange4media.com/digital-news/why-the-first-few-seconds-of-an-instagram-reel-can-make-or-break-an-influencer-ad-145586.html), [inbeat](https://inbeat.agency/blog/instagram-reels-ads))
- Meta research (via trade press): **brand and message in the first 5 s → 1.7× more likely to reach the top purchase-intent tier**; repeated brand presence across scenes → 1.8×. ([Search Engine Land](https://searchengineland.com/meta-native-reels-ads-can-lift-purchase-intent-5-3x-465615), [bestmediainfo](https://bestmediainfo.com/insights/want-reels-ads-that-actually-work-meta-just-revealed-the-playbook-10866888))
- But **opening on a big logo or heavy text overlay** reportedly lowers median CTR by about 15 %. So brand *cues* (lime colour, kiwi-wheel motif, product) should be there early, with the full logo lock-up later. ([gethookd](https://www.gethookd.ai/learn/facebook-reels-ads-specs-examples-best-practices/))
- For us: motion and the subject in frame 0; a hook line by about 0.3 s; a lime brand cue (composited) by 2–3 s; the logo moment by about 10–13 s, with a smaller brand presence earlier.

**3.2 Optimal length**
- Ads: 15–30 s performs best per most guides; test 15 vs 30 s. Reels can now run to 3 minutes, but that is irrelevant for a brand spot. Change the visual every 2–4 s. ([Demand Curve](https://www.demandcurve.com/blog/instagram-video-length), [quso.ai](https://quso.ai/blog/instagram-reels-best-practices), [topgrowthmarketing](https://topgrowthmarketing.com/?p=31997))
- For us: **18–22 s master** plus a **9–12 s cut-down** (hook, one benefit, CTA) for paid placements.

**3.3 On-screen text**
- Text should *carry the message for silent viewers* and follow the narrative; keep it short; burn captions in (Instagram auto-captions are unreliable). ([gethookd](https://www.gethookd.ai/learn/facebook-reels-ads-specs-examples-best-practices/), [quso.ai](https://quso.ai/blog/instagram-reels-best-practices.html), [webtonic](https://www.webtonic.io/blog/instagram-reels-ads-7-step-guide-to-creating-high-converting-campaigns))
- Message via sound *and* on-screen text/visuals → 1.8× more likely top-20 % brand interest (Meta via press). ([bestmediainfo](https://bestmediainfo.com/insights/want-reels-ads-that-actually-work-meta-just-revealed-the-playbook-10866888))
- Working rules for us: ≤6 words per super; one idea per super; on screen for at least 0.4 s per word (minimum 1.2 s); Onest Bold/SemiBold; ≥64 px at 1080 width for supers; high contrast (ink on cream/lime, or white with a soft shadow on footage).

**3.4 Sound-off viewing**
- A large share watch muted (estimates of 20–30 % on Reels, higher in feeds); design so the story works muted, and *also* use sound, because Reels is a sound-on surface. ([gethookd](https://www.gethookd.ai/learn/facebook-reels-ads-specs-examples-best-practices/), [hallam](https://hallam.agency/blog/insights-from-metas-reels-playbook-for-maximising-reach-and-engagement/), [metricool](https://metricool.com/facebook-reels-ads-guide/))
- For us: the export has no music by design. The Reel must make complete sense muted (supers carry the benefits). The client's music then adds emotion on beat points we document.

**3.5 Loopability**
- Ranking weighs watch time (percent and absolute seconds), likes and shares. Seamless loops encourage replays (average watch time > length = replays), strongest on short videos. No official replay weighting is published, so treat it as "likely helps". ([fanpagekarma](https://www.fanpagekarma.com/insights/instagram-reels-algorithm/), [later glossary](https://later.com/social-media-glossary/loop/), [thesocialcat](https://thesocialcat.com/glossary/video-loop-short-form-content), [getkoro](https://getkoro.app/blog/how-to-loop-a-video-on-instagram))
- For us: no black tail. The last frame (CTA card with a cream fog) flows into frame 0 (cream fog-lift), and the music bed can be cut to loop on a bar.

**3.6 9:16 safe zones**
- Meta's guidance is usually quoted as percentages: keep clear the **top ≈14 % (≈270 px)**, **bottom ≈35 % (≈670 px)** and **≈6 % per side (≈65 px)**, with extra room on the right for the like/comment/share column. Blogs disagree on pixels (top 150–270, bottom 250–670); check against the Ads Manager safe-zone overlay. The feed may crop to 4:5. ([hopperhq](https://www.hopperhq.com/blog/instagram-reel-size/), [contentstudio](https://contentstudio.io/blog/instagram-reel-size), [maketecheasier](https://maketecheasier.com/instagram-story-reel-safe-zone), [poster.ly checker](https://poster.ly/tools/meta-ads-safe-zone-visualizer), [houseofmarketers](https://www.houseofmarketers.com/guide-to-safe-zones-tiktok-facebook-instagram-stories))
- For us (1080×1920): **all text and logos inside x 80–900 (allowing for the right action column), y 270–1250**. The critical message band is y 600–1150, which also survives a 4:5 crop (y 285–1635). Hero subjects should sit in the upper-middle too.

**3.7 The miniature / tilt-shift trend**
- AI "miniature world" / tilt-shift diorama videos are a recognised viral visual trend (prompt tokens: *tilt-shift, diorama, macro lens, extreme shallow DOF, toy-scale motion*). Brand use: *make the product the biggest/hero thing in a tiny world*. Higgsfield itself promotes it. ([crepal](https://crepal.ai/blog/?p=8123), [novoads](https://novoads.ai/blog/how-to-create-miniature-world-videos-with-ai), [higgsfield blog](https://higgsfield.ai/blog/Hot-Trend-in-Digital-Marketing), [carat prompt gallery](https://carat.im/en/prompt-gallery/tilt-shift), [contentbeta examples](https://www.contentbeta.com/blog/best-ai-video-ad-examples/))
- There is little hard performance data for brands. It fits Kiwi Go well: "all of Kyrgyzstan as a miniature you can send parcels across" is a natural metaphor for covering about 80 destinations, and toy-scale reads as friendly.

**3.8 AI-video brand ads that worked (and lessons)**
- Self-reported wins: Boost Oxygen (+20 % branded search) and Party Propz (+35 % CTR) on Amazon Ads with AI video ([Amazon Ads](https://advertising.amazon.com/en-gb/library/case-studies/boost-oxygen), [Amazon Ads](https://advertising.amazon.com/en-gb/library/case-studies/party-propz)); DEPT × Pit Viper "Impossible Ad" on Google, +3.8 % ad recall ([Think with Google](https://thinkwithgoogle.com/marketing-strategies/automation/dept-ai-video-ad-campaign)); Kalshi's roughly $2k AI spot with about 20 M impressions ([pulse.bot](https://www.pulse.bot/advertising/video/this-2000-ai-ad-got-20-million-impressions-b1d79490-d83c-43ed-8182-56b2c6fcafc6/)); Starburst's modular AI worlds and Nike roundups ([pixis](https://pixis.ai/blog/10-breakthrough-ai-marketing-campaigns-we-loved-in-2025/), [kapwing](https://www.kapwing.com/resources/11-brands-making-video-ads-with-ai-its-not-just-coca-cola/), [creatify](https://creatify.ai/blog/ai-marketing-campaign-examples)).
- Backlash cases: Coca-Cola's AI holiday ads and Valentino's morphing ads ([creatify](https://creatify.ai/blog/ai-marketing-campaign-examples), [Make it Pop](https://makeitpop.beehiiv.com/p/make-it-pop-09-the-2026-ai-video-playbook-for-brands-how-to-avoid-the-ai-slop-trap)).
- **Lessons:** wins came from a clear idea, brand guardrails and a stylised world (where AI artefacts read as style). Backlash came from uncanny realism, morphing and "AI slop" faces. → Stay stylised (miniature), avoid close-up human faces and hands, never let AI draw the logo or text, and use few shots with long, controlled camera moves.

**3.9 Delivery / logistics specifically**
- What works: showing the *delivery journey* (order → pickup → route → doorstep), quick FAQ answers (price, pickup, tracking), a light and human tone, and a strong hook + storytelling to compete with bigger carriers. Also make sure the profile bio carries the info. ([searates](https://www.searates.com/fr/blog/post/instagram-marketing-strategies-for-small-shipping-companies-competing-with-big-carriers), [tryotter](https://tryotter.com/blog/toolkit/27-instagram-reels-ideas-for-restaurants-in-2022-with-examples), [pickupp](https://hk.pickupp.io/en/blog/igreels), [insidea](https://insidea.com/blog/instagram/captions/shipping-companies))
- For Kiwi Go: the "door → road → door" journey in a miniature Kyrgyzstan is both the trend and the category's proven story. Our target sellers care about *price per parcel, no % fee, COD paid out, tracking*. Pick 2–3 of these, not all.

---

## 4. Professional pre-publish checklist (the final Reel must pass every line)

### A. Hook and story
- [ ] Frame 0 shows a readable subject in motion (no blank/white/black first frame; fog overlay ≤85 % and gone by 1.5 s).
- [ ] A hook super (≤6 words, Russian) is on screen by 0.3–0.5 s and inside the safe zone.
- [ ] A brand cue (lime, kiwi-wheel motif, or the composited logo) appears within the first 3–5 s, with no big logo slate as the opener.
- [ ] One protagonist and one A → B journey (sender door → road → recipient door); a stranger can say what Kiwi Go does after one muted view.
- [ ] Energy rises toward the logo/CTA (camera speed and music swell), not flat or falling.

### B. Marketing content (public facts only)
- [ ] 2–3 benefit supers, e.g. «Курьер заберёт от двери», «Посылку видно на каждом шаге», «от 350 сом за место». Each is in CONTEXT's public-facts list.
- [ ] A clear CTA on the end card (site/app) held ≥1.5 s, and repeated in the caption and the ad button.
- [ ] No forbidden items: no exact delivery times, no city names as text, no «Скоро запуск», no competitor names, no internal numbers.
- [ ] Russian copy proofread by a native speaker (spelling, «ё», non-breaking spaces before «сом», correct quotes «»).

### C. Craft — picture
- [ ] One consistent grade across all shots (one time of day or a deliberate story arc); saturation controlled; cream highlights; bloom; light grain.
- [ ] Miniature DOF is consistent (tilt-shift band on every shot).
- [ ] No AI artefacts: morphing, melting wheels or vehicles, extra limbs, flicker, warped horizons, gibberish signage or letters, AI-drawn logos. Checked frame by frame at 100 %.
- [ ] Vans and trucks unbranded or with clean panels; any branding is our composite and tracks correctly (no sliding).
- [ ] Every camera move is motivated and eased. No locked-off postcard longer than about 2.5 s without new information.
- [ ] Transitions hidden in light, motion or occlusion. **No plain cross-dissolve between unrelated shots.**
- [ ] Timeline and export at 24 fps (or proper interpolation); duplicate-frame ratio <2 % (check with the frame-diff script).
- [ ] Logo-in-sky: exact logo file, no spin stack, sits under the flare/bloom layer, on a calm sky area; match-cut position into the end card.

### D. Craft — type and layout
- [ ] Font: Onest (site font) throughout; at most 2 weights; supers ≥64 px; CTA ≥56 px; descriptor ≥40 px at 1080 width.
- [ ] All text and logos inside x 80–900, y 270–1250; the key message within y 600–1150 (survives a 4:5 crop). Verified against Meta's safe-zone overlay.
- [ ] Contrast ≥4.5:1 (ink on cream/lime; white on footage only with a soft shadow or scrim).
- [ ] Each super is on screen long enough to read twice (≈0.4 s/word, minimum 1.2 s); one idea at a time.
- [ ] Type-on reveals a pre-rendered centred line (no jumping or re-centring); kerning checked; no orphans or widows in two-line supers.
- [ ] Brand colours exact: lime #B8F03C, ink #111410, paper #FFFDF7, cream #F6F1E4; logo unaltered.

### E. Sound readiness (export has no music)
- [ ] Edit built on a tempo grid (≈115–120 BPM); a beat sheet is delivered listing the hook hit, each transition, the logo hit and the CTA (timecodes).
- [ ] Works completely muted (all info in supers).
- [ ] Suggested music shape documented: groove → swell into the reveal → short breath → peak on the logo → resolve under the CTA (as in the reference).

### F. Platform and delivery
- [ ] 1080×1920, 9:16, H.264 High, yuv420p, 24 fps, about 10–16 Mbps, `+faststart`, Rec.709, no letterboxing.
- [ ] Length: master 18–22 s; cut-down 9–12 s; both checked.
- [ ] Loop: no black tail; the last frame flows into frame 0.
- [ ] Cover frame chosen (logo + benefit, inside the 4:5 centre crop for the grid).
- [ ] Previewed on a real phone inside the Instagram UI (draft or Ads preview), muted and unmuted, in bright light.
- [ ] Caption: hook line + benefit + CTA + link-in-bio/site; 3–5 relevant hashtags; alt text written.
- [ ] Final sanity: a person who has never heard of Kiwi Go watches it once, muted, and answers: *what is it, how much, how do I start?*

---

### Summary
- The reference has 3 shots plus a card in 17 s (5.0 / 7.6 / 2.4 s). Every image change is hidden in light (cuts at 5.57 s and 13.20 s inside white) or inside a continuous crane move.
- Its music is about 117 BPM, swells at 9 s with the crane, dips at 10.5–11.5 s, peaks at 12.5–13 s on the logo, and the card cut lands on an onset.
- Grade: high-key, lifted blacks, saturation falling 0.45 → 0.20 toward the brand moment, cream highlights equal to the card colour, bloom, and a strong tilt-shift DOF band.
- Logo in the sky: a flat, screen-locked mark on a calm sky, under the flare, then a match cut into a type-on card. Seven recreation recipes (R1–R7) are given.
- Old film: white first frame (no hook), three unrelated postcards (no story), falling motion energy, three different lighting setups, over-saturated and too sharp, a ghosting dissolve, and a spinning sticker logo with no match cut.
- It also has off-brand Inter type with weak hierarchy, a muddy grey fade, no benefits, no price and no CTA.
- New technical bug: 24 → 30 fps nearest-frame resampling in `edit.py` causes stutter (20–43 % duplicate frames). Use a 24 fps pipeline.
- Research takeaways: hook within 0.5–3 s with brand cues by 5 s but no logo slate; 15–30 s; burnt-in supers that work muted; seamless loop; text inside y 270–1250 and x 80–900.
- The miniature trend fits Kiwi Go. AI ads win when stylised and guarded, and fail when uncanny.
- A 33-point pre-publish checklist (sections A–F) covers hook, story, marketing, picture, type, sound readiness and delivery.
