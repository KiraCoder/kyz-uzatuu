# 04 — Three concepts for the Kiwi Go hero Reel

Author role: creative director / scriptwriter. Written 2026-11-18.
Inputs: `CONTEXT.md`, `01-marketing-strategy.md`, `02-higgsfield-playbook.md`, `03-reels-craft.md`, reference contact sheets (`research/reference/sheet0.png`, `sheet1.png`) and old-film frames (`research/frames/old/`).
Nothing was generated and no credits were spent. All prices are the real quotes from the playbook.

The three concepts:

| | Concept | Engine | One line |
|---|---|---|---|
| **C1** | **«Вечер без автовокзала»** (seller story) | Pain → relief | The same seller and the same sofa, first in the cold «где посылка?» panic and then in warm calm, because Kiwi Go took the trip off her hands. |
| **C2** | **«Отправлено»** (parcel = message) | Magical realism | A parcel leaves the doorstep the way a message leaves a chat, crosses miniature Kyrgyzstan at night like a comet, and lands in a real courier's hands. |
| **C3** | **«Страна-диорама»** (Kyrgyzstan as a diorama) | Miniature journey | One toy truck crosses the whole country, built as a hand-made diorama, from a city door to a regional door. A yurt's crown turns into our logo. |

---

## 0. Shared production rules (they apply to all three concepts)

These rules keep the concept tables short. Each one closes a flaw from the critique in `03-reels-craft.md` §2; the table in §0.8 maps them.

### 0.1 Tempo grid, length and loop
- **The edit is cut on a 120 BPM grid.** One beat is 0.5 s, which is exactly **12 frames at 24 fps**, and one bar (4/4) is 2.0 s. Bar *n* starts at 2·(n−1) s, so downbeats fall on even seconds. "B8.1" means bar 8, beat 1, which is 14.0 s.
- **Master = 20.0 s = 10 bars** for every concept, so A/B tests are fair. **Cut-down = 10.0 s = 5 bars.**
- **Fitting a 110–120 BPM track:** the music editor either time-stretches the track to 120 BPM (a change of 8 % or less is inaudible on a bed), or we re-conform the edit by multiplying every timecode by 120/BPM. At 115 BPM the master becomes 20.9 s; at 110 BPM it becomes 21.8 s. Both stay inside the 18–22 s brief, which is why the master is 20.0 s and not 22.
- **Music shape** (copied from the reference): groove → **swell** on the big camera move → a short **breath** (one beat) → **PEAK** on the cut to the end card → resolve under the CTA. Beat points are marked in every table: HIT, swell, breath, PEAK, loop.
- **Loop (R7 → R1):** there is no black tail. The end card dissolves into a cream #F6F1E4 fog over the last 10 frames (19.6–20.0 s). Frame 0 opens under the same fog at **40 % opacity**, which lifts to 0 by 0.75 s, so the hook picture is readable on frame 0. The music bed loops on the bar line.
- **Picture pipeline:** 24 fps from source to export, no 24→30 resampling, and fewer than 2 % duplicate frames (checked with the frame-difference script). 1080×1920, H.264 High, `+faststart`.

### 0.2 Look and grade
- Every start frame uses the **style anchor from playbook §4, word for word**, plus "no text, no letters, no signage, no logos, blank panels".
- **R6 on every clip:** lifted blacks, saturation 0.85, cream highlight roll-off, bloom, 2–3 % grain, and tilt-shift reinforcement when the plate is too sharp.
- **One LUT family.** Each concept has one deliberate time-of-day arc that follows its story. Saturation falls toward the brand moment, so the lime of the logo is the most saturated thing on screen when it lands.
- Logos and text are composited **after** the grade. Flares and bloom go **over** the logo.

### 0.3 Type and safe zones (1080×1920)
- **Font: Onest** (the site font), in two weights only: SemiBold for supers and UI, Bold for the wordmark and price.
- **Super style:** Onest SemiBold 72 px, ink #111410 on a cream #F6F1E4 pill at 92 % opacity, corner radius 28, a 14 px lime #B8F03C dot on the left. Supers **cut in on the beat** with no fade-in; they leave with a 4-frame fade. Hold time is at least 0.4 s per word and never less than 1.2 s.
- **Positions.** All text sits inside **x 80–900** (clear of the right-hand action column) and **y 270–1250**. The centre line is x = 490.
  - **P-HOOK:** pill centred at y 660, the top of the key band. It survives a 4:5 crop.
  - **P-LOW:** pill centred at y 1100, the bottom of the key band, above the Instagram UI.
  - **P-HIGH:** pill centred at y 380. Used only when the subject fills the key band. It also survives a 4:5 crop (285–1635).
- **Status UI (seller-side only).** Composited chips read «Забрали» → «В пути» → «В городе» → «У курьера» → «Вручено». The active chip is lime with ink text; past chips are cream with a ✓. Chips **always live inside a seller's device or a seller's app panel**: on her phone screen, in a mini-phone picture-in-picture (**PiP**) at top-left x 80–330, y 300–720 that reads as "her phone", or in an app card headed «Kiwi Go для магазинов». The film never implies that the recipient sees tracking.
- **Copy rules:** no city names, no delivery times («завтра», «за ночь», «до обеда»), no «Скоро», no competitors, no salaries or strategy. The price is always written «от 350 сом», with a non-breaking space before «сом». The SMS code is always framed as given to the courier on handover («Вручаем по коду из SMS»), because of the current SMS-code scams.

### 0.4 Coverage line: both variants, the client picks
The client asked for **A «по всему Кыргызстану»**. The strategist warns that it is not door-to-door everywhere and recommends **B «между городами Кыргызстана»**. Every concept carries both versions of the same super in the same position and length. They are rendered as two exports (`_covA`, `_covB`), so choosing one costs no credits.

### 0.5 The logo
- The logo is always the exact file `kiwi-go-soon/logo/kiwi-go-logo.svg`, rendered at 2× and downsampled. It is **never** AI-drawn, recoloured, given 3D, spun or glowed.
- It enters on a beat with **scale 0.92 → 1.0 and opacity 0 → 1 over 6 frames** (easeOutBack, overshoot of 5 % at most).
- It is integrated by layer order: a scene tint (multiply at 8–10 %), a soft scene-coloured haze, and the flare and bloom on top.
- **Wheels in AI footage are always plain** (ink tyre, cream hub). Kiwi-slice wheels are composited by us only where the feasibility gate in §0.6 passes.

### 0.6 Kiwi-wheel feasibility gate (for composited kiwi wheels)
We composite our SVG onto a truck wheel only if all of these hold:
- the truck is strictly side-on;
- the wheel is at least 70 px in diameter on the plate;
- the camera is locked or moves laterally;
- a 2-point track (hub plus a rim point) holds within 2 px.

A parked truck takes static wheels. A rolling truck gets rotation = distance travelled ÷ radius, computed from the hub track. If any test fails, the wheels stay plain. This is never an AI job.

### 0.7 Shared end card (concept-specific lines are in each concept)
- Paper #FFFDF7, a 4 % cream radial vignette and 2 % grain. It is entered through a **R5 flash match-cut**: 3 frames of #FFFDF7 peak, and the logo keeps the exact x/y it had in the world.

| Element | Spec | Position (centre / baseline) | In at |
|---|---|---|---|
| Logo icon | exact SVG, Ø 280 px | starts at its in-world position, then eases to (490, 520) over 0.35 s | 16.00 (PEAK B9.1) |
| Wordmark «Kiwi Go» | Onest Bold 128 px, ink; type-on through a mask over a pre-rendered **centred** line, 0.07 s per glyph | baseline y 790 | 16.25–16.75 |
| Descriptor | Onest SemiBold 46 px, green ink #3F6212 (concept-specific) | baseline y 860 | 16.90 (fade + 12 px rise) |
| Price | «от 350 сом», Onest Bold 104 px, ink, 8 px lime underline under «350» | baseline y 990 | 17.00 (B9.3) |
| Price note | «цена за место», Onest SemiBold 40 px, ink at 70 % | baseline y 1045 | 17.00 |
| CTA verb | Onest SemiBold 48 px, ink (concept-specific) | baseline y 1115 | 17.50 (B9.4) |
| CTA pill | lime #B8F03C pill 680×104, radius 52; text «app.kiwigo.kg» Onest SemiBold 60 px, ink | centre y 1190 (spans 1138–1242) | 17.50 |
| Loop fog | cream #F6F1E4 to 40 %, matching frame 0 | full frame | 19.60–20.00 |

- The CTA is held for 2.1 s (more than the 1.5 s minimum). Everything sits inside y 270–1250 and x 100–880. Nothing is grey and nothing goes to black.
- **Caption and ad button** repeat the CTA: «Ссылка в профиле — оформите первую доставку». Use the «Подробнее» button → app.kiwigo.kg with UTM per concept and hook, or the WhatsApp «Отправить сообщение» button for private senders.

### 0.8 How the concepts avoid every flaw of the old film

| # | Old-film flaw (03 §2) | What all three concepts do instead |
|---|---|---|
| 1 | White frame 0, no hook | A subject is moving on frame 0 under a 40 % fog only. A hook super is on screen from frame 0. Each hook is a pain, an impossibility or a direct question. |
| 2 | Three unrelated postcards | One protagonist (a seller, a parcel or a truck) and one A → B journey from a sender's door to a recipient's door. |
| 3 | No benefit | Three to four proof supers, each a public fact: pickup at the door, seller-side tracking, the SMS code on handover, price per place, «от 350 сом». |
| 4 | No CTA | A lime CTA pill with app.kiwigo.kg, held 2.1 s, repeated in the caption and the ad button. |
| 5 | A lone AI kiwi tyre | No AI-drawn kiwi anything. Plain wheels; kiwi wheels only through the §0.6 gate. |
| 6 | Falling energy, static postcards | Every shot has a motivated move. Something new arrives every 1.5–2.5 s. The camera speed peaks at the swell before the logo. |
| 7 | 24→30 fps judder | A 24 fps pipeline end to end, with a duplicate-frame check. |
| 8 | Ghosting cross-dissolve | **Zero dissolves between unrelated shots.** Every cut is hidden in light (R2, a glow flash), in motion (a whip, a crane, a chained frame), in occlusion (a cloud, a tree, a light streak) or in a match cut. |
| 9 | Three lighting worlds, over-saturated, too sharp | One LUT family with one story-motivated time-of-day arc. R6 grade, saturation falling toward the logo, tilt-shift falloff. |
| 10 | Spinning sticker logo | The logo is born inside the world on a real object or a calm sky. It is screen- or plane-locked with no spin, sits under the flare, and match-cuts into the card. |
| 11 | Inter, weak hierarchy, grey fade | Onest. Hierarchy of logo → name → descriptor → price → CTA pill. The card ends in cream fog, never grey. |
| 12 | No tempo plan | A 120 BPM grid with a beat column in every table. |
| 13 | Black tail | A cream-fog loop that matches frame 0. |
| 14 | AI drawing brand elements | AI plates hold no brand marks, letters or UI. Everything branded is ours. |

### 0.9 Abbreviations used in the "AI method" column
- **GPT-hi** = `gpt_image_2_6`, quality high, 2k, 9:16 (2.75 cr).
- **K3P** = `kling3_0`, `mode:"pro"`, `sound:"off"`, start frame, 5 s (7.5 cr).
- **FLF-P** = `kling_o3_flf`, pro, start + end frame (6.25 cr for 5 s, 12.5 for 10 s).
- **FLF-S** = the same model on std, used for motion tests (5 cr for 5 s, 10 for 10 s).
- **Sheet** = the `character-sheet` workflow, Classic 3D, `seedream_5_5` 2K (3.5 cr).

Motion prompts follow playbook §3.2: what moves → one camera verb → end state → "all surfaces stay blank, no text, no morphing".

---

# C1 — «Вечер без автовокзала» (seller story: pain → relief)

## C1.1 Overview
**The idea in one line:** we see the same seller on the same sofa twice. First she is drowning in «где посылка?» at night. Then, after one doorstep handover to a Kiwi Go courier, she is watching her parcels move on her phone with a cup of tea.

**Single-minded proposition:** «Отправить посылку — как написать сообщение». Here it is shown as the relief of not making the trip.

**Proof points:** «Заберём у двери» · «Видно каждый шаг» (on her phone) · «Вручаем по коду из SMS» · «от 350 сом», «цена за место».

**CTA:** «Подключите магазин» → app.kiwigo.kg. This is the seller-targeted cut; the private-sender CTA in §C1.4 is an export variant.

**Why it stops the scroll:** frame 0 is the strategist's #1 hook. Native-looking DM bubbles pop over a tiny, tired seller, and every Instagram seller has lived that moment («это же я»). The miniature look makes the pain charming, not whiny.

**Why it sells:** it is the only concept where the viewer *is* the protagonist. The before and after on the same sofa is the clearest possible demonstration that the problem is solved. All four proof points are shown in action, not read off a list. Its share driver is built in: sellers send it to seller friends.

## C1.2 Shot-by-shot script (master 20.0 s)

**Time-of-day arc:** cold blue night and blue dawn for the pain (S1–S2). The R2 leak flips the grade warm. Then warm evening (S3–S4), dusk road cranes into golden morning (S5), and golden morning arrival (S6–S7). It is one LUT family whose temperature curve follows the story.

| # | TC (s) / bars | Picture: what we SEE | AI method | Transition IN / OUT | Super (RU), position | Our composite | Beat |
|---|---|---|---|---|---|---|---|
| S1 | 0.00–2.50 · B1.1–B2.2 | **HOOK.** Tilt-shift miniature living room at night. A toy seller (Classic 3D, woman about 30, cream cardigan, hair bun) sits small on a sofa among stacks of blank cream parcels. Her phone throws cold blue light on her face; warm city bokeh is in the window. Macro-lens look with a narrow sharp band through her and soft top and bottom. **Camera:** a slow push-in that is already moving on frame 0. She lowers the phone a little and exhales; her shoulders sink. | Seller **Sheet** → GPT-hi start (an edit with the sheet as `image_references`) → **K3P** 5 s; use 0–2.5 s. Motion prompt: "She lowers the phone slightly and exhales, shoulders sinking; phone light flickers on her face; very slow push in. All surfaces blank, no text." | IN: **R1** fog-lift from the loop (40 % → 0 by 0.75 s). OUT: **glow cut**. The push ends into the phone glow; a 3-frame cold-white bloom flash, and the cut sits on the white peak. | «Где моя посылка?» at **P-HOOK**, from frame 0 to 2.40 | Four DM bubbles pop around her head (x 120–860, y 330–600), each a scale-pop of 6 frames: «где посылка?» 0.00, «уже отправили?» 0.50, «а когда будет?» 1.00, «??» 1.50. They are neutral grey and white, in our own style, with no real messenger's colours or icons. | Bubble pops on beats B1.1–B1.4. Soft, sparse groove. |
| S2 | 2.50–4.00 · B2.2–B3.1 | **Pain, escalated.** Miniature intercity bus yard at blue dawn: rows of **unbranded** white minibuses with blank windscreens and no route boards. Headlights are on. A tiny seller with a box looks left and right. **Camera:** a push-in from wide to medium-wide, with headlight flares in the foreground. | GPT-hi start (the seller from the sheet, small in frame) → **K3P** 5 s; use 1.5 s. "The tiny woman turns her head left then right holding the box; headlights glare; slow push in. All vehicles stay blank, no lettering." | IN: glow cut (opens on a headlight flare that matches the phone glow). OUT: **R2 orange light leak**, 3.75–4.50, with the cut at the peak, 4.00. This is the "turn". | «Опять на автовокзал?» at **P-HIGH** (the minibuses fill the key band), 2.50–3.90 | Light leak R2, procedural or stock, with a warm-lime fringe. | **HIT B3.1 (4.0 s): the turn.** Riser 3.0 → 4.0. |
| S3 | 4.00–6.50 · B3.1–B4.2 | **Relief begins.** Warm evening at the seller's apartment door (a miniature stairwell landing with a lamp and a cream door). The **courier** (Classic 3D, ink jacket, **lime cap**, back three-quarters to camera) already holds the parcel, which has a **blank round cream sticker** on the tape. The seller lets go, smiles and leans on the door frame. The courier turns and walks out of frame to the right. **Camera:** locked medium shot that ends with a **whip-pan right** following him. | Seller + courier **Sheets** and the parcel still → GPT-hi start, with the box **already in the courier's hands** on frame 0 → **FLF-S** motion test 5 s → **K3P** 5 s final; use 2.5 s. "She releases the parcel and smiles; the courier turns and walks right; at the end the camera whip-pans right with motion blur. Hands stay still on the box, no extra fingers, surfaces blank." | IN: R2 leak (warm). OUT: **whip-pan right** with a composited 4-frame directional-blur bridge. | «Заберём у двери» at **P-LOW**, 4.25–6.25 | The first lime brand cue is the cap, which is in the AI plate as a colour only. | Music opens up. B3.3 (5.0 s): the courier turns. |
| S4 | 6.50–9.00 · B4.2–B5.3 | **Relief.** The same living room, now warm: a lamp is on and the parcels are gone. In the soft background the seller leans back on the sofa holding tea (a micro-motion sip). Sharp in the foreground: **her phone, lying on the sofa armrest, with a matte chroma-green #00B140 screen.** No hands touch the phone. **Camera:** a whip-pan lands on it, then a very slow push-in. | GPT-hi start (edited from the S1 room still, same layout) → **K3P** 5 s; use 2.5 s. "She sips tea and relaxes in the soft background; very slow push in toward the phone; the phone and its green screen stay perfectly still and flat." | IN: whip-pan landing (the blur bridge). OUT: a **zoom through the screen**: our 2D push scales the phone screen up to fill the frame under a soft lime-white flash of 4 frames, and S5 starts behind it. | «Видно каждый шаг» at **P-HIGH**, 6.75–8.75 | **Phone UI** (4-corner planar track): an app screen headed «Kiwi Go для магазинов» with an order card and chips. «Забрали ✓» appears at 7.00, then «В пути» goes lime at 8.00. After S4 the same UI shrinks into the **PiP** mini-phone at top-left and stays through S6. | Chips land on B4.3 (7.0) and **B5.1 (8.0)**. |
| S5 | 9.00–11.50 · B5.3–B6.4 | **Journey.** A miniature mountain road at dusk. A small **unbranded** cream-and-ink box truck with plain wheels and blank panels winds up the switchbacks, its headlights on. **Camera:** follows, then **cranes up over the ridge**, rising through a thin cloud layer into golden morning light over a regional valley town. | GPT-hi **end frame first** (a golden valley town seen through thinning cloud), then the **start frame** as an edit of it (the dusk road, same horizon and sun side) → **FLF-S** test → **FLF-P** 5 s; use 2.5 s with an ease-in ramp. "The truck climbs the switchback; the camera follows, then cranes up over the ridge through a soft cloud layer into golden morning, ending exactly on the last frame. One continuous move, no cuts." | IN: zoom through the screen. OUT: **cloud wipe**. The cut sits inside the uniform cloud texture (R3), and S6 opens from soft morning haze. | «Без автовокзала и звонков» at **P-LOW**, 9.25–11.25 | PiP: «В городе» goes lime at 11.00. No kiwi wheels: the truck is too small and moving, so it fails the §0.6 gate. | **Swell 10.0–11.5** (B6.1) on the crane. |
| S6 | 11.50–13.50 · B6.4–B7.4 | **Arrival.** Golden morning at the door of a miniature regional house (a courtyard, an apricot tree, a blue gate). The recipient (Classic 3D, an older woman in a headscarf, three-quarter view) receives the parcel from the courier, whose back is to camera. Frame 0 is mid-handover with both holding the box. Motion: the courier releases it, she draws it to her chest and smiles. **Camera:** a slow push-in that ends on the box. | Courier **Sheet** + parcel still → GPT-hi start → **FLF-S** test → **K3P** 5 s; use 2 s. "The courier releases the parcel; the woman draws it to her chest and smiles warmly; slow push in toward the parcel. Hands stay on the box, no extra fingers, surfaces blank." | IN: emerges from the cloud haze (a short fog-lift). OUT: **match cut on the box** (same sticker position, same push direction) into S7. | «Вручаем по коду из SMS» at **P-HIGH**, 11.50–13.50 | PiP: «У курьера» at 12.00, then «Вручено ✓» at 13.00. The PiP shrinks away at 13.4. | Warm resolve. B7.1 and B7.3 chips. **Breath 13.5–14.0.** |
| S7 | 13.50–16.00 · B7.4–B9.1 | **Logo born in the world.** Macro: the same parcel now rests on her wooden table in golden window light. The **blank round cream sticker** on the tape is centred at about (490, 800). **Camera:** a very slow push-in toward the sticker. | GPT-hi start (an edit of the parcel still, same sticker) → **K3P** 5 s; use 2.5 s. "Very slow push in toward the round sticker; dust motes drift in the window light; the box stays perfectly still." | IN: match cut. OUT: **R5** flash match-cut to the card. | none (a clean brand moment) | **Our logo** is planar-tracked onto the sticker (§C1.3). The light sweep goes over it at 15.5. | **HIT B8.1 (14.0): logo lands.** Flare at 15.5. **PEAK B9.1 (16.0): flash cut.** |
| Card | 16.00–20.00 · B9.1–B10.4 | End card (§0.7 and §C1.4). | none | IN: R5 flash plus the logo match. OUT: **R7** cream fog → loop to S1. | see §C1.4 | full card | Resolve. CTA at B9.4. Loop on B10.4 → B1.1. |

**Cut-down (10.0 s, five bars):**
1. S1 hook, 0.0–2.0 («Где моя посылка?», three bubbles).
2. S3 doorstep, 2.0–4.0 («Заберём у двери»).
3. S4 phone, 4.0–6.0 («Видно каждый шаг», chips at 4.5 and 5.0).
4. S7 sticker, 6.0–7.0, with the logo landing at B4.1 (6.0).
5. Card, 7.0–10.0: the flash on 7.0 (B4.3), price at 7.5, CTA at 8.0, fog loop from 9.6.

The bus yard, the journey and the arrival are dropped. The pain → relief contrast survives because S1 and S4 are the same room.

**Hook test heads (optional, +10.25 cr each):** Hook 2 («Опять на автовокзал?», S2 extended to 0–2 s) and Hook 3 (C2's lifting parcel). They are swapped onto the same body for the 48–72 h hold-rate test.

## C1.3 Logo and brand moment
1. **Brand cues before the logo:** the courier's lime cap (S3, at 4 s), the lime active chip (S4), and the lime-fringed light leak.
2. **In the world (S7, 14.0 s):** the AI plate holds a **blank round cream sticker** sealing the parcel's tape. That sticker is the parcel's identity from S3 onward. We 4-corner planar-track the sticker during the slow push. On B8.1 our SVG appears **inside the sticker's ellipse**: scale 0.92 → 1.0 and opacity over 6 frames, then plane-locked so it follows the push.
3. **Integration:** a luminance-matched shading pass (the plate's light gradient multiplied at 10 %), 2 % paper grain, and the window-light sweep and bloom composited **over** it at 15.5. It reads as "this parcel was a Kiwi Go parcel all along".
4. **Resolve to the card (R5):** a 3-frame cream flash at 16.0. The icon keeps its x/y (490, 800) and its size, then eases to (490, 520) as the wordmark types on below. That is a match cut on the logo.
5. **Wheels:** the S5 truck keeps plain wheels; the gate fails (too small and moving). No kiwi wheels in C1.

## C1.4 End card copy (Onest)
- Logo → **«Kiwi Go»**
- Descriptor (coverage, the client picks): **A «Посылки по всему Кыргызстану»** / **B «Посылки между городами Кыргызстана»**
- **«от 350 сом»** + «цена за место»
- CTA verb: **«Подключите магазин»** (seller cut). For the private-sender export: «Оформите доставку».
- Pill: **«app.kiwigo.kg»**

## C1.5 Risks and mitigation

| Risk | Where | Mitigation |
|---|---|---|
| Face drift or uncanny seller | S1, S3, S4 | Classic 3D toy style from one approved **Sheet**. Every start frame is an edit from the sheet. Micro-motion only (an exhale, a smile, a sip). Faces are never in close-up; S4 keeps her soft in the background. |
| Hands and extra fingers in the two handovers | S3, S6 | Frame 0 is **mid-handover with both people already gripping the box**, and the only motion is a release. Test on FLF-S (5 cr) before the Pro run. Fallback: `seedance_2_0` fast 720p with the sheets as refs (12.5). Last resort: re-stage so the box is already with the receiver and the action is just a smile. |
| Phone screen grows fake UI or glare | S4 | A matte chroma-green screen in the still, the phone lying flat on the armrest (no hand on it), angled away from the lamp, and a near-locked camera. If keying fails, track 4 corners and replace the whole screen area. |
| Gibberish on minibuses (route boards, plates) | S2 | "Blank windscreens, no route boards, no plates" in the still. Dawn backlight turns the buses into silhouettes, plus strong tilt-shift blur. Check at 100 % and paint out from a clean plate. |
| DM bubbles look like a real messenger brand | S1 | Our own neutral bubble style; no WhatsApp, Telegram or Instagram colours or icons. |
| Parcel and sticker inconsistency across S3, S6, S7 | S3, S6, S7 | One approved **parcel still** (cream box, lime-free tape, blank round sticker) as `image_references` in all three start frames. The logo only goes on the S7 sticker. |
| Two worlds (cold vs warm) | grade | One LUT, with only the temperature and exposure curves keyed to the story; the R2 leak motivates the flip. The cream highlight is identical in both halves. |
| Crane melts the road into cloud | S5 | The end frame is generated first and the start frame is edited from it (same horizon and sun). An explicit path in the prompt. The cut is hidden inside the cloud. Fallback: `kling4_0` 720p with one middle keyframe (11.25). |
| Seven shots feel choppy | edit | Every cut is hidden (glow, leak, whip, zoom-through, cloud, match cut, flash). Average shot length is 2.3 s, which suits a story Reel. |

## C1.6 Budget (Higgsfield credits)

| Line | Qty | Unit | Credits |
|---|---|---|---|
| Character sheets (seller, courier) | 2 | 3.5 | 7.0 |
| Parcel object still (blank round sticker) | 1 | 2.75 | 2.75 |
| Exploration stills (7 shots × 2 at 0.25 + 2 at 1.0) | 28 | — | 17.5 |
| Final start frames, 7 + 1 redo each | 14 | 2.75 | 38.5 |
| End frame for S5, plus a redo | 2 | 2.75 | 5.5 |
| Motion tests on FLF-S (S3, S5, S6) | 3 | 5 | 15.0 |
| Finals: K3P × 6 (S1, S2, S3, S4, S6, S7) | 6 | 7.5 | 45.0 |
| Final: FLF-P 5 s (S5) | 1 | 6.25 | 6.25 |
| Retries: S1, S3, S4, S6 at 1.5 each (6 × 7.5) | 6 | 7.5 | 45.0 |
| Retries: S2 and S7 at 0.5 each (1 × 7.5); S5 × 1 (6.25) | — | — | 13.75 |
| **Subtotal** | | | **196.25** |
| Contingency: 2 handovers on `seedance_2_0` fast 720p | 2 | 12.5 | 25.0 |
| **Total with contingency** | | | **≈ 221** (about 268 of 489 left) |
| Optional hook test heads | 2 | 10.25 | +20.5 |

---

# C2 — «Отправлено» (parcel = message, magical realism)

## C2.1 Overview
**The idea in one line:** a seller sends a parcel the way she sends a message. It lifts off her doorstep, flies across a sleeping miniature Kyrgyzstan as a streak of light, and lands in the hands of a real Kiwi Go courier at the other door. Magic on the outside, a real service inside.

**Single-minded proposition:** «Отправить посылку — как сообщение», stated literally in the first 2.5 s and then shown.

**Proof points:** «Заберём у двери» · the coverage line (A/B) · «Видно каждый шаг» (her phone and the PiP) · «Вручаем по коду из SMS» · «от 350 сом».

**CTA:** «Оформите доставку» → app.kiwigo.kg.

**Why it stops the scroll:** a box floating off a doorstep in frame 0 is an impossible image («как она полетела?»). It is a curiosity gap, the strategist's Hook 3, and it is completed by a two-part super that lands the proposition on the second beat.

**Why it sells:** it is the most **brand-ownable** idea. The company's own positioning becomes the film's physics. It is closest in spirit to the reference (one object's journey, a crane into clouds, the logo in the sky). The courier reveal at the end grounds the magic in a real, reliable service.

## C2.2 Shot-by-shot script (master 20.0 s)

**Time-of-day arc:** blue dusk sending (S1–S2) → night flight (S3) → golden dawn arrival (S4) → golden clouds (S5). The parcel's light trail is our composite, lime-white with a cream core, and it carries the brand colour through the night.

| # | TC (s) / bars | Picture: what we SEE | AI method | Transition IN / OUT | Super (RU), position | Our composite | Beat |
|---|---|---|---|---|---|---|---|
| S1 | 0.00–2.50 · B1.1–B2.2 | **HOOK.** Blue-dusk miniature porch of a city apartment block: a cream door, warm lamp, potted geranium. The seller (Classic 3D, seen from behind and slightly to the side) stands in the doorway holding her phone at chest height. On the step a **cream parcel is already 2 cm off the ground on frame 0, rising slowly and perfectly level**. **Camera:** tilts up to follow it as it rises out of the top of frame. | Seller **Sheet** + parcel still → GPT-hi start → **FLF-S** test → **K3P** 5 s; use 2.5 s. "The cardboard parcel floats straight up, slowly, rigid, perfectly level, no wobble; the camera tilts up following it; the woman stays still watching. Box shape never changes, no strings, no hands, surfaces blank." | IN: **R1** loop fog (40 % → 0). OUT: **streak cut**. The parcel exits the top of frame and its light trail flares upward for 4 frames; the cut sits on the flare. | Line 1 «Отправить посылку…» at **P-LOW**, from frame 0. At 1.00 s (B1.3) line 2 «…как сообщение» cuts in under it (a two-line pill). Both hold to 2.40. | **Light trail** under and behind the parcel: a lime-white glow, tracked to the box, made with additive blobs and a motion-blurred tail. The glow also lights the porch floor in a screen pass. | HIT on frame 0. **Line 2 lands on B1.3 (1.0) → hold.** |
| S2 | 2.50–4.00 · B2.2–B3.1 | Over-the-shoulder macro of **her phone** in her hand: a matte chroma-green screen, her thumb resting at the lower edge and lifting after a tap. The porch lamp and the sky behind are soft. **Camera:** near-locked, a very slow push. | GPT-hi start (sheet-edited hand and phone) → **K3P** 5 s; use 1.5 s. "Her thumb lifts slightly off the screen edge; very slow push in; the phone and its green screen stay still and flat." | IN: streak cut (the upward motion matches the bubble flying up on screen). OUT: **R2 orange-lime light leak**, 3.75–4.50, cut at 4.00. | «Заберём у двери» at **P-HIGH**, 2.50–3.90 | **Phone UI** (4-corner track), styled like a chat: a parcel photo "message" bubble flies up with the ticks «Отправлено ✓»; under it the chip «Забрали ✓» appears at 3.0. The UI then shrinks into the **PiP**. | Bubble send on B2.3 (2.5). **HIT B3.1 (4.0): leak.** |
| S3 | 4.00–8.00 · B3.1–B5.1 | **Night flight.** A miniature night landscape seen from the air: a snow-capped felt-textured ridge, a river, a yurt camp with a tiny warm fire, village lights strung along a road. **Camera:** a slow forward drone drift with a gentle descent. **The AI plate has no parcel.** | GPT-hi start → **K3P** 5 s; use 4 s. "Slow forward drone drift with gentle descent over the miniature night valley; lights twinkle softly; no objects fly; buildings stay rigid." | IN: R2 leak. OUT: **light-streak whip**: our comet crosses the lens diagonally and fills the frame for 6 frames; the cut sits inside it at 8.00. | Coverage, **A «По всему Кыргызстану»** / **B «Между городами Кыргызстана»**, at **P-HIGH**, 4.25–6.00. Then «Видно каждый шаг» at **P-HIGH**, 6.00–7.90. | **Comet parcel**: a 2.5D sprite of the approved parcel still (background removed locally, lit by a gradient), moving on a bezier path across the valley with the lime-white trail. **PiP**: «В пути» goes lime at 5.00. | Groove. Chip on B3.3. Second super on B4.1 (6.0). **Whip on B5.1 (8.0).** |
| S4 | 8.00–11.50 · B5.1–B6.4 | **Arrival, golden dawn.** A miniature regional courtyard: blue gate, apricot tree, a recipient's door. The **courier** (lime cap, ink jacket, seen from behind) is holding the parcel at chest height on frame 0. Our composite glow is just fading off the box, as if it has just landed. The recipient (an older man in a kalpak, three-quarter view) takes the box and nods with a smile. **Camera:** slow push-in. | Courier **Sheet** + parcel still → GPT-hi start, with frame 0 mid-handover → **FLF-S** test → **K3P** 5 s; use 3.5 s. "The courier holds the parcel out; the man takes it with both hands and nods, smiling; slow push in. Hands stay on the box, no extra fingers, surfaces blank." | IN: inside the light streak; the glow lands on the box. OUT: **chained frame**. S5's start image is S4's last frame, so the cut is invisible. | «Вручаем по коду из SMS» at **P-HIGH**, 9.00–11.00 | The glow decays off the box 8.00–8.50, our composite. **PiP**: «В городе» at 8.50, «Вручено ✓✓» at 11.00, then the PiP shrinks away at 11.4. | Warm resolve. B5.2, B6.3 chips. |
| S5 | 11.50–16.00 · B6.4–B9.1 | **Crane into the sky.** The same courtyard. The camera **cranes up** past the apricot tree and rooftops, rises through a layer of golden cumulus, and ends in calm golden sky with a **clear zone in the upper centre**. As the camera rises, a last lime-white spark (ours) lifts off the box and climbs with it. | GPT-hi **end frame first** (calm golden cloud sky with a clear zone at the upper centre) → start = S4's last frame (chained) → **FLF-S** test → **FLF-P** 5 s; use 4.5 s with an ease-in-out ramp. "One continuous crane up from the courtyard past rooftops, through soft golden clouds into open sky, slow ease-in and ease-out, ending exactly on the last frame." | IN: chained frame. OUT: **R4 → R5** (the logo in the sky, then a flash match-cut). | none (a clean brand moment) | The spark rises into the clear zone and becomes the **logo** at B8.1 (§C2.3). A flare from the top edge goes **over** the logo at 15.5. | **Swell 12.0–13.5** (B7.1). **Breath 13.5–14.0.** **HIT B8.1 (14.0): logo.** **PEAK B9.1 (16.0): flash cut.** |
| Card | 16.00–20.00 | End card (§0.7 and §C2.4). | none | IN: R5. OUT: R7 → loop to S1. | see §C2.4 | full card | Resolve. Loop on the bar. |

**Cut-down (10.0 s):**
1. S1 hook, 0.0–2.5 (the two-line super).
2. S3 night flight, 2.5–5.0 (coverage super A/B, PiP «В пути»).
3. S5 crane, 5.0–7.0, with the logo at B4.1 (6.0).
4. Card, 7.0–10.0.

The phone shot and the arrival are dropped. The PiP still shows seller-side tracking during the flight.

## C2.3 Logo and brand moment
1. **Brand cues before the logo:** the lime-white trail from frame 0 (a brand colour moving on screen in the first second), the courier's lime cap, and the lime chips.
2. **In the world (S5, 14.0 s), R4:** the AI end frame contains an empty, calm sky zone at the upper centre. Our composite spark (the last piece of the parcel's trail) rises into it and swells into a soft cream disc. On B8.1 the disc resolves into our logo: a crossfade within the same circle over 6 frames, scale 0.92 → 1.0, centred at (490, 800), 400 px wide.
3. **Integration:** the logo is screen-locked and the clouds keep drifting under it (motion contrast). It gets a sky-coloured haze, no glow halo, and a cloud wisp luma-keyed from the plate **in front of** its lower edge. The flare at 15.5 washes over it. **No spin.**
4. **Resolve (R5):** a flash at 16.0. The icon keeps (490, 800), then eases to (490, 520) as the wordmark types on.
5. **Wheels:** there is no truck in C2, so kiwi wheels do not apply. The brand "wheel" is the logo itself.

## C2.4 End card copy (Onest)
- Logo → **«Kiwi Go»**
- Descriptor (the proposition): **«Посылка — как сообщение»**
- **«от 350 сом»** + «цена за место»
- CTA verb: **«Оформите доставку»** (the seller export: «Подключите магазин»)
- Pill: **«app.kiwigo.kg»**
- The coverage line A/B already appears in S3. If the client wants it on the card as well, it replaces the price note in 40 px: «по всему Кыргызстану» (A) or «между городами Кыргызстана» (B).

## C2.5 Risks and mitigation

| Risk | Where | Mitigation |
|---|---|---|
| A levitating box deforms, wobbles or grows strings or hands | S1 | Rigid-body wording; the box is already floating on frame 0 (so there is no "lift-off" physics to invent); an FLF-S test. **Fallback, which costs no credits:** generate the porch plate *without* the box and composite our 2.5D parcel sprite rising, with a tracked tilt. Second fallback: `cinematic_studio_video_v2` pro with `speedramp:"slowmo"` (7.5). |
| "Is this a drone? Magic?" (the service is unclear) | concept | The supers carry the facts («Заберём у двери», «Вручаем по коду из SMS»). S4 shows a **real courier** handing it over. The PiP shows ordinary seller-side statuses. The card states the price and CTA. Test with one muted viewer: "what is it, how much, how do I start?" |
| Phone and thumb artefacts | S2 | The thumb rests at the screen edge with a micro-lift only; Classic 3D hand; matte green screen; 4-corner replacement fallback. |
| Hands in the handover | S4 | Frame 0 is mid-handover with both people already holding the box; an FLF-S test; fallback `seedance_2_0` fast 720p with the sheet (12.5). |
| Buildings or yurts warp in the night aerial; fake lights become letters | S3 | One slow drift, no orbit, a static busy still, and lights kept as bokeh points. The parcel is **not** in the AI plate, so it cannot melt. |
| Crane melts the courtyard into cloud | S5 | Chained start, an end frame generated first, an explicit path, 5 s. Fallback: `kling4_0` 720p with a middle keyframe of the rooftops (11.25). |
| The logo-in-sky reads as a "sticker" (the old film's sin) | S5 | Spark → logo continuity, a cloud wisp in front, flare over the logo, screen lock, no spin, no halo. |
| Night grade too dark for the feed | S3 | Lifted blacks (R6), blue-hour rather than black night, with the trail as the brightest element. |

## C2.6 Budget (Higgsfield credits)

| Line | Qty | Unit | Credits |
|---|---|---|---|
| Character sheets (seller, courier) | 2 | 3.5 | 7.0 |
| Parcel object still | 1 | 2.75 | 2.75 |
| Exploration stills (5 shots × 2.5 cr) | 20 | — | 12.5 |
| Final start frames, 5 + 1 redo each | 10 | 2.75 | 27.5 |
| End frame for S5 (the cloud zone), plus a redo | 2 | 2.75 | 5.5 |
| Motion tests on FLF-S (S1 float, S4 handover) | 2 | 5 | 10.0 |
| Finals: K3P × 4 (S1–S4) | 4 | 7.5 | 30.0 |
| Final: FLF-P 5 s (S5) | 1 | 6.25 | 6.25 |
| Retries: S1 × 2 (15), S4 × 1.5 (11.25), S2 × 1 (7.5), S3 × 0.5 (3.75), S5 × 1 (6.25) | — | — | 43.75 |
| **Subtotal** | | | **145.25** |
| Contingency: S1 on `cinematic_studio_video_v2` pro × 2 (15) + S4 on `seedance_2_0` fast (12.5) | — | — | 27.5 |
| **Total with contingency** | | | **≈ 173** (about 316 of 489 left) |

Removing the parcel's background for the sprite is done locally in Python (for example with rembg). It does not use Higgsfield's paid tool.

---

# C3 — «Страна-диорама» (Kyrgyzstan as a miniature world)

## C3.1 Overview
**The idea in one line:** all of Kyrgyzstan as one hand-made diorama (felt mountains, a ribbon of switchback road, yurts, poplar rows, a turquoise lake), crossed by one small cream toy truck that carries a parcel from a city door to a regional door. At the end, the round crown of a yurt becomes our logo.

**Single-minded proposition:** **«Посылки между городами — от двери до двери»**. The country feels small and simple when Kiwi Go carries the parcel. The message proposition («как сообщение») sits on the card as the tagline backup.

**Proof points:** «Заберём у двери» · the coverage line (A/B) · «Цена за место — вес не важен» · «Вручаем по коду из SMS» · «от 350 сом» · seller-side tracking in an app card.

**CTA:** «Оформите доставку» → app.kiwigo.kg.

**Why it stops the scroll:** a vertiginous top-down view of a toy truck on a ribbon of switchbacks is the purest version of the viral miniature trend, and the closest to the reference the client loves. The direct question «Посылка в другой город?» selects the audience in under a second.

**Why it sells:** it visualises **coverage**, the client's own ask, honestly: it shows a journey between cities, not a claim about every door. It owns the **local** card (yurts, felt mountains, the tunduk), so it could not be mistaken for a foreign template ad. AI risk is the lowest of the three, because people stay tiny.

## C3.2 Shot-by-shot script (master 20.0 s)

**Time-of-day arc:** golden dusk (S1–S2) → a blue night-to-dawn journey across the diorama (S3) → golden morning (S4–S5). The diorama materials stay consistent: felt mountains, painted-resin water, flocked trees, matte toy plastic for vehicles and figures.

| # | TC (s) / bars | Picture: what we SEE | AI method | Transition IN / OUT | Super (RU), position | Our composite | Beat |
|---|---|---|---|---|---|---|---|
| S1 | 0.00–2.00 · B1.1–B1.4 | **HOOK.** A top-down, slightly tilted view of a diorama mountain pass: felt-textured slopes, a cream ribbon road folding into 8 switchbacks, and long golden-dusk shadows. A small **cream-and-ink box truck** (blank panels, plain wheels) is climbing; its headlights are on. **Camera:** a slow **descent toward the truck's roof** with a slight roll correction, already moving on frame 0. | Truck object still (turnaround) → GPT-hi start → **K3P** 5 s; use 2 s. "The toy truck climbs the switchback road; the camera descends slowly straight down toward its roof; trees and mountains stay rigid; all surfaces blank." | IN: **R1** loop fog. OUT: **roof match**. The descent ends with the cream roof filling the lower half of frame, and S2 starts on the same roof. | «Посылка в другой город?» at **P-HOOK**, 0.00–1.90 | none | HIT on frame 0. Sparse groove. |
| S2 | 2.00–4.00 · B2.1–B2.4 | **Pickup.** It opens on the same cream truck roof, top-down, then **tilts up** to reveal it parked side-on at a miniature city apartment block at dusk. The courier (lime cap) carries a parcel from the entrance door, where the seller waves small and soft in the doorway, toward the truck's side door. | GPT-hi **end frame** (a side-on street view: truck, door, courier mid-walk) + GPT-hi **start frame** (an edit: roof top-down, same light) → **FLF-S** test → **FLF-P** 5 s; use 2 s with a speed ramp. "Continuous tilt up from the truck roof to reveal the street; the courier walks from the door to the truck carrying the parcel; ending exactly on the last frame." | IN: roof match. OUT: **R2 light leak**: the truck's headlight flare blooms into the orange-lime leak, 3.75–4.50, cut at 4.00. | «Заберём у двери» at **P-HIGH**, 2.25–3.90 | **Kiwi wheels (the gate passes):** the parked side-on truck, wheels about 90 px, static, our SVG with a ±1° wobble lock. **App card** at top-left: «Kiwi Go для магазинов» with «Забрали ✓» at 3.50. | **HIT B3.1 (4.0): leak.** |
| S3 | 4.00–10.00 · B3.1–B5.4 | **The diorama run (hero).** One continuous move across the country-board. The camera tracks alongside the truck (tiny, on a road between felt ridges, blue night with the headlights on), then rises as the road crosses a yurt valley by a turquoise lake, while the sky in the diorama warms to dawn. It ends behind a foreground **poplar** as the road enters a regional town. | GPT-hi **end frame first** (a dawn town edge behind a foreground poplar) + **start frame** as an edit (a night ridge road, same horizon and light side) → **FLF-S** 10 s test → **FLF-P 10 s**; time-remapped to 6 s (an ease ramp; frames dropped, not interpolated). "The tiny truck drives along the road between felt mountains; the camera tracks alongside, then rises gently over the yurt valley and lake as light warms to dawn, finally passing behind a foreground poplar tree; one continuous move ending exactly on the last frame." | IN: R2 leak. OUT: **occlusion wipe**: the poplar trunk crosses the lens, with the cut on the trunk; a backup trunk sprite cut from the plate is composited if needed. | Coverage, **A «По всему Кыргызстану»** / **B «Между городами Кыргызстана»**, at **P-HIGH**, 4.25–6.75. Then «Цена за место — вес не важен» at **P-LOW**, 7.00–9.75 (6 words, 2.75 s). | App card: «В пути» goes lime at 5.00, «В городе» at 9.00. No kiwi wheels (the truck is tiny; the gate fails). | **Swell 8.0–9.5** (B5.1) on the rise over the lake. |
| S4 | 10.00–12.50 · B6.1–B7.2 | **Arrival.** Golden morning in a miniature regional street: a blue gate and a courtyard with a **white yurt** set up beside the house. The truck **rolls in side-on and stops** at 10.75. The courier hands the parcel to the recipient at the gate (both small in a medium-wide shot, three-quarter view). **Camera:** locked with a slight push. | Courier **Sheet** + truck still → GPT-hi start (the truck entering from the left) → **FLF-S** test → **K3P** 5 s; use 2.5 s. "The toy truck rolls in from the left and stops at the gate; the courier steps out and hands the parcel to the woman, who takes it with both hands; camera locked, slight push in. Surfaces blank." | IN: the occlusion wipe (the poplar trunk slides off left). OUT: **chained frame** into S5. | «Вручаем по коду из SMS» at **P-HIGH**, 10.25–12.25 | **Kiwi wheels** if the gate passes (side-on, about 80 px, rotation from the hub track until the stop, then static). App card: «Вручено ✓» at 12.00, then the card slides out. | B6.1 cut. B7.1 chip. |
| S5 | 12.50–16.00 · B7.2–B9.1 | **Logo born in the world.** From the courtyard the camera **cranes straight up** into a perfect top-down view of the white yurt. Its round **tunduk** (crown ring with crossed spokes) lands dead centre at (490, 800). Golden morning; long soft shadows. | GPT-hi **end frame first** (a top-down yurt with the tunduk centred, 400 px wide) → start = S4's last frame (chained) → **FLF-S** test → **FLF-P** 5 s; use 3.5 s. "One continuous crane straight up and tilt down to a perfect top-down view of the yurt roof, the round crown centred, ending exactly on the last frame; slow ease-out." | IN: chained frame. OUT: **R5** flash match-cut. | none | **Tunduk → logo** (§C3.3), plus a light sweep over the logo at 15.5. | **Swell 12.5–13.5. Breath 13.5–14.0. HIT B8.1 (14.0): logo. PEAK B9.1 (16.0).** |
| Card | 16.00–20.00 | End card (§0.7 and §C3.4). | none | IN: R5. OUT: R7 → loop to S1. | see §C3.4 | full card | Resolve, loop. |

**Cut-down (10.0 s):**
1. S1 hook, 0.0–2.0.
2. S3 diorama run, 2.0–5.0: the coverage super A/B, then the app card «В пути». The price-per-place super moves to the card.
3. S5 yurt crane, 5.0–7.0, with the logo at B4.1 (6.0).
4. Card, 7.0–10.0.

## C3.3 Logo and brand moment
1. **Brand cues before the logo:** the courier's lime cap (S2, at 2.5 s), **our kiwi wheels on the parked truck** (S2), and the lime chip in the app card.
2. **Kiwi wheels, composited:** S2 passes the §0.6 gate (parked, side-on, about 90 px), so our SVG sits on both visible wheels and is static. In S4 the truck rolls in side-on and the SVG rotates by distance ÷ radius from the hub track until it stops. If the S4 track error is above 2 px, the S4 wheels stay plain and only S2 keeps them. AI never draws a kiwi.
3. **In the world (S5, 14.0 s):** the end frame centres the yurt's round crown at (490, 800), 400 px wide. On B8.1, a circular matte taken from the crown cross-fades it into our logo over 6 frames, with scale 0.92 → 1.0. The crown's ring and spokes give way to the kiwi's rim and 12 seeds, a **shape match, not an AI morph**. The logo is then plane-locked to the slowly settling plate, and the morning light sweep goes **over** it at 15.5.
4. **Resolve (R5):** a flash at 16.0. The icon keeps (490, 800), then eases to (490, 520) with the wordmark type-on.
5. **Cultural fallback:** the tunduk is also the centre of the national flag. **Before production**, a local check is needed that turning a yurt crown into a commercial logo will not read as disrespect to a national symbol. If the answer is "risky", use the same mechanic on a **top-down round лепёшка (нан)** on a dastarkhan in the courtyard: its stamped centre and ring also match the kiwi slice. That costs one more end-frame still (2.75) and no extra video, because S5 is regenerated only if needed.

## C3.4 End card copy (Onest)
- Logo → **«Kiwi Go»**
- Descriptor: **«От двери до двери»**. If the client wants the coverage line on the card too: **A «По всему Кыргызстану»** / **B «Между городами Кыргызстана»** at 40 px, replacing the price note.
- **«от 350 сом»** + «цена за место»
- CTA verb: **«Оформите доставку»** (the seller export: «Подключите магазин»)
- Pill: **«app.kiwigo.kg»**

## C3.5 Risks and mitigation

| Risk | Where | Mitigation |
|---|---|---|
| The diorama drifts to a "real aerial" look and the miniature magic is lost | S1, S3 | Materials are named in every still (felt, flocked trees, resin water, matte toy plastic) on top of the style anchor. A strong tilt-shift band. R6 tilt-shift reinforcement in post. A 4-still "world bible" is approved before any video. |
| The 10 s hero move melts or warps (a long path) | S3 | End frame first, start frame as an edit (same horizon and sun side), a simple path (track → rise → pass behind a tree), and an FLF-S 10 s test (10 cr). Fallback: `kling4_0` 1080p 10 s with two ordered middle keyframes (32.5). Premium: `cinematic_studio_3_0` 720p, `genre:"epic"`, 25 per try. |
| The top-down crane rotates or misses centre | S5 | The end frame locks the composition; the tunduk is centred in the still; our 2D stabilise and re-centre in post (a few pixels is fine because the logo is plane-locked). |
| Lettering on the truck, gate or shop fronts | S1, S2, S4 | Blank panels; "no signage, no numbers, no plates". 100 % check and paint-out. Any stray marks on the truck side can be covered by a composited clean panel. |
| Kiwi-wheel composite slides | S2, S4 | §0.6 gate. A static composite in S2; in S4 only if the track holds within 2 px; otherwise plain wheels. |
| Hands in the handover | S4 | People are small in a medium-wide; frame 0 is mid-handover; FLF-S test. At this scale artefacts are hidden by the tilt-shift blur. |
| The tunduk reads as appropriating a national symbol | S5 | A local cultural check before production; the лепёшка fallback (§C3.3). |
| Too many supers on the long hero shot | S3 | Only two supers in sequence, each on its own beat, with nothing else in the key band. |

## C3.6 Budget (Higgsfield credits)

| Line | Qty | Unit | Credits |
|---|---|---|---|
| Character sheet (courier) | 1 | 3.5 | 3.5 |
| Truck turnaround still (blank panels, plain wheels) | 1 | 2.75 | 2.75 |
| "World bible" diorama stills (materials, palette) | 4 | 1.0 | 4.0 |
| Exploration stills (5 shots × 2.5 cr) | 20 | — | 12.5 |
| Final start frames, 5 + 1 redo each | 10 | 2.75 | 27.5 |
| End frames for S2, S3 and S5, plus a redo each | 6 | 2.75 | 16.5 |
| Motion tests on FLF-S (S2 at 5 s, S3 at 10 s, S5 at 5 s) | — | 5 / 10 / 5 | 20.0 |
| Finals: K3P × 2 (S1, S4) | 2 | 7.5 | 15.0 |
| Finals: FLF-P 5 s × 2 (S2, S5) + FLF-P 10 s (S3) | — | 6.25 / 12.5 | 25.0 |
| Retries: S1 × 0.5 (3.75), S2 × 1 (6.25), S3 × 1.5 (18.75), S4 × 1.5 (11.25), S5 × 1 (6.25) | — | — | 46.25 |
| **Subtotal** | | | **173.0** |
| Contingency: S3 premium `cinematic_studio_3_0` 720p, 1 try + 1 retry | 2 | 25 | 50.0 |
| Lepyoshka fallback end frame (only if needed) | 1 | 2.75 | 2.75 |
| **Total with contingency** | | | **≈ 226** (about 263 of 489 left) |

---

## Ranking (my own verdict)

| Rank | Concept | Marketing strength | Craft / reference fit | AI risk | Cost (with contingency) |
|---|---|---|---|---|---|
| **1** | **C1 «Вечер без автовокзала»** | ★★★★★ | ★★★★ | Medium–high (two handovers, a phone) | ≈ 221 |
| **2** | **C3 «Страна-диорама»** | ★★★★ | ★★★★★ | Low–medium (one long move) | ≈ 226 |
| **3** | **C2 «Отправлено»** | ★★★½ | ★★★★½ | Medium (levitation, handover) | ≈ 173 |

1. **C1 wins** because it answers the client's actual complaint ("no marketing") most directly.
   - It opens on the strategist's #1 hook, which is the target customer's daily pain.
   - It has a real story turn (cold to warm, same sofa).
   - It shows every proof point in action, including seller-side tracking on *her* phone, which is the most honest way to show tracking.
   - Its weak spot is people and hands. That risk is contained by mid-handover starting frames, toy style, motion tests and a Seedance fallback inside the budget.
2. **C3 is the safest high-craft choice.** It looks most like the reference the client loves, is the most local and spectacular, and is the most honest way to show the client's coverage wish.
   - It ranks second because its hook is a question, not a felt pain, and its story is about the truck rather than the seller, so it converts sellers less sharply.
   - It is the best brand-awareness or cold-reach film, and it has the lowest risk of uncanny people.
3. **C2 is the most brand-ownable idea** (the proposition becomes the film's physics) and the cheapest.
   - Magical realism risks the viewer not understanding *what the company does* until the courier appears at 8 s.
   - The levitation shot is the single most failure-prone generation across the three concepts, although it has a credit-free composite fallback.
   - It is the best **hook head**: the floating parcel should be tested as the alternative first 2.5 s on C1's body.

**Recommendation:** produce **C1 as the master**, with **C2's S1 as the A/B hook head** (+10.25 cr). If the client wants a second film from the same reserve, **C3** follows as the brand-awareness piece. C1 plus the C2 head costs about 231 cr. C1 and C3 together cost about 447 of 489, which is too tight for client revisions, so produce C3 only after C1 is approved.

---

## Summary
- Three distinct 20.0 s masters (10 bars at 120 BPM, re-conformable to 110–120 BPM while staying at or under 22 s), each with a 10 s cut-down, a frame-0 hook super, a story arc, seller-side tracking only, and a cream-fog loop.
- **C1 «Вечер без автовокзала»:** a seller's pain → relief on the same sofa. The logo is born on the parcel's blank round sticker. ≈ 196 cr, ≈ 221 with contingency.
- **C2 «Отправлено»:** a parcel that flies like a message, then a real courier at the door. The logo is born from the trail's spark in a calm sky (R4). ≈ 145 cr, ≈ 173 with contingency.
- **C3 «Страна-диорама»:** a toy truck crosses a felt-and-resin Kyrgyzstan. A yurt's tunduk becomes the logo (with a cultural check and a лепёшка fallback). Composited kiwi wheels where the gate passes. ≈ 173 cr, ≈ 226 with contingency.
- The coverage super appears in both variants everywhere: A «По всему Кыргызстану» and B «Между городами Кыргызстана», exported as `_covA` and `_covB`.
- Copy: «от 350 сом», «цена за место», «Заберём у двери», «Видно каждый шаг», «Вручаем по коду из SMS». CTA pill «app.kiwigo.kg». Onest throughout. No city names, times, «Скоро» or internals.
- All logos and kiwi wheels are our composite of the exact SVG. AI plates are blank, unbranded, text-free, with plain wheels.
- Every one of the 14 old-film flaws is mapped to a fix (§0.8). There are no dissolves between unrelated shots; every cut is hidden in light, motion, occlusion or a match cut.
- Ranking: **1. C1** (best marketing), **2. C3** (best craft and coverage, lowest people risk), **3. C2** (most ownable; best used as C1's A/B hook head).
- Nothing was generated and no credits were spent.
