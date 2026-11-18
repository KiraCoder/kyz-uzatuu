# 06 — Copy and brand review of the three concepts

Reviewer role: senior Russian-language copy editor and brand guardian. I did not write `04-concepts.md`.
Inputs: `CONTEXT.md`, `01-marketing-strategy.md`, `04-concepts.md`, `research/site/index.html.txt`, `research/site/support.html.txt` (the source of truth for claims), the logo file `kiwi-go-soon/logo/kiwi-go-logo.svg`, and the Onest TTFs from Google Fonts (downloaded to the scratchpad only so I could measure line widths and check glyphs).
Nothing was generated and no credits were spent.

**How the widths were measured.** I set every line in real Onest (SemiBold 600 for supers and UI, Bold 700 for the wordmark and price) with PIL at the size `04 §0.3/§0.7` specifies. A super pill sits inside x 80–900. That is 820 px, and after the lime dot and the padding about **720 px is left for text at 72 px**. The end card text column is x 100–880, which is **780 px**.

**Reading-speed rule I used.** On a phone a viewer reads **up to 3 words in about 1 s**. 4–5 words need 1.5–2 s. 6 or more words don't belong in a super. The concepts' own hold rule (at least 0.4 s per word and at least 1.2 s) is fine and every super meets it. The real problem is **width**: eight supers do not fit on one line at 72 px.

---

## 1. Every on-screen line: language, naturalness, length, verdict

Legend: **OK** = ship as is · **FIX** = ship the corrected version · **CUT** = remove. "/" in the corrected column marks the line break I prescribe. Never end a line on a one-letter or short preposition or conjunction (и, в, у, по, на, за).

### 1A. Supers (in-shot)

| # | Where | Line as written | Words | Width at 72 px (limit ≈ 720) | Spelling, grammar, ё, «» | Naturalness (Bishkek or Osh seller) | Verdict | Corrected version |
|---|---|---|---|---|---|---|---|---|
| S-1 | C1 S1 (hook) | «Где моя посылка?» | 3 | 633 ✔ one line | Correct. | Exactly what clients write. The voice is the client's, which the bubbles make clear. | **OK** | Где моя посылка? |
| S-2 | C1 S2 | «Опять на автовокзал?» | 3 | 772 ✘ slightly too wide | Correct. | Natural and instantly recognised. "Передать с водителем" is the local idiom; a stronger local variant for the hook A/B test is «Опять искать, с кем передать?». | **FIX** (line break only) | Опять / на автовокзал? |
| S-3 | C1 S3, C2 S2, C3 S2 | «Заберём у двери» | 3 | 603 ✔ | **ё is mandatory** («Заберём», not «Заберем»). | Natural. | **OK** (C2 note below) | Заберём у двери |
| S-4 | C1 S4, C2 S3 | «Видно каждый шаг» | 3 | 669 ✔ | Acceptable. «видно» plus the nominative is conversational and fine for a super. The site's own form is «Каждый шаг виден» / «Посылку видно на каждом шаге». | Natural. | **OK** | Видно каждый шаг |
| S-5 | C1 S5 | «Без автовокзала и звонков» | 4 | 958 ✘ | Correct. | Natural. «звонков» reads as calls to drivers, which is fine. | **FIX** (break) | Без автовокзала / и звонков |
| S-6 | C1 S6, C2 S4, C3 S4 | «Вручаем по коду из SMS» | 4 | 876 ✘ | Correct; «SMS» in Latin script matches the site. | Natural, **but scam-sensitive** (see §2.5). | **FIX** | Вручаем / по коду получения |
| S-7 | C2 S1 (hook, line 1) | «Отправить посылку…» | 2 | 748 ✘ | The ellipsis must be one glyph «…» with no space. The ellipsis reads as trailing off, while the dash reads as a set-up. | Natural. | **FIX** | Отправить посылку — |
| S-8 | C2 S1 (hook, line 2) | «…как сообщение» | 2 | 591 ✔ | Drop the leading ellipsis. | Natural. It is the company's own idea. | **FIX** | как сообщение |
| S-9 | C2 S3, C3 S3 (cov. A) | «По всему Кыргызстану» | 3 | 816 ✘ | Correct. Use «Кыргызстан» (the official and locally preferred name), never «Киргизия». | Natural. | **FIX** (claim, §2.1) | A: По всему / Кыргызстану (only if the client signs off) · **A′: По Кыргызстану** (520 px, one line) |
| S-10 | C2 S3, C3 S3 (cov. B) | «Между городами Кыргызстана» | 3 | 1092 ✘ | Correct. | Natural; it is the site's H1 wording. | **FIX** (break) | Между городами / Кыргызстана |
| S-11 | C3 S1 (hook) | «Посылка в другой город?» | 4 | 899 ✘ | Correct. | Natural; it selects the audience. | **FIX** (break) | Посылка / в другой город? |
| S-12 | C3 S3 | «Цена за место — вес не важен» | 6 | 1070 ✘ | Grammar is correct (em dash with spaces). | «за место» is cargo jargon, and a private sender may read it as **"per seat"** (as on a marshrutka). 6 words is too many for a moving shot. | **FIX** | Вес и размер / цену не меняют (verbatim from the site, 5 words, 2.75 s hold is fine) |

### 1B. UI chips, chat bubbles and app chrome (composited)

| # | Where | Line | Spelling, grammar | Naturalness | Verdict | Corrected |
|---|---|---|---|---|---|---|
| U-1 | C1 S1 bubbles | «где посылка?» · «уже отправили?» · «а когда будет?» · «??» | Lower case is deliberate (real typing). Correct. | Very natural; this is how clients write in DMs. They are texture, not reading copy, so 4 in 2 s is fine **as long as the main super is clearly dominant** (bigger, opaque pill, on top). | **OK** | No change. Keep the bubbles neutral (no WhatsApp green, no Telegram blue). |
| U-2 | C1 S4, C3 S2 app header | «Kiwi Go для магазинов» | No guillemets inside a UI header. In running text and captions it is always «Kiwi Go для магазинов». | It is the real app name (support page). | **OK** | Kiwi Go для магазинов (443 px at 40 px) |
| U-3 | Chips, all concepts | «Забрали» → «В пути» → «В городе» → «У курьера» → «Вручено» | Correct, sentence case. | These are the site's own statuses («Забрали, в пути, в городе, у курьера»). | **OK** | ✓ (U+2713) exists in Onest, so the tick renders in the same font. |
| U-4 | C2 S2 chat UI | «Отправлено ✓» | Correct. | Natural. | **OK** | Отправлено ✓ |
| U-5 | C2 S4 PiP | «Вручено ✓✓» | — | A double tick reads as a **WhatsApp read receipt** (mimicry of another brand), and it is inconsistent with the other concepts. | **FIX** | Вручено ✓ |
| U-6 | Strategy copy bank (not in the concepts) | «Наложка — на следующий рабочий день» | «Наложка» is seller slang, which is fine in a caption. | — | **Not on screen.** If added: | Деньги за товар — / на следующий рабочий день (caption only; the site adds "после вручения") |

### 1C. End card (shared §0.7 and the per-concept lines)

| # | Element | Line | Size, width (limit 780) | Notes | Verdict | Corrected |
|---|---|---|---|---|---|---|
| E-1 | Wordmark | «Kiwi Go» | Bold 128 → 468 ✔ | Use a no-break space (U+00A0) between Kiwi and Go. | **OK** | Kiwi Go |
| E-2 | C1 descriptor A | «Посылки по всему Кыргызстану» | SemiBold 46 → 726 ✔ | Claim risk (§2.1). | **FIX** | A: По всему Кыргызстану · A′: Посылки по Кыргызстану (577 ✔) |
| E-3 | C1 descriptor B | «Посылки между городами Кыргызстана» | 46 → **903 ✘ overflows** | The longest card line. | **FIX** | Между городами Кыргызстана (≈ 698 at 46 ✔) |
| E-4 | C2 descriptor | «Посылка — как сообщение» | 46 → 603 ✔ | Correct. | **OK** | Посылка — как сообщение |
| E-5 | C2 optional card coverage | «по всему Кыргызстану» / «между городами Кыргызстана» (40 px, lower case) | 447 / 600 ✔ | A lower-case start on a standalone line looks like a typo next to the sentence-case lines. | **FIX** | По всему Кыргызстану / Между городами Кыргызстана |
| E-6 | C3 descriptor | «От двери до двери» | 46 → 425 ✔ | It is a **universal promise** (§2.3). | **FIX** | Use the coverage line instead (B: Между городами Кыргызстана). |
| E-7 | Price | «от 350 сом» | Bold 104 → 566 ✔ | Lower-case «от» on a price tag is an accepted retail convention. Use a no-break space after «от» and before «сом». Write «сом», never «сомов» or «KGS». | **OK / decision** (§2.7) | от 350 сом (or «от 300 сом», see §2.7) |
| E-8 | Price note | «цена за место» | 40 → 276 ✔ | It is the seat ambiguity again, and it is a fourth reading line in 1 s. | **FIX** | за посылку · вес не важен |
| E-9 | CTA verb (seller) | «Подключите магазин» | 48 → 497 ✔ | Correct imperative, polite plural. | **OK** | Подключите магазин |
| E-10 | CTA verb (private) | «Оформите доставку» | ✔ | Better Russian than the site's «Сделать доставку». **Check** that a private person can actually order at app.kiwigo.kg; the support FAQ only describes shop registration. | **OK, with a check** | Оформите доставку (or, if private sign-up is not possible: «Напишите нам в WhatsApp» plus the ad button) |
| E-11 | CTA pill | «app.kiwigo.kg» | SemiBold 60 → 396 in a 680 pill ✔ | Lower case; no `https://` and no `www`. **Verify that the address opens a sign-up screen.** It is not in the public site text I have, which only shows the button «Открыть Kiwi Go · Работает в браузере». | **OK, with a check** | app.kiwigo.kg |

### 1D. Copy-to-picture notes
- **C2 S2:** «Заберём у двери» sits over a thumb tapping a phone, so the words and the picture disagree. Either use «Курьер заберёт у двери» (3 words, it says who does it) or swap it for «Отправлено» as the super and move «Заберём у двери» to S4.
- **C1 S1:** the hook super must be the top layer, at 100 % opacity, and larger than any bubble. Four bubbles plus a super in 2.4 s is the most text-dense moment in all three films.
- **C3 S3:** two supers back to back (coverage, then the weight line) during the most spectacular shot. That is fine, but keep the app card at top-left small (it is a third reading target).

---

## 2. Claim check against the public site

| # | Topic | What the site says | Lines affected | Risk | Safe wording |
|---|---|---|---|---|---|
| 2.1 | **Coverage** | H1: «Экспресс-доставка посылок между городами Кыргызстана». Hero eyebrow: «Посылки по Кыргызстану». Footer link: «Экспресс-доставка по Кыргызстану». FAQ: "сейчас посылки отправляют магазины Бишкека, а доставляем мы в Оше; в регионы посылки везут службы-партнёры. По Бишкеку пока не доставляем." The calculator has about 80 destinations, some only «до центра» or «у дороги». | S-9, E-2, E-5 | **«по всему Кыргызстану» is not on the site.** It implies every village and delivery within a city, and both are false today. Kyrgyz advertising law prohibits misleading (недостоверная) advertising; this is the line a competitor or customer could point at. | **B «Между городами Кыргызстана»** (site H1). Compromise if the client insists on the "whole country" feel: **A′ «По Кыргызстану»** / «Посылки по Кыргызстану», which is **the site's own hero wording**. Use A only with the client's written acceptance. |
| 2.2 | **Tracking visible to recipients** | The index page says «Получатель тоже видит — ссылка для отслеживания…» and «вы и получатель видите одно и то же». The support FAQ says: «Страницы отслеживания для получателя пока нет.» **The site contradicts itself.** | U-3 chips, S-4 | The concepts handle it correctly: chips only live in the seller's phone, PiP or app card. Never write «получатель тоже видит» and never show a chip on the recipient's phone. | «Видно каждый шаг» only over the seller's UI. **Tell the client to fix the index page**; it currently promises what the FAQ denies. |
| 2.3 | **«От двери до двери» as a universal promise** | It is the site headline, but the calculator labels many points «до центра» or «у дороги», and regions go through partners. | E-6 (C3 card), C3's proposition | It is fine as one step of a story («Заберём у двери» is true for shops), and risky as a standalone card promise. | In shot: «Заберём у двери». On the card: the coverage line, not «От двери до двери». If the client wants it, then only in the caption next to «Бишкек — Ош» (city names are banned on screen, not in captions; client's call). |
| 2.4 | **Speed or time** | The FAQ gives an evening pickup and delivery to the recipient before lunch the next day, for Bishkek→Osh only. Nothing public is stated for the regions. | No super makes a time claim. ✔ | **Visual implication:** C1 and C3 run night → morning and end at a **regional** house; C2 is a night flight. That suggests overnight delivery to the regions, which is not public. | Keep the arc (it is mood, not a promise), but **make the arrival read as a city courtyard** (Osh is a city with apricot trees and blue gates) rather than a village. Never put «экспресс», «быстро», «за ночь», «завтра» or «до обеда» on screen. Also do not use the strategy hook «Вы спите — посылка едет». |
| 2.5 | **«по коду из SMS»** | The FAQ says the recipient gets an SMS with a «код получения» and tells it to the courier on handover. | S-6 (all three concepts) | **Scam-sensitive.** KG press (Sept 2026) reports fraudsters posing as couriers who ask for SMS codes. An ad that teaches "give your SMS code to the courier" works against the public warning "никому не сообщайте код из SMS". | **«Вручаем по коду получения»** (the site's own term, used for the courier app: «вручение по коду получения»). Explain in the caption: «Получатель получает код в SMS и называет его курьеру при вручении». Add «Kiwi Go никогда не просит код по телефону» **only if the client confirms that this is true**. |
| 2.6 | **«цена за место»** | «цена за место по направлению, вес и размер её не меняют». | S-12, E-8 | The fact is true. The word is ambiguous («место» = seat on a marshrutka) and jargon for private senders. «по направлению» means the price changes by destination, which «от» covers. | On screen: «за посылку» and «Вес и размер цену не меняют» (verbatim). Keep «за место» in the caption and on the site, where there is room to explain it ("одна коробка или пакет = одно место"). |
| 2.7 | **«от 350 сом» vs regional prices 300–500** | The public text I have shows only «Бишкек — Ош: 350 сом за место». CONTEXT says regions are 300–500 and names «от 350 сом» as the public wording. | E-7 | «от X» means "X is the lowest price". If some destination really costs 300, «от 350» is **factually wrong, although in the customer's favour**. Nobody is misled into paying more, so the legal risk is low; it is a credibility issue if a viewer checks the calculator. «от» does correctly cover the 500 destinations. | **Decision for the client:** if a 300 tariff is live in the public calculator, use **«от 300 сом»** (accurate, and a stronger number). If the 300 rows are not public or not final, keep **«от 350 сом»**. Never show a route next to the price, and never drop the «от». |
| 2.8 | Branded courier in the regions | Regions are served by partner services. | C1 S6, C2 S4, C3 S4 (lime cap at a regional gate) | Low. The cap is a colour, not a logo. | Same fix as 2.4: a city-looking arrival. Don't composite the logo on the courier. |
| 2.9 | App UI shown on the phone | Real app tabs: «Заказы»: «В работе», «Завершённые». | C1 S4, C3 app card | Low. A fake UI that differs from the real app invites "this isn't what I got". | Build the mock from a real screenshot of «Kiwi Go для магазинов» (same layout and status names). |

---

## 3. Brand rules check

### 3.1 Logo
- **The file is correct:** `kiwi-go-soon/logo/kiwi-go-logo.svg` has exactly **12 seed ellipses** (cy −56.3, rx 5, ry 14, rotate 0…330 in 30° steps), the tyre r100 #111410, rim r86 #6BA82B, flesh r80.5 #B8F03C, cream centre r26 and ink dot r8.5. ✔
- **AI never draws it:** all three concepts composite the SVG (C1 sticker, C2 sky disc, C3 tunduk crossfade), and AI wheels are plain. ✔
- **Two conflicts with the "never spun or recoloured" rule (§0.5), to resolve before compositing:**
  1. **Rolling kiwi wheels (C3 S4)** rotate the logo. A wheel rolling is physically motivated, so I accept it **only as a separately approved "kiwi-wheel" use of the same SVG**, never on the icon or the card. The 12 seeds repeat every 30°, so above about 15° per frame (at 24 fps) the wheel strobes or appears to roll backwards. **Cap the rotation at 10° per frame**, or keep the wheels static (parked only).
  2. **The in-world tint** (multiply 8–10 %, haze, flare over the logo) is fine inside the scene. **On the end card the logo must be pure**: exact hex values, no tint, no bloom, no flare over it. Hand it over at the R5 flash.
- The «±1° wobble lock» in C3 S2 must mean "track tolerance", **not** an added wobble.
- **The wordmark:** the repository has only the icon. «Kiwi Go» set in Onest Bold is fine, but confirm it matches the site header lockup (case, spacing, weight) so the card and the site look like one brand.

### 3.2 Colour and contrast (WCAG ratios, calculated)

| Pair | Ratio | Use |
|---|---|---|
| ink #111410 on paper #FFFDF7 | 18.3 | ✔ all text |
| ink on cream #F6F1E4 (super pill) | 16.5 | ✔ supers |
| **ink on lime** (active chip, CTA pill) | **13.8** | ✔ signature pair, text OK |
| lime on ink | 13.8 | ✔ allowed: lime **text** only on ink |
| green ink #3F6212 on paper (descriptor) | 7.0 | ✔ AA at 46 px |
| ink at 70 % on paper (= #585A55, price note) | 6.9 | ✔ |
| **lime on paper** | **1.33** | ✘ never as text |
| lime on cream | 1.20 | ✘ never as text |
| rim #6BA82B on paper | 2.84 | ✘ never as text |

- **Lime as text on a light background: no violations found.** Lime appears only as fills (chips, CTA pill), the 14 px dot, the underline under «350», the cap and the trail. ✔
- **CTA pill:** the ink text inside it is perfect (13.8), but the **lime pill's edge against the paper card is 1.33**. In bright sunlight the pill can look like loose text. Add a 1.5 px stroke of ink at 15 % or a soft 8 % ink shadow. Do **not** switch to lime text.
- The DM bubbles are "neutral grey and white". The **text** inside them must be ink, not grey.

### 3.3 Onest vs Inter: **use Onest**
- It matches kiwigo.kg (one brand voice from the ad to the landing page), and its Cyrillic is friendlier and more modern than Inter's.
- **Cyrillic support is confirmed:** the Google Fonts CSS API serves Onest as a **variable font, weights 100–900**, with `cyrillic` and `cyrillic-ext` subsets (as well as latin, latin-ext, vietnamese, math and symbols). Weights **600 and 700**, the only two the spec uses, are available as static TTFs.
- **Glyphs checked in the 600 and 700 TTFs:** ё/Ё, « », „ “, — –, …, ✓ (U+2713), no-break space U+00A0, narrow NBSP U+202F, ₸, № are all present. ✘ The heavy check ✔ (U+2714) and the non-breaking hyphen (U+2011) are **missing**, so use ✓ and don't rely on U+2011.
- Bundle the TTFs locally in the pipeline (they are under the OFL licence). Don't let Playwright fall back to a web or system font; one missing glyph would silently switch to another typeface.

### 3.4 End-card hierarchy
The order in `04 §0.7` (logo → wordmark → descriptor → price → price note → CTA verb → pill) is right. The problems are that it is **dense** (7 elements and about 15 words in 4 s, about 2.5 s after the price lands) and that **one line overflows** (E-3).
Recommended card, 6 elements, all measured to fit in 780 px:

| Order | Element | Spec | In at (master / cut) |
|---|---|---|---|
| 1 | Logo icon | exact SVG, Ø 280, pure colours | 16.00 / 7.00 |
| 2 | «Kiwi Go» | Onest Bold 128, ink | 16.25 / 7.10 |
| 3 | Coverage descriptor | Onest SemiBold 46, green ink #3F6212 | 16.90 / 7.30 |
| 4 | «от 350 сом» | Onest Bold 104, ink, lime underline under the number | 17.00 / 7.50 |
| 5 | «за посылку · вес не важен» | Onest SemiBold 40, ink at 70 % (one line, replaces «цена за место») | 17.00 / 7.50 |
| 6 | CTA verb + lime pill «app.kiwigo.kg» | SemiBold 48 + pill 680×104, SemiBold 60 ink, 1.5 px ink stroke at 15 % | 17.50 / 8.00 |

The CTA then holds 2.1 s in the master and 1.6 s in the cut, which is just above the 1.5 s minimum. Don't start the loop fog in the cut before 9.6 s.

### 3.5 Name and domain consistency
- The brand is **«Kiwi Go»**: Latin script, capital K and G, one space (a no-break space). Never «KiwiGo», «Kiwi-Go», «KIWI GO» or «Киви Го» (the Cyrillic form is the legal name ОсОО «Киви Го» only).
- The app is **«Kiwi Go для магазинов»**, with guillemets in running text and captions and none in a UI header. Don't shorten it to «Kiwi Go Shop» or «приложение для продавцов».
- Domains are lower case: **kiwigo.kg** (site) and **app.kiwigo.kg** (the web app; the CTA). Use one CTA domain per export: don't show kiwigo.kg on the card and app.kiwigo.kg in the caption. Captions need «Ссылка в профиле», because Reels links are not clickable.

---

## 4. Recommended final copy set

Built on **C1** (the recommended master). Timecodes follow `04` C1. For C2 and C3, the same supers apply in their own slots, and the coverage super sits in S3.

### 4.1 Master, 20 s

| TC | Slot | Variant A «по всему Кыргызстану» | Variant B «между городами Кыргызстана» |
|---|---|---|---|
| 0.00–2.40 | Hook (P-HOOK) + bubbles | **Где моя посылка?** · bubbles: где посылка? / уже отправили? / а когда будет? / ?? | same |
| 2.50–3.90 | Super | Опять / на автовокзал? | same |
| 4.25–6.25 | Super | Заберём у двери | same |
| 6.75–8.75 | Super + app card «Kiwi Go для магазинов», chips Забрали ✓ → В пути | Видно каждый шаг | same |
| 9.25–11.25 | Super + chip В городе | **По всему / Кыргызстану** | **Между городами / Кыргызстана** |
| 11.50–13.50 | Super + chips У курьера → Вручено ✓ | Вручаем / по коду получения | same |
| 14.0–16.0 | Logo on the sticker | — | — |
| 16.0–20.0 | End card | Kiwi Go · **По всему Кыргызстану** · от 350 сом · за посылку · вес не важен · Подключите магазин · [app.kiwigo.kg] | Kiwi Go · **Между городами Кыргызстана** · от 350 сом · за посылку · вес не важен · Подключите магазин · [app.kiwigo.kg] |

Note: the coverage super replaces C1's «Без автовокзала и звонков» on the journey shot, because the journey is where coverage is shown and the bus station has already been named at 2.5 s. If the client wants to keep that line, put coverage on the card only.
Private-sender export: CTA verb «Оформите доставку», or «Напишите нам в WhatsApp» if private sign-up is not possible at app.kiwigo.kg.
Price: switch «от 350 сом» to «от 300 сом» if the client confirms a public 300 tariff (§2.7).

### 4.2 Cut-down, 10 s

| TC | Slot | Variant A | Variant B |
|---|---|---|---|
| 0.00–1.90 | Hook + 3 bubbles | **Где моя посылка?** | same |
| 2.00–3.90 | Super | Заберём у двери | same |
| 4.00–5.90 | Super + chips | Видно каждый шаг | same |
| 6.00–7.00 | Logo on the sticker | — | — |
| 7.00–10.00 | End card | Kiwi Go · **По всему Кыргызстану** · от 350 сом · за посылку · вес не важен · Подключите магазин · [app.kiwigo.kg] | Kiwi Go · **Между городами Кыргызстана** · от 350 сом · за посылку · вес не важен · Подключите магазин · [app.kiwigo.kg] |

(In the cut the coverage lives only on the card, which carries the whole proposition.)

### 4.3 Caption (both variants; only the bold part changes)
> Посылка в другой город — без автовокзала и звонков водителю.
> Заберём у двери и отвезём **по всему Кыргызстану / между городами Кыргызстана**. Каждый шаг видно в приложении «Kiwi Go для магазинов».
> Получатель получает код в SMS и называет его курьеру при вручении.
> от 350 сом за место — вес и размер цену не меняют.
> Ссылка в профиле: app.kiwigo.kg

### 4.4 Honest recommendation
**Ship B «Между городами Кыргызстана».** It is the site's own H1 and it is true today. If the client insists on the "whole country" feel, use **A′ «По Кыргызстану»** (the site's own hero line), not «по всему Кыргызстану», which today over-claims villages and delivery within a city.

---

## Summary
1. 30 on-screen lines were checked (supers, bubbles, chips, app chrome, card). Spelling is clean; the one mandatory ё is «Заберём».
2. Eight supers overflow one line at 72 px (measured in real Onest). Line breaks are prescribed, with no prepositions left hanging at the end of a line.
3. The C1 card descriptor B overflows at 46 px (903 > 780). Fix: «Между городами Кыргызстана».
4. Fix «Вручаем по коду из SMS» → «Вручаем по коду получения»; the SMS wording echoes current courier scams.
5. Fix «цена за место» → «за посылку» on screen (it can be read as a marshrutka seat), and use «Вес и размер цену не меняют» verbatim.
6. «По всему Кыргызстану» is not on the site and over-claims. Recommend B, or A′ «По Кыргызстану» (the site's own words).
7. «От двери до двери» should come off the C3 card. Night-to-dawn arrivals at regional houses imply overnight delivery to the regions; make the arrival a city courtyard.
8. «от 350 сом» is inaccurate if 300 tariffs are public; switch to «от 300 сом» once the client confirms.
9. Recipient tracking is handled correctly (seller-side only). The live index page contradicts its own FAQ and should be fixed.
10. Brand: the logo SVG has exactly 12 seeds. There are no lime-text-on-light violations. Rolling kiwi wheels need sign-off and a 10°-per-frame cap, and the card logo must not be tinted.
11. Use Onest: variable 100–900, Cyrillic confirmed, with ё, «», ✓ and NBSP present. Bundle the TTFs locally. The card is trimmed to 6 elements.
12. Check before launch: app.kiwigo.kg opens sign-up, private senders can order there, and the 300 tariff is live.
