# 07 — Production plan: the hybrid «Отправлено» on C1's spine

Role: producer and prompt engineer. Written 2026-11-18. This file is the **single source of truth for production**. Where it conflicts with 01–06, this file wins. It applies every fix from `05-marketing-review.md` and `06-copy-brand-review.md`, plus the client decisions received during planning (§0.1).

Nothing was generated. The only Higgsfield calls made were `balance`, `models_explore` (get) and `estimate_image_cost` / `estimate_video_cost`. **Every credit figure below is a live quote from this account, taken 2026-11-18** (§3b).

---

## 0. Binding inputs

### 0.1 Client decisions (received 2026-11-18; they override the reviewers on these points)

| Variable | Decision | Where it goes |
|---|---|---|
| COVERAGE | **«По всему Кыргызстану»** (on screen as «По всему / Кыргызстану»). The client chose it knowingly after the 05/06 warnings. **Get this in writing and keep it on file** (Q-1). | S3 super and caption |
| PRICE | **«от 350 сом»** (with no-break spaces: `от 350 сом`) | End card and caption |
| CTA | **Anyone can order today, private senders included.** End-card CTA: **«Оформите доставку»**, with the pill **«kiwigo.kg»** and the line **«или напишите в WhatsApp»** | End card, caption and ad button |
| Language | **Russian only.** No Kyrgyz track for now. | — |

Because of these decisions, no copy placeholders remain. The only open data items are the WhatsApp number (if it is to be shown) and the real app labels (§6).

### 0.2 Fix checklist (05 and 06). Every item is applied, and the table shows where.

| Fix | Applied as | Where |
|---|---|---|
| Arrival in a **city**, not a village | S4 is a Soviet-era city courtyard (4–5-storey block, balconies, poplars, blue entrance door). No village, gate, yurt or valley at the door. | S4 |
| Tracking on the **seller's side only** | The status chips live only in the seller's mini-phone PiP, headed «Kiwi Go для магазинов». The recipient never holds a phone and never sees a chip. | S3, S4 |
| «**код получения**», not SMS | Super «Вручаем / по коду получения». The caption says the code arrives by SMS and goes **only to the courier at handover**. | S4, caption |
| **No tunduk or yurt symbolism** | No yurt, tunduk, лепёшка, kalpak or state-like round emblem anywhere. The style bible bans them (§2.6). | all |
| No «вес не важен» as an absolute claim | The card note is «за посылку» only. The site's clause «вес и размер цену не меняют» appears only in the caption, after the client confirms the size limit (Q-7). | Card, caption |
| **Real status labels only**, or none | The chips are the site's published labels: «Забрали», «В пути», «В городе», «У курьера». **«Вручено» is not a published label, so there is no final chip.** The PiP slides out after «У курьера» unless the client supplies the real final label from the app (Q-3). | S3, S4 |
| Logo **born on the kiwi wheel** of a parked, side-on truck, **by compositing** | In S6 a light sweep crosses the parked truck. In its wake our SVG replaces the plain wheels, plane-locked, and it hits on B8.1 (14.00 s). The R5 flash then match-cuts it into the card icon. AI never draws a kiwi. | S6, T2 |
| No duplicate pill in the hook; single ✓, not ✓✓; neutral bubbles | Bubbles only on frame 0, one ✓, our own bubble shape, no messenger colours | S1, S5 |
| Supers' line breaks and no hanging prepositions | The breaks are in §1.3 and were measured in Onest | all |
| «Заберём» with ё; no-break spaces in «Kiwi Go», «350 сом» | Typesetting rules in §5.4 | all |
| CTA held ≥ 3 s in the master | The CTA is held 16.50–19.60 s = **3.1 s** (cut-down: 2.1 s) | Card |
| Onest, bundled locally | Onest 600 and 700 TTFs live in the repository; no web font fallback | §5.4 |

Not carried over:
- «Посылки по всему Кыргызстану» as the card descriptor. Per 05, the card descriptor is the proposition, and coverage sits in S3.
- The 06 card note «за посылку · вес не важен», which breaks the "no absolute weight claim" rule.
- `app.kiwigo.kg`, which the client replaced with `kiwigo.kg`.

---

## 1. Final script

### 1.1 Grid and frame maths
- **24 fps** end to end. **120 BPM**, so 1 beat = 0.5 s = **12 frames** and 1 bar = 2.0 s = 48 frames. Bar *n* starts at 2(n−1) s. "B8.1" = bar 8, beat 1 = 14.00 s = f336.
- The master is **20.00 s = 480 frames (f0–f479) = 10 bars**. The cut-down is **10.00 s = 240 frames = 5 bars**.
- Positions are in the 1080×1920 frame. Centre line x = 490. Text-safe area: x 80–900, y 270–1250. The 4:5 crop survives y 285–1635.

### 1.2 Master, 20.0 s: shot table

| # | TC in–out (s) · frames | Bars | Picture (what we see) | Transition IN / OUT | Supers / UI (RU, final) | Composited elements | Beat |
|---|---|---|---|---|---|---|---|
| **S1** | 0.00–2.50 · f0–f59 | B1.1–B2.2 | **HOOK.** Night. A felt-toy miniature living room: the **seller** sits small on a sofa among stacks of blank cream parcels. Her phone's cold light is on her face, and warm city bokeh shows through the window. A slow push-in is already moving on f0. She lowers the phone a little and exhales. | IN: **R1** fog **20 % at f0 → 0 by 0.50 s (f12)**, which matches the loop tail. OUT: **R2** leak, 2.25–2.75, cut at its peak on f60. | Incoming bubbles, left: «где моя посылка?» **0.00**; «уже отправили?» **0.50**; «??» **1.00**. Outgoing **lime** bubble, right, with the 40 px kiwi icon: «Отправлено ✓» **1.50** | 4 bubbles (§1.3) | Pops on B1.1, B1.2, B1.3. **Send on B1.4 (1.50)** |
| T1 | 2.25–2.75 · f54–f66 | B2.1–B2.2 | R2 warm orange leak with a lime fringe. The "send" visibly flies out as light. | Cut S1→S2 at the peak, **f60** | — | Leak (§5.2) | **HIT B2.2 (2.50)** |
| **S2** | 2.50–4.50 · f60–f107 | B2.2–B3.2 | **Pickup.** Warm evening at the seller's apartment door, a felt stairwell landing with a lamp and a cream door. On f0 the **courier** (lime cap, ink jacket, back three-quarters) **already holds the parcel** with the blank round sticker. The seller, in the doorway with her hands at her waist, smiles. The courier turns right and walks out. The camera is locked off. | IN: leak. OUT: **composited whip-pan right**, a 6-frame directional-blur bridge, f102–f113, with the cut on f108. | «Заберём у двери» at **P-LOW**, 2.75–4.40 (f66–f105) | Whip blur | B2.3 (3.00): the courier turns |
| **S3** | 4.50–8.50 · f108–f203 | B3.2–B5.2 | **Journey.** A night felt diorama: a cream ribbon road winds through felt hills, and a tiny unbranded truck with plain wheels climbs with its headlights on. **One continuous move:** follow, then **crane up** through a thin cloud layer into golden dawn over a **felt city edge** (blocks with balconies, poplar rows, mountains behind). | IN: whip landing. OUT: **haze cut**: the plate's last frames are cloud wisps, an 8-frame cream bloom peaks on f204, and S4 opens from it. | «По всему / Кыргызстану» at **P-LOW**, 4.75–6.50 (f114–f155). «Видно каждый шаг» at **P-LOW**, 6.75–8.40 (f162–f201). **PiP** «Kiwi Go для магазинов» slides in at 4.75: «Забрали ✓» shown at **5.00**, «В пути» goes lime at **6.00**, «В городе» goes lime at **8.00** | **Lime-white long-exposure light trail** following the truck along the switchbacks (§5.3). PiP. | **Swell 6.00–8.00** on the crane (B4.1–B5.1) |
| **S4** | 8.50–11.00 · f204–f263 | B5.2–B6.3 | **Arrival, city.** Golden morning in an urban courtyard: a 4–5-storey block with balconies, poplars, a blue entrance door. The **recipient** (the young customer) **already holds the parcel** at her chest on f0. She gives a small nod; the courier, back to camera, turns away left. Very slow push-in. | IN: fog-lift out of the haze (8 frames). OUT: **glow cut**: a 4-frame warm bloom flash, cut at its peak on f264. | «Вручаем / по коду получения» at **P-LOW**, 8.75–10.90 (f210–f261). PiP: «У курьера» goes lime at **9.00**. PiP slides out left 10.50–10.75. *(Only if the client supplies the real final label: that chip at 10.00, otherwise none.)* | PiP | B5.3 (9.00) chip. B6.2 (10.50) PiP out |
| **S5** | 11.00–12.50 · f264–f299 | B6.3–B7.2 | **Payoff.** The same living room as S1, now warm: the lamp is on and the parcels are gone. The seller, soft in the background, leans back and smiles, holding her phone loosely with the screen away from camera. Very slow push-in. | IN: glow cut. OUT: **focus-pull cut**: S5 defocuses over its last 6 frames, S6 opens defocused and racks sharp over 8 frames (both done in post). | Incoming bubble «получила, спасибо!» pops at **11.50**, in the same position and style as S1's first bubble | Bubble | **B6.4 (11.50) bubble. Breath 12.00–12.50** |
| **S6** | 12.50–15.00 · f300–f359 | B7.2–B8.3 | **Logo born in the world.** Morning city street. A **parked small box truck, strictly side-on**, cab facing left, with flat blank cream panels and **plain wheels**. A slow lateral dolly right ends with the **rear wheel at (490, 800), Ø ≈ 300 px**. | IN: focus pull. OUT: **R5 flash match-cut**, peak on f360. | none | A lime-white **light sweep** travels left to right across the truck. **In its wake our kiwi-wheel SVG replaces each plain wheel** (front at ≈13.60, rear at **14.00**), plane-locked and static (§5.5) | **HIT B8.1 (14.00)**: rear wheel |
| T2 | 14.88–15.12 · f357–f363 | B8.3 | R5 cream flash: f357–f359 ramp up, **f360 peak**, f361–f363 ramp down. The rear-wheel kiwi becomes the card icon at the same x/y. | Cut on f360 | — | Flash | **PEAK B8.3 (15.00)** |
| **Card** | 15.00–20.00 · f360–f479 | B8.3–B10.4 | Paper end card (§1.4) | IN: R5. OUT: **R7** cream fog to 20 % over 19.60–20.00 (f470–f479), which matches f0 for the loop | Wordmark, proposition, price, CTA (§1.4) | Card render | Price on **B9.1 (16.00)**. **CTA on B9.2 (16.50)**. WhatsApp line B9.3 (17.00). Loop B10.4 → B1.1 |

Shot count: 6 plus the card. Every cut is hidden in a leak, a whip, a haze, a glow, a focus pull or a flash. There are no dissolves between unrelated shots.

### 1.3 Supers, bubbles and UI: exact copy, line breaks, positions (Onest, widths measured)

| ID | Text (RU, final; "/" = line break) | Font | Measured width | Position | In → out (s) |
|---|---|---|---|---|---|
| BU-1 | где моя посылка? | Onest SemiBold 68, ink, on a paper #FFFDF7 incoming bubble | 591 px | left edge x 100, top y 330, tail bottom-left | 0.00 → 2.50 (out under the leak) |
| BU-2 | уже отправили? | SemiBold 56 | ≈ 443 | x 100, top y 470 | 0.50 → 2.50 |
| BU-3 | ?? | SemiBold 56 | — | x 100, top y 590 | 1.00 → 2.50 |
| BU-4 | Отправлено ✓ (U+2713; single tick) | SemiBold 64, ink on a **lime #B8F03C** outgoing bubble with a 40 px kiwi icon inside on the left | 493 at 68 (≈ 464 at 64) + icon | right edge x 880, top y 720, tail bottom-right | 1.50 → 2.50 |
| SP-1 | Заберём у двери | SemiBold 72, ink, cream #F6F1E4 pill at 92 %, r 28, 14 px lime dot | 603 | P-LOW, centre y 1100 | 2.75 → 4.40 |
| SP-2 | По всему / Кыргызстану | SemiBold 72, two lines, leading 1.12 | 330 / 465 | P-LOW, centre y 1100 (pill ≈ 989–1211) | 4.75 → 6.50 |
| SP-3 | Видно каждый шаг | SemiBold 72 | 669 | P-LOW | 6.75 → 8.40 |
| SP-4 | Вручаем / по коду получения | SemiBold 72, two lines | 305 / 663 | P-LOW (pill ≈ 989–1211) | 8.75 → 10.90 |
| BU-5 | получила, спасибо! | SemiBold 68, paper incoming bubble | 644 | x 100, top y 330 (same as BU-1) | 11.50 → 12.50 |
| PiP | Header: kiwi icon 40 px + «Kiwi Go» (Bold 34, 124 px) over «для магазинов» (SemiBold 24, 173 px). Chips at SemiBold 28: «Забрали ✓» 154 · «В пути» 90 · «В городе» 122 · «У курьера» 138 | Mini phone 320×470, ink bezel 6 px, r 36, paper screen | — | **x 80–400, y 290–760** | 4.75 → 10.75 (slide-in 6 frames, slide-out 6 frames) |

Rules:
- **Bubbles and the PiP never share the screen.** Bubbles are only in S1 and S5; the PiP is only in S3 and S4.
- At most **one pill plus the PiP** at any time.
- Pills cut in on the beat with no fade-in, and leave with a 4-frame fade.
- Bubble pops: scale 0.85 → 1.0 over 6 frames, easeOutBack with at most 5 % overshoot.
- Active chip: lime fill, ink text. Past chips: cream with ✓.
- The PiP order card is built from **real app screenshots** (Q-3). Until they arrive, the card body shows neutral grey placeholder bars and no invented words.
- No text ever goes over the seller's or the recipient's face.

### 1.4 End card (master in-times; cut-down in-times in brackets)

Paper #FFFDF7 with a 4 % cream radial vignette and 2 % grain. Everything sits inside x 100–880, y 270–1250. **The logo on the card is pure**: exact hex, no tint, no bloom, no flare.

| Order | Element | Spec | Position | In at |
|---|---|---|---|---|
| 1 | Logo icon (exact SVG) | Arrives at Ø 300 from the S6 rear wheel at (490, 800). Eases to **Ø 260 at (490, 470)** over 0.35 s, easeInOut | centre (490, 470), spans y 340–600 | 15.00 (cut-down: 6.50) |
| 2 | **Kiwi Go** (U+00A0 between the words) | Onest Bold 128, ink. Type-on through a mask over a pre-rendered centred line, 0.07 s per glyph | baseline y 740, width 468 | 15.25–15.75 |
| 3 | **Посылка — как сообщение** (U+00A0 before the dash) | SemiBold 46, green ink #3F6212. Fade with a 12 px rise | baseline y 808, width 603 | 15.90 |
| 4 | **от 350 сом** (U+00A0 ×2) | Bold 104, ink, 8 px lime underline under «350» | baseline y 930, width 566 | **16.00 (B9.1)** |
| 5 | **за посылку** | SemiBold 40, ink at 70 % (#585A55) | baseline y 982, width 221 | 16.00 |
| 6 | **Оформите доставку** | SemiBold 48, ink | baseline y 1052, width 475 | **16.50 (B9.2)** |
| 7 | Lime pill **kiwigo.kg** | Pill 520×96, r 48, lime #B8F03C, with a 1.5 px stroke of ink at 15 %. Text SemiBold 60, ink (272 px) | centre y 1120 (spans 1072–1168) | 16.50 |
| 8 | **или напишите в WhatsApp** | SemiBold 40, ink at 70 %. Text only; no WhatsApp icon or green unless the client approves (Q-4) | baseline y 1226, width 520 | 17.00 (B9.3) |
| — | Loop fog | cream #F6F1E4 to 20 % | full frame | 19.60–20.00 |

The CTA (rows 6–7) holds 16.50–19.60 = **3.1 s**. Nothing is grey and nothing goes to black.

### 1.5 Beat sheet, master (delivered as `kiwigo_reel_master_20s_beats.txt`)

```
# Kiwi Go hero Reel — master 20.000 s, 24 fps, 120 BPM, 4/4. TC = seconds; frame = TC*24
0.000  f000  B1.1  HIT    hook frame 0, bubble 1 «где моя посылка?»
0.500  f012  B1.2  pop    bubble 2
1.000  f024  B1.3  pop    bubble 3
1.500  f036  B1.4  SEND   lime bubble «Отправлено ✓»
2.500  f060  B2.2  HIT    light-leak cut to pickup (riser 1.5→2.5)
3.000  f072  B2.3  accent courier turns
4.500  f108  B3.2  whip   whip-pan cut to journey
6.000  f144  B4.1  SWELL  crane begins rising; chip «В пути»
8.000  f192  B5.1  swell-top chip «В городе»
8.500  f204  B5.2  cut    haze cut to arrival
9.000  f216  B5.3  accent chip «У курьера»
11.000 f264  B6.3  cut    glow cut to payoff
11.500 f276  B6.4  accent bubble «получила, спасибо!»
12.000 f288  B7.1  BREATH (drop out, one beat)
12.500 f300  B7.2  re-entry truck shot
14.000 f336  B8.1  HIT    kiwi wheel born (light sweep)
15.000 f360  B8.3  PEAK   flash cut to card
16.000 f384  B9.1  accent price
16.500 f396  B9.2  CTA    «Оформите доставку» + kiwigo.kg
17.000 f408  B9.3  accent WhatsApp line
19.500 f468  B10.4 loop   resolve; loop point at 20.000 → 0.000
```
Music shape: groove → riser into 2.5 → open → **swell 6–8** on the crane → settle → breath at 12.0 → hit at 14.0 → **peak at 15.0** → resolve under the CTA. If the licensed track is not at 120 BPM: time-stretch the bed if the difference is ≤ 8 %, or re-conform by multiplying every TC by 120/BPM (115 BPM → 20.9 s).

### 1.6 Cut-down, 10.0 s (5 bars, f0–f239). No new generations.

| TC (s) · frames | Source | Picture and edit | Supers / UI | Beat |
|---|---|---|---|---|
| 0.00–2.00 · f0–f47 | S1 | Hook, fog 20 % → 0 by 0.50 | BU-1 «где моя посылка?» 0.00; BU-3 «??» 0.50; BU-4 «Отправлено ✓» **1.50** | B1.1, B1.2, **B1.4** |
| 1.75–2.25 | T1 | R2 leak, cut at its peak on f48 | — | **HIT B2.1 (2.00)** |
| 2.00–3.50 · f48–f83 | S2 | Pickup, ending in a whip at 3.25–3.50 (cut on f84) | SP-1 «Заберём у двери» 2.10–3.40 | B2.2 courier turns |
| 3.50–5.50 · f84–f131 | S3 | The second half of the crane, 1.25× speed (frame-drop retime, no interpolation) | SP-2 «По всему / Кыргызстану» 3.75–5.40. PiP in at 3.75 with «Забрали ✓»; «В пути» goes lime at **4.00** | **Swell B3.1–B3.4** |
| 5.50–6.50 · f132–f155 | S6 | Last 24 frames of the dolly | none. Light sweep: front wheel 5.70, **rear wheel 6.00** | **HIT B4.1 (6.00)** |
| 6.50 · f156 | T2 | R5 flash, peak on f156 | — | **PEAK B4.2 (6.50)** |
| 6.50–10.00 · f156–f239 | Card | Icon 6.50, wordmark 6.60–7.00, descriptor 6.90, **price 7.00 (B4.3)**, **CTA + pill 7.50 (B4.4)**, WhatsApp line 8.00 (B5.1), fog 9.60–10.00 | §1.4 rows | CTA held 7.50–9.60 = 2.1 s |

The cut-down drops the code-handover and payoff beats: it is the rational paid and retargeting cut. Beat file: `kiwigo_reel_cut_10s_beats.txt`, in the same format as §1.5.

### 1.7 Caption, button, pinned comment (Russian; the client signs off)
> Посылка в другой город — без автовокзала и звонков водителю.
> Заберём у двери и отвезём по всему Кыргызстану. Каждый шаг видно в приложении «Kiwi Go для магазинов».
> Получатель получает код получения в SMS и называет его только курьеру при вручении.
> От 350 сом за место. *(add «вес и размер цену не меняют» only once the client confirms the size limit per place, Q-7)*
> Оформите доставку на kiwigo.kg или напишите нам в WhatsApp. Ссылка в профиле.

- **Ad buttons.** Shops: «Подробнее» → `kiwigo.kg?utm_source=instagram&utm_campaign=hero_reel&utm_content=master`. Private senders: «Отправить сообщение» (WhatsApp destination).
- **Pinned comment:** «Оформить доставку: kiwigo.kg · или пишите в WhatsApp».
- The caption never contains «утром», «завтра», «за ночь», «до обеда» or «экспресс». No city names appear on screen; in the caption they are the client's call.

---

## 2. Style bible

### 2.1 Material: **felt-toy miniature** (chosen)
05 §4.3 asks for "felt or wool-toy texture for people, matching the felt diorama", because it hides faces and hands, reads as local craft (ала-кийиз and шырдак felting) and avoids the Pixar-lite default. Felt is the **material**. We **photograph** it like the reference: through a tilt-shift macro lens. So the reference's lens grammar stays, but the surface is handmade.

- **People:** needle-felted wool dolls with visible soft fibres. Faces are simple: embroidered or stitched calm eyes, a small stitched mouth and gently blushed cheeks. Proportions are **adult and dignified**: the head is about 1/6 of body height, never chibi or big-headed, with no exaggerated features and no comic poses.
- **Vehicles and props:** a felt or matte-painted-wood toy truck, card-and-wood buildings, flocked felt trees and poplars, felt hills, a cream ribbon road of matte card. Parcels are matte cream card with sand paper tape.
- **Not allowed:** glossy plastic, photoreal skin, clay or claymation smears, LEGO-like studs, anime eyes.

### 2.2 Lighting
- **Story arc, one rig logic.**
  - S1: cold night. The key is the phone glow (cool, 7000 K), with warm practical bokeh outside.
  - S2: warm evening. A single warm lamp on the landing, 3200 K.
  - S3: blue night that becomes golden dawn. The headlights are the only warm source until the dawn rim light rises from the right.
  - S4–S6: golden morning, low sun from the **right** (camera-right) in every shot, long soft shadows.
  - S5: warm lamp plus morning window.
- Always **soft**: large diffused sources, gentle bloom on highlights, and highlights that roll off to cream.

### 2.3 Colour grade (applied in post on every clip, R6 from 03)
- **Golden and airy, with lifted blacks:** curves `0/0.06 0.5/0.55 1/0.96`. The cream highlight pass pulls values above 0.8 toward #F6F1E4 at 20 % soft-light.
- **Saturation per shot**, falling toward the brand moment: S1 0.80 (cool); S2 0.90; S3 0.75 → 0.65; S4 0.70; S5 0.65; **S6 0.55**. That leaves the lime kiwi wheel and the lime sweep as the most saturated pixels in the film. The card is near-neutral.
- **Lime accents** live only in the cap, our trail and sweep, our bubbles, chips and pill, and our logo. Nothing else in the plates is lime.
- Bloom: threshold 0.75, σ 40 px at quarter resolution, screen at 15–25 %. Grain: 2–3 % luma. Vignette PI/5.

### 2.4 Lens and depth of field
- A tilt-shift macro look: the equivalent of a 90 mm macro at f/2.8, from a slightly high vantage (15–30° down) for the exteriors and eye level for the interiors.
- **A narrow sharp band through the subject** with strong blur at the top and bottom. Fixed band heights: S1/S5 the band runs through the seller at y 950–1150; S2 at y 700–1200; S4 at y 450–950; S6 at y 650–950.
- In post, reinforce the tilt-shift if a plate is too sharp (03 R6).

### 2.5 Characters (no text, letters, logos or patches on any clothing)
- **Seller ("SH-1"):** a Kyrgyz woman of about 30, modern and urban. Dark hair in a neat low bun; warm medium skin; a cream chunky-knit cardigan over a plain sand-coloured dress; ink-coloured house slippers. Calm, capable, kind. No headscarf and no national costume: she is an everyday city seller.
- **Courier ("SH-2"):** a Kyrgyz man of about 30. Short neat dark hair. A **plain lime (#B8F03C) cap with no logo**, a plain **ink (#111410) zip jacket**, sand trousers, ink trainers. Neat posture. Mostly seen from behind at three-quarters. He appears **only in the city** (S2, S4).
- **Recipient (in the S4 frame only, no sheet):** a Kyrgyz woman of about 23. Dark hair in a low ponytail, a sand wool coat over a cream sweater, a plain kiwi-brown (#7A5A3C) scarf. Her silhouette is clearly different from the seller's (ponytail and coat versus bun and cardigan).
- **Dignity rules (05 §4.2):** no comic posing, no hugging the box like a prize, no exaggerated features, no ethnic caricature.

### 2.6 Props and set rules
- **Parcel ("OB-1"):** a cream matte card box with a 3:2:1.5 ratio and sand paper tape. **One blank, round cream sticker**, Ø ≈ 1/4 of the box width, sits on the front face. It has no print, no barcode and no lines.
- **Truck ("OB-1"):** a small generic box truck. Ink cab, cream box body, **flat, completely blank side panels**, plain flat windows. No grille badge, no plates, no lettering. **Plain wheels:** a matte ink tyre with a **flat, flush, featureless cream hub disc**: no spokes, no bolts, no hubcap relief, no tread text. The wheel should read as a clean flat circle side-on, so our SVG covers it completely.
- **City set:** Soviet-era 4–5-storey blocks with balconies, poplar rows, apricot trees, blue-painted entrance doors and metal canopies. All windows, doors and balconies are blank, with **no signs, numbers or graffiti**.
- **Banned in every frame:** yurts, tunduks, round crowns with crossing spokes, лепёшка/нан, kalpaks, shyrdak medallions in hero positions, flags, state emblems, recognisable landmarks (no Sulaiman-Too, no Ala-Too Square), real vehicle brands, messenger UI, any text or numbers.

### 2.7 STYLE ANCHOR (paste verbatim into every still prompt)
> **Handmade needle-felted wool miniature diorama photographed with a tilt-shift macro lens: soft visible wool fibres, matte card and painted-wood props, dignified adult felt-doll figures with simple stitched faces, narrow sharp focus band with strong soft blur at top and bottom, soft diffused light with gentle bloom, lifted shadows and creamy highlights, muted palette of cream #F6F1E4, sand #ECE6D6 and kiwi-brown #7A5A3C with ink-dark #111410 details and only tiny lime #B8F03C accents; every surface plain and unbranded — no text, no letters, no numbers, no signage, no logos.**

The per-shot time-of-day and light sentence comes **after** the anchor and never replaces it.

---

## 3. Per-shot generation spec

Conventions:
- **GPT-hi** = `gpt_image_2_6`, `quality:"high"`, `resolution:"2k"`, `aspect_ratio:"9:16"`.
- **GPT-med** = the same at `quality:"medium"`, with `count:2` for exploration.
- **SDR** = `seedream_5_5`, `resolution:"2k"`, `aspect_ratio:"16:9"`.
- **K3P** = `kling3_0`, `mode:"pro"`, `sound:"off"`, `aspect_ratio:"9:16"`, `medias:[{role:"start_image"}]`.
- **FLF-P** = `kling_o3_flf`, `mode:"pro"`, `sound:"off"`, 9:16, with start_image + end_image.
- Every start frame is an **edit** with `image_references` = the relevant sheets (and the previous approved frame where noted).
- Kling outputs 1076×1924 at 24 fps (§5.1).
- Before every animation, read the still at 100 % for: letters, extra fingers, stray kiwi or lime objects, brand-like shapes.

### 3.0 Sheets (Gate 1)

**SH-1 Seller sheet.** SDR (3.5 cr). Run the `character-sheet` workflow, Classic 3D / drawn route, at execution time (read its instructions then).
> Character turnaround sheet of ONE handmade needle-felted wool doll: a Kyrgyz woman about 30, modern city seller, dark hair in a neat low bun, warm medium skin, simple stitched calm eyes and small stitched smile, cream chunky-knit cardigan over a plain sand dress, ink-coloured slippers; adult dignified proportions, head about one sixth of body height. Views: front, three-quarter left, side, back, plus two head close-ups (calm; soft relieved smile). Plain cream studio background, soft even light, consistent scale. No text, no labels, no letters, no logos, no patterns on clothing.

Accept if: one identity in all views; no letters or labels; adult proportions; wool texture visible; nothing printed on the clothes. Fallback: re-run once with "no captions or labels"; then try GPT-hi at 16:9 (2.75).

**SH-2 Courier sheet.** SDR (3.5 cr).
> Character turnaround sheet of ONE handmade needle-felted wool doll: a Kyrgyz man about 30, short neat dark hair, simple stitched calm face, plain lime #B8F03C baseball cap with no logo, plain ink #111410 zip jacket with no patches or print, sand trousers, ink trainers; adult dignified proportions. Views: front, three-quarter right, side, back three-quarter, back; plus one pose holding a plain cream card box with both hands at chest height. Plain cream studio background, soft even light. No text, no labels, no letters, no logos.

Accept if: the cap is plain lime and is the only lime item; the jacket is fully blank; the box-holding hands are clear, with ≤ 5 fingers each; nothing is written anywhere. Fallback: same as SH-1.

**OB-1 Truck and parcel object sheet.** `gpt_image_2_6` high 2k **16:9** (2.75 cr).
> Object reference sheet, felt-and-painted-wood toy miniature: (1) a small generic box truck, ink-dark cab, cream box body, completely flat blank side panels, plain windows, no grille badge, no plates, wheels are matte ink tyres with a flat flush featureless cream hub disc (no spokes, no bolts) — shown strictly side-on (cab facing left), three-quarter front, and rear; (2) a cream matte card parcel box with sand paper tape and one blank round cream sticker on its front face, shown front and three-quarter. Plain cream background, soft even light, consistent scale. No text, no letters, no numbers, no logos.

Accept if: the side-on view is truly orthographic-looking; both wheels are perfect circles with flat hubs; the panels are blank; the sticker is round and blank; nothing resembles a real truck brand. Fallback: one re-run; then `seedream_v4_5` (re-pose).

### 3.1 S1, hook (night living room)
- **References:** SH-1, OB-1 (parcel).
- **Start frame (GPT-hi, edit):**
> Felt miniature living room at night, viewed slightly from above. The seller from the reference sheet sits small on a plain sand sofa in the lower centre of the frame (her face around y 1050 of 1920), surrounded by stacks of the cream parcels from the reference, each with its blank round sticker. She holds a phone in both hands at chest height, screen facing her, its plain back toward camera; the cool phone glow lights her face. Behind her a window shows soft warm out-of-focus city lights. Upper third of frame is calm dark wall with soft bokeh (space for chat bubbles). Cold blue night mood with one cool key from the phone. [STYLE ANCHOR]
- **Video:** K3P, **5 s** (7.5 cr). Use f0–f59, or f0–f47 in the cut-down.
- **Motion prompt:**
> The seller slowly lowers the phone a little and exhales, her shoulders sinking softly; the cool phone light flickers gently on her face; the parcels stay perfectly still. Very slow push in, already moving from the first frame. Faces, hands and felt textures keep their exact shape — no morphing, no warping, no extra fingers. All surfaces stay blank: no text, no letters, no logos.
- **Accept still if:** the seller matches SH-1; her face is readable at thumbnail size; the upper third is calm; the phone's back is blank; ≥ 6 parcels, all with blank stickers; no text.
- **Accept clip if:** motion is present on f0 (no frozen start); no face drift over f0–f59; the phone does not grow a screen or a logo toward camera; no flicker; fingers stable.
- **Fallback:** retry once with "camera push is very slow; hands do not move". If it fails twice, do a **2.5D push** on the approved still (a Python zoom of 1.00 → 1.06 plus a phone-glow flicker composite), which costs 0 cr.

### 3.2 S2, pickup (Gate 2 motion test)
- **References:** SH-1, SH-2, OB-1 (parcel).
- **Start frame (GPT-hi, edit):**
> Felt miniature apartment stairwell landing in warm evening light: a plain cream door open on the left, the seller from sheet 1 stands in the doorway, hands resting together at her waist, soft smile. The courier from sheet 2 stands right of centre, back three-quarters to camera, already holding the cream parcel with both hands at chest height, its blank round sticker visible. One warm wall lamp, plain walls, no door numbers. Medium shot, subjects within the middle band (y 700–1200 of 1920), empty space on the right for him to walk into. [STYLE ANCHOR]
- **Video:** K3P, **4 s** (6.0 cr). Use about 2.0 s (f60–f107).
- **Motion prompt:**
> The courier, already holding the parcel with both hands, turns slowly to his right and walks out of frame to the right; the seller stays in the doorway and her smile grows softly, her hands stay still at her waist. Locked-off camera. The parcel keeps its shape and its blank round sticker; hands stay simple with no extra fingers; no morphing of faces or bodies. All surfaces stay blank: no text, no letters, no numbers, no logos.
- The whip-pan is **ours** (post), not AI.
- **Accept still if:** both identities match their sheets; the box is held by the courier only; hands clean; the cap is the only lime; nothing written on the door or walls.
- **Accept clip if:** no fingers merge into the box; the box does not deform; the seller's face is stable; the courier exits cleanly by about 3.5 s; ≥ 2.0 s usable.
- **Fallback:** retry 1 adds "the courier simply turns and walks right, the seller only smiles". Retry 2 is a **re-stage**: the courier is already turning away, box at his side. If that also fails, use `seedance_2_0` `fast` 720p with SH-1 and SH-2 as references (12.5 cr), upscaled.

### 3.3 S3, journey crane (FLF): end frame first
- **References:** OB-1 (truck) for both frames. **On Kling Omni an end frame cannot be combined with references**, so the identity must already be inside the two frames.
- **End frame (GPT-hi, generate FIRST):**
> Felt miniature city edge at golden dawn, seen from above through thinning soft clouds: rows of small cream and sand card apartment blocks with balconies, lines of flocked poplars, a few apricot trees, a cream ribbon road entering the city from lower left, felt mountains with soft snowy tops behind under a pale golden sky; low warm sun from the right; thin wisps of cloud in the foreground corners. No landmarks, no signs, no text. [STYLE ANCHOR]
- **Start frame (GPT-hi, an edit of the end frame + OB-1):**
> Same miniature world, same horizon height and same sun side, but at blue night and from a low vantage on the mountain road: a cream ribbon road winds up felt hills in switchbacks; the small truck from the reference, tiny (about 60 px long) in the lower middle, climbs with warm headlights on; a thin cloud layer drifts above the ridge in the upper half. Cool blue moonlight, one warm source (the headlights). [STYLE ANCHOR]
- **Video:** FLF-P, **5 s** (6.25 cr). Retime to 4.0 s with an ease curve (a 1.25× frame-drop speed-up, no interpolation).
- **Motion prompt:**
> The tiny truck drives forward along the winding road with its headlights on. One continuous camera move: hold for half a second, then a smooth crane up and tilt up over the ridge, rising through a thin layer of soft cloud while the light warms from blue night to golden dawn, revealing the miniature city in front of the mountains and ending exactly on the last frame. Slow ease-in and ease-out, no cuts. Road, hills and buildings stay rigid — no morphing, no melting, no warping. All surfaces stay blank: no text, no letters, no signage, no logos.
- **Accept stills if:** horizon and sun side match between the frames (overlay at 50 %); the road is continuous; the truck is unbranded with plain wheels; the city has no signs or landmark; the sky has room for the PiP at top-left.
- **Accept clip if:** no dissolve-like morph of road into city; buildings stay rigid; the truck stays visible for ≥ 1.5 s (needed for the trail track); the cloud pass hides the scene change; no flicker.
- **Fallback:** retry 1 adds "the camera rises vertically; the road and city do not transform into each other". Retry 2: `kling4_0` `image-to-video` 720p, with start, end and one middle keyframe (the ridge with cloud at mid-height, GPT-hi 2.75) as `image_references` (11.25 cr). If that fails, **split into two cuts**: animate the night road (K3P, 7.5) and the dawn city (K3P, 7.5), and hide the cut in a composited cloud wipe. Cinema Studio 3.0 720p (25 cr) is used **only with client approval**.

### 3.4 S4, city arrival
- **References:** SH-2, OB-1 (parcel). The recipient is described in the prompt (no sheet).
- **Start frame (GPT-hi, edit):**
> Felt miniature city courtyard in golden morning light, low sun from the right: a 4–5-storey card apartment block with blank balconies, a blue-painted entrance door with a plain metal canopy, poplars and an apricot tree. A young Kyrgyz woman of about 23 — dark hair in a low ponytail, sand wool coat over a cream sweater, plain kiwi-brown scarf — stands in the middle band (y 450–950 of 1920) holding the cream parcel against her chest with both arms, its blank round sticker facing camera, a small grateful smile. The courier from the reference sheet stands at the left edge, back to camera, already turning away. Lower part of frame calm paving (space for a caption). No numbers, no signs. [STYLE ANCHOR]
- **Video:** K3P, **4 s** (6.0 cr). Use 2.5 s (f204–f263).
- **Motion prompt:**
> The young woman keeps holding the parcel against her chest and gives a small grateful nod; the courier, back to camera, walks slowly out of frame to the left. Locked camera with a very slow push in. The parcel keeps its shape and blank sticker; her hands stay still on the box with no extra fingers; no morphing of faces or bodies. Balconies, doors and walls stay blank: no text, no letters, no numbers, no logos.
- **Accept still if:** clearly urban (no gate, no village, no yurt); the recipient is different from the seller; no phone visible; she alone holds the box; nothing written anywhere.
- **Accept clip if:** her face and hands are stable; the box is rigid; the courier leaves cleanly; the buildings are rigid.
- **Fallback:** retry 1 drops the courier entirely (she alone, nodding). Retry 2: `seedance_2_0` fast 720p (12.5 cr). Last resort: a 2.5D push on the still (0 cr).

### 3.5 S5, payoff (warm living room)
- **References:** the **approved S1 still** + SH-1.
- **Start frame (GPT-hi, edit of S1):**
> The same living room as the reference frame, same camera and layout, now warm: a table lamp on, golden light, the parcel stacks are gone, the sofa tidy. The seller sits back relaxed, softly out of focus in the middle of the frame, holding her phone loosely in her lap with the screen turned away from camera, a gentle smile. Upper third calm and soft (space for a chat bubble). [STYLE ANCHOR]
- **Video:** K3P, **3 s** (4.5 cr). Use 1.5 s (f264–f299).
- **Motion prompt:**
> The seller leans back a little on the sofa and her smile grows softly with a slow breath; the lamp glow stays steady. Very slow push in. Faces and hands keep their shape — no morphing, no extra fingers. All surfaces stay blank: no text, no letters, no logos.
- **Accept still if:** the layout matches S1 (an overlay check: sofa, window, lamp); she is the same person; no parcels; the phone screen is not visible.
- **Accept clip if:** stable; no face drift (she is soft anyway).
- **Fallback:** a **2.5D push on the still** plus a lamp-flicker composite (0 cr). This is the preferred fallback after just one failure.

### 3.6 S6, parked side-on truck (the logo plate)
- **References:** OB-1 (truck, the side-on view), plus the S4 still for the city look.
- **Start frame (GPT-hi, edit):**
> Felt miniature city street in golden morning light, low sun from the right: the small truck from the reference sheet parked strictly side-on, perfectly parallel to the camera, cab facing left, flat blank cream box panels, plain wheels with flat featureless cream hubs. Camera at wheel-hub height, level, no perspective tilt. Framing: the front wheel and cab on the left half, the rear wheel at about x 640, y 800 of 1080×1920, about 300 px in diameter; behind the truck a soft-focus apartment block with poplars; plain clean paving below. No text, no plates, no logos, no numbers. [STYLE ANCHOR]
- **Video:** K3P, **5 s** (7.5 cr). Use the last 2.5 s (f300–f359), with the dolly ending with the rear wheel at (490, 800).
- **Motion prompt:**
> The parked truck stays completely still and its wheels do not turn. The camera trucks slowly and steadily to the right, parallel to the truck's side, keeping it strictly side-on, ending with the rear wheel near the centre of the frame. Constant speed, no rotation, no zoom, no tilt. The truck body, wheels and blank panels keep their exact shape — no morphing, no warping. All surfaces stay blank: no text, no letters, no numbers, no logos.
- **Accept still if:** both wheels fit circles with an axis ratio ≥ 0.97; the hubs are flat and featureless; the panels are blank; the rear wheel Ø is 270–330 px.
- **Accept clip if:** this is the **§0.6 gate**. A 2-point track (hub + rim) holds within 2 px over the used window; the wheels stay circular (ratio ≥ 0.97 in every frame); the wheels do not rotate; no panel text appears.
- **Fallback:** retry 1 adds "camera moves very slowly; nothing else moves". If it fails twice, use **2.5D**: separate the approved still into a background layer and a truck layer (`remove_background` costs credits, so use an OpenCV/GrabCut mask instead at 0 cr) and do a parallax pan in Python. This gives a perfect track at 0 cr.

### 3.7 What is **not** AI
- The light trail, the kiwi wheels, the light sweep, bubbles, the PiP, chips, supers, the end card, leaks, flashes, the whip, the focus pull and every logo.
- Optional hook head H-C (the sprite-composited lifting box) needs only one GPT-med still (1.0 cr) if the client wants it later. It is not in this budget.

---

## 3b. Real credit quotes (live, 2026-11-18, 9:16, silent)

**Balance: 488.92 credits (plan: plus).**

| Config (exact params quoted) | Credits |
|---|---|
| `kling3_0` pro, 5 s, sound off | **7.5** |
| `kling3_0` pro, 4 s, sound off | **6.0** |
| `kling3_0` pro, 3 s, sound off | **4.5** |
| `kling3_0` std, 5 s, sound off | 6.25 |
| `kling3_0` std, 3 s, sound off | 3.75 |
| `kling_o3_flf` pro, 5 s, sound off | **6.25** |
| `kling_o3_flf` pro, 6 s, sound off | 7.5 |
| `kling_o3_flf` std, 5 s, sound off | 5.0 |
| `seedance_2_0` fast, 720p, 5 s (fallback) | 12.5 |
| `kling4_0` image-to-video, 720p, 5 s (fallback) | 11.25 |
| `cinematic_studio_3_0` 720p, 5 s, genre epic (approval only) | 25 |
| `seedream_5_5` 2k, 16:9 (sheets) | **3.5** |
| `gpt_image_2_6` high 2k, 9:16 (final frames) | **2.75** |
| `gpt_image_2_6` high 2k, 16:9 (object sheet) | 2.75 |
| `gpt_image_2_6` medium 2k, 9:16, count 1 / **count 2** | 1.0 / **2.0** |
| `gpt_image_2_6` medium 2k, 16:9 | 1.0 |
| `gpt_image_2_6` low 1k, 9:16 | 0.25 |

Durations were chosen to the quote: S2 and S4 at 4 s and S5 at 3 s save 4.5 cr against all-5 s, and each still gives ≥ 1.5× the used length for trimming.

---

## 4. Production order, stop-loss gates and budget

### 4.1 Order

**Gate 0, before any spend (0 cr).** Client answers Q-1 to Q-6 (§6). Copy the Onest TTFs (OFL) into the repository. Build the composite pipeline skeleton (§5) with placeholder plates, so the UI, card and beat file are reviewed in parallel.

**Gate 1, style frames only (cheap).**

| Step | Item | Config | Qty | Cr |
|---|---|---|---|---|
| 1a | SH-1 seller sheet | seedream_5_5 2k 16:9 | 1 | 3.5 |
| 1b | SH-2 courier sheet | seedream_5_5 2k 16:9 | 1 | 3.5 |
| 1c | OB-1 truck and parcel sheet | gpt_image_2_6 high 2k 16:9 | 1 | 2.75 |
| 1d | Style frames for S1, S2, S3-end, S3-start, S4, S5, S6, 2 variants each | gpt_image_2_6 medium 2k 9:16, count 2 | 7 calls | 14.0 |
| | **Gate 1 total** | | | **23.75** |

- **Show the client:** the 3 sheets plus the best variant of each of the 7 frames, assembled as a 7-panel animatic with our supers composited on top.
- **Approval needed:** felt style, characters, city arrival, truck, colour arc.
- **STOP if not approved.** Revise at medium only. One revision round is budgeted under retries.

**Gate 2, one motion test.**

| Step | Item | Config | Cr |
|---|---|---|---|
| 2a | S2 final start frame | GPT-hi | 2.75 |
| 2b | **S2 motion test** (riskiest: two people and a box) | K3P 4 s | 6.0 |
| | **Gate 2 total** | | **8.75** |

- The test runs on **Pro**, not std: the gap is only 1.25 cr, and a passing test becomes the final clip.
- Check it in the real pipeline: grade, supers, and frame-0 sharpness.
- **STOP-LOSS:** if S2 fails twice, re-stage as in §3.2 before any other clip is animated. If the felt look breaks in motion (texture boiling, faces sliding), stop and return to Gate 1 with the client. Do not push on.

**Gate 3, all clips.**

| Step | Item | Config | Cr |
|---|---|---|---|
| 3a | Final frames for S1, S3-end, S3-start, S4, S5, S6 | GPT-hi ×6 | 16.5 |
| 3b | S1 | K3P 5 s | 7.5 |
| 3c | S3 | FLF-P 5 s | 6.25 |
| 3d | S4 | K3P 4 s | 6.0 |
| 3e | S5 | K3P 3 s | 4.5 |
| 3f | S6 | K3P 5 s | 7.5 |
| | **Gate 3 total** | | **48.25** |

Order inside Gate 3: S6 (the logo plate: run the §0.6 gate immediately) → S3 → S4 → S1 → S5.

**Stop-loss rules:**
- At most **2 retries** on S2, S3 and S4, and **1 retry** on S1, S5 and S6. After that, use the shot's 0-cr or cheap fallback.
- **Change the still before changing the model.**
- Halt Gate 3 and re-plan with the client if the cumulative spend reaches **170 cr** before every shot is accepted.

### 4.2 Budget

| Line | Cr |
|---|---|
| Gate 1 | 23.75 |
| Gate 2 | 8.75 |
| Gate 3 | 48.25 |
| **BASE** | **80.75** |
| Retries, images: sheet redos (2 × 3.5), object sheet redo (2.75), one high redo per final frame (7 × 2.75), one extra medium exploration round (2 × 2.0) | 33.0 |
| Retries, video: a 1st retry on every clip (37.75) and a 2nd on S2, S3 and S4 (6.0 + 6.25 + 6.0) | 56.0 |
| **BASE + RETRIES (expected worst normal case)** | **169.75** |
| Paid fallbacks: `seedance_2_0` fast 720p for S2 and S4 (2 × 12.5), `kling4_0` 720p for S3 (11.25), plus its middle keyframe (2.75) | 39.0 |
| **MAX CEILING** | **208.75** |
| Not budgeted (client approval required): Cinema Studio 3.0 720p for S3 | +25 per try |

- With a balance of **488.92**, the reserve is **280.17 cr at the ceiling**, or **408.17 cr** if only the base is spent. 05 asked for a cap of about 210 and a reserve of ≥ 250; both are met.
- The base is **80.75 cr**, well under the 200 target. The ceiling stays under 210.

---

## 5. Compositing plan (our pipeline: Python/numpy + ffmpeg + Playwright)

### 5.1 Timeline and ingest
- **24 fps project timeline**, 1080×1920. No 24→30 resampling anywhere.
- Ingest each Kling clip (1076×1924, 24 fps): `ffmpeg -i in.mp4 -vf "scale=1080:-2:flags=lanczos,crop=1080:1920" -pix_fmt rgb48le frames/%04d.png`. The 1076→1080 upscale gives 1927 rows, which are centre-cropped to 1920.
- Retimes use frame-drop or frame-hold maps on the 24 fps grid. S3 runs at 1.25× via a precomputed ease map; `minterpolate` is allowed only for speed-ups ≤ 1.3× and only if the frame-drop version judders.
- **QC:** after ingest and after export, run the frame-difference script. The duplicate-frame ratio must be **< 2 %**.

### 5.2 Layer order per frame
1. Plate.
2. R6 grade (§2.3), per-shot saturation and tilt-shift reinforcement.
3. In-world composites: the S3 trail, the S6 kiwi wheels.
4. Scene tint over the in-world composites: multiply 8–10 % from the plate's local luminance, plus a soft scene-coloured haze.
5. Light layers: bloom, the S6 light sweep, leaks, flashes. **These go over the logo.**
6. Grain (2–3 %).
7. UI: bubbles, PiP, supers. These are crisp and never under grain or bloom.
8. Fog.

**Recipes from 03 (exact):**
- **R1 fog-lift (open):** `out = lerp(frame, CREAM(246,241,228), k)`, with `k = 0.20·(1−easeOutCubic(t/0.5))` for t in 0–0.5 s. Bloom strength follows k.
  - Loop tail: `k` ramps 0 → 0.20 over f470–f479 on the card, so f479 ≈ f0.
- **R2 light leak (T1, f54–f66, cut on f60):** procedural. 3 Gaussian blobs (radius 0.6–1.0 × W) on noise-perturbed left-to-right paths. Colours #FFB347, #FFD27A and cream, plus a **lime #B8F03C fringe at 25 %** on the trailing blob's edge (the "sent" message). Add-blend with `sin(π·p)` intensity and a global lift to luma ≈ 230 at f60. Add one soft circular bokeh disc (alpha 0.5) bottom-left. (Licensed 4K stock with a screen blend is allowed instead, if the client licenses it.)
- **Haze cut (S3→S4, f200–f208):** a cream bloom wash to luma ≈ 225, peaking on f204; S4 fog-lifts 0.6 → 0 over 8 frames.
- **Glow cut (S4→S5, f262–f266):** a 4-frame warm (#FFE6B8) bloom flash, cut on f264.
- **Whip (S2→S3, f102–f113):** horizontal directional blur ramping to 120 px (a box-blur stack) on the S2 tail and the S3 head, plus a 20 px horizontal offset per frame, cut on f108.
- **Focus pull (S5→S6):** a Gaussian σ ramp 0 → 18 px over f294–f299, then 18 → 0 over f300–f307.
- **R5 flash (T2):** cream #FFFDF7 blended at 35 % → 70 % → 100 % on f357–f359, **100 % on f360** (the card's first frame, composited under it), then 70/35/10 % on f361–f363.
- **Match cut:** the rear-wheel logo position (490, 800, Ø 300) on f359 equals the card icon on f360. It then eases to (490, 470, Ø 260) over f360–f368 (easeInOut).

### 5.3 S3 light trail
- Hand-place the road centreline as a spline on keyframes every 6 frames.
- Solve a per-frame homography of the ground plane: ORB features on the road and hills, RANSAC, smoothed with Savitzky–Golay (window 9). This keeps the spline glued while the camera cranes.
- Track the truck's headlights with a template match. The trail is drawn from the start of the road up to the truck's current position.
- **Trail look:** a core of 4 px #F4FFE0, a lime #B8F03C glow (σ 10 px at 60 %), and a soft outer bloom. The opacity of the tail fades along its length over about 1.5 s of travel. No sparkles, no particles.
- The trail fades out as the cloud layer passes (f170–f185).

### 5.4 Type, UI and card (HTML + Playwright)
- **Fonts:** copy `onest-600.ttf` and `onest-700.ttf` (plus the OFL licence) into `kiwi-go-soon/brand-reel/build/fonts/`. Every HTML file declares `@font-face { src: url("fonts/onest-600.ttf") }`. There are **no Google Fonts or system-font fallbacks**: the font stack is `"Onest Local"` only, so a missing glyph shows up as tofu rather than a silent substitution.
- Before rendering, a Playwright check asserts `document.fonts.check('600 72px "Onest Local"', 'ёЁ«»—…✓')` and that the computed font is "Onest Local" for every element.
- **Components:** `bubble.html` (incoming and outgoing), `pill.html` (supers, one and two lines), `pip.html` (mini phone, header, chips, active-state param), `card.html` (§1.4 layout, type-on mask steps).
- Each component is driven by URL params (text, state, size) and screenshotted as a **transparent PNG at 2× (2160×3840), then downsampled** with Lanczos.
- Animation (scale-pops, slides, type-on masks, fades) is done in Python on those PNGs, frame by frame, on the 24 fps grid. Type-on reveals a pre-rendered **centred** line through a left-to-right mask in glyph steps, and never re-centres.
- **Typesetting:**
  - U+00A0 in «Kiwi Go», «от 350 сом», and before «—» in «Посылка — как сообщение».
  - ✓ is U+2713 (U+2714 is missing in Onest).
  - «Заберём» keeps ё.
  - Ink text on cream or lime only. Lime is never text on light.
- **Logo:** render `kiwi-go-soon/logo/kiwi-go-logo.svg` through Playwright at 2× the target size (the existing `logo/render.js` pattern), with a transparent background. The PNG is never recoloured.

### 5.5 Kiwi-wheel logo tracking (S6)
1. **Track:** on each frame of the used window, fit the tyre circle (HoughCircles seeded from the previous frame, refined by edge-based ellipse fitting) for both wheels → centre (x, y), radius r and axis ratio. Then template-track one rim point on the tyre's tread edge, which gives 2 points.
2. **Gate:** the hub residual is ≤ 2 px after Savitzky–Golay smoothing (window 7); the axis ratio is ≥ 0.97; the radius drift is ≤ 1 %. **If any test fails, the wheels stay plain** and we switch to the §3.6 2.5D fallback plate.
3. **Place:** the SVG render scaled to the **tyre** diameter, because the logo's own ink r100 tyre covers the plate tyre exactly. It is **static (0° rotation)**, since the truck is parked, and centred on the smoothed hub.
4. **Birth in the sweep:** the sweep is a soft diagonal band (width 1.2× the wheel diameter, core #F4FFE0, lime fringe, add-blend at 70 %) travelling left to right in step with the dolly.
   - The logo's alpha is revealed **behind the band**, as a wipe mask = the band's trailing edge. The front wheel turns kiwi around f326 (13.60) and the **rear wheel on f336 (14.00)**.
   - At the moment of reveal: a 6-frame scale of 0.97 → 1.0 (no overshoot), and the sweep's peak passes **over** the logo.
5. **Integration:** a multiply shading of 8 % from the plate's wheel luminance (the sun is from the right, so the left edge is slightly darker), a 1 px contact shadow at the tyre's bottom, and grain on top.
   - **No tint on the card version.** The card icon on f360 onward is the pure render; the in-world version cross-switches under the flash peak.

### 5.6 Export spec
- Master: `kiwigo_reel_master_20s_v01.mp4`. Cut-down: `kiwigo_reel_cut_10s_v01.mp4`.

```
ffmpeg -framerate 24 -i comp/%04d.png -c:v libx264 -profile:v high -preset slow \
  -crf 16 -maxrate 16M -bufsize 32M -g 48 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -vf "scale=1080:1920:flags=lanczos,format=yuv420p" -an -movflags +faststart out.mp4
```

- 1080×1920, H.264 High, yuv420p, 24 fps CFR, **no audio stream (`-an`)**, Rec.709 tags, `+faststart`, about 10–16 Mbps.
- Beat markers: `kiwigo_reel_master_20s_beats.txt` and `kiwigo_reel_cut_10s_beats.txt` (§1.5 format: seconds, frame, bar.beat, label, note).
- Verify with `ffprobe` (codec, fps, no audio, dimensions, duration exactly 20.000 / 10.000 s).
- Also export a cover frame: the card at f420, PNG.
- Run the 03 §4 checklist line by line, the Meta safe-zone overlay check, and the muted 3-stranger test before the client sees the cut.

---

## 6. Client questions (answers needed before Gate 1)

**Already decided:** coverage «По всему Кыргызстану», «от 350 сом», CTA «Оформите доставку» + kiwigo.kg + WhatsApp, Russian only.

| # | Question | Why it blocks Gate 1 | Default if no answer |
|---|---|---|---|
| Q-1 | Please confirm **in writing** that you choose «По всему Кыргызстану» knowing that regions go through partner services and some points are «до центра» or «у дороги». | It is a legal and credibility record for a claim our reviewers flagged | We do not render without the written note |
| Q-2 | Do you approve the **felt-toy miniature** style (handmade wool figures shot like a tilt-shift miniature), as opposed to a glossy toy look? | It sets every prompt | Felt (recommended) |
| Q-3 | Can you send **real screenshots of «Kiwi Go для магазинов»** (order card, status labels)? Is there a final status after «У курьера», and what exactly is it called? | The PiP must copy the real UI; no invented labels | Chips stop at «У курьера»; the card body is neutral bars |
| Q-4 | What **WhatsApp number** goes in the caption and button? Do you want the number or the WhatsApp icon on the end card, or text only («или напишите в WhatsApp»)? | The card layout and the trade-dress check | Text only, with no number and no icon |
| Q-5 | Does **kiwigo.kg** take a private sender straight to ordering? Which page should the ad button open? | The CTA must not dead-end | kiwigo.kg home with UTM |
| Q-6 | Does the wordmark **«Kiwi Go» in Onest Bold** match your site header lockup (case, weight, spacing), or do you have a wordmark file? | It goes on the card in every export | Onest Bold 128, as specified |
| Q-7 | What is the **maximum size or weight per «место»**? May the caption say «вес и размер цену не меняют»? | The weight claim must not be absolute | Caption omits the weight clause |
| Q-8 | Is it true that **Kiwi Go never asks for the code by phone**? If so, we add it to the caption (scam safety). | Scam-safety copy | Not added |
| Q-9 | Are the **courier look** (plain lime cap, ink jacket) and the **truck look** (ink cab, cream body, kiwi wheels like the site illustration) OK? Should any real uniform or vehicle colours be matched? | They fix the sheets | As specified in §2 |
| Q-10 | Will the **index page** be fixed? It says the recipient sees a tracking link, but the FAQ says there is no such page yet. | The ad drives traffic there | We flag it; the Reel stays seller-side |
| Q-11 | Music: who licenses the track, and at what tempo? (We cut at 120 BPM; 110–120 is fine.) | Re-conform planning | 120 BPM grid |
| Q-12 | Who is the **native proofreader** for the final Russian lines (§1.3, §1.4, §1.7)? | It is a sign-off before rendering | Internal proofread, flagged |
| Q-13 | Optional: do you want the extra **A/B hook heads** (H-B bus station, H-C flying box, H-D price)? They are not in this budget. | Budget only | Master only |

---

## Summary
- This is the single production source for the hybrid «Отправлено» on C1's spine: 20.0 s master (480 frames, 10 bars at 120 BPM) and 10.0 s cut-down, 24 fps, 6 AI shots plus a composited card.
- Every fix from 05 and 06 is applied: a city arrival, seller-side tracking only, «Вручаем / по коду получения», no yurt or tunduk, no «вес не важен», real labels only (no «Вручено»), and the logo born on the parked side-on truck's wheel by compositing at B8.1.
- The client decisions are filled in: «По всему / Кыргызстану» (a written confirmation is requested), «от 350 сом», CTA «Оформите доставку» + pill «kiwigo.kg» + «или напишите в WhatsApp», Russian only.
- Style: felt-toy miniature shot through a tilt-shift macro lens, with a verbatim STYLE ANCHOR, dignified characters, blank props and a flat-hub plain-wheel truck.
- Pipeline: sheets (Seedream 5.5) → GPT Image 2.6 high-2k start frames → Kling 3.0 Pro (S1, S2, S4, S5, S6) and Kling O3 FLF Pro (S3 crane).
- Every shot has a written prompt, acceptance tests and a fallback; S1, S4, S5 and S6 have 0-cr 2.5D fallbacks.
- Live quotes: K3P 7.5 / 6.0 / 4.5 cr for 5 / 4 / 3 s; FLF-P 6.25 cr for 5 s; GPT-hi 2.75; GPT-med ×2 2.0; Seedream 2k 3.5. Balance: **488.92 cr**.
- Gate 1 (sheets plus 7 style frames) costs 23.75 cr and needs client approval. Gate 2 (an S2 Pro motion test) costs 8.75 cr. Gate 3 (all remaining clips) costs 48.25 cr.
- **Total: base 80.75 cr; base plus retries 169.75 cr; max ceiling 208.75 cr.** That leaves ≥ 280 cr in reserve. Cinema Studio is used only with approval.
- Compositing: R1, R2 and R5 recipes, haze, glow, whip and focus-pull bridges, a homography-tracked lime light trail, a 2-point wheel track with the 2 px gate, and HTML/Playwright UI with Onest bundled locally.
- Export: H.264 High, 1080×1920, 24 fps, no audio, +faststart, plus beat-marker text files.
- Thirteen client questions are listed. The blockers are the written coverage sign-off, the style approval, the real app screenshots and labels, and the WhatsApp details.
