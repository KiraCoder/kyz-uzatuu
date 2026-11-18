# Kiwi Go — professional brand Reel: shared context for every agent

## Goal
Produce ONE professional, scroll-stopping, cinematic Instagram Reel for Kiwi Go: 9:16, about 15–25 s, NO music in the export (the client adds licensed music later, so plan beat points). The footage comes from Higgsfield AI video (no text, no logos inside the AI footage). The exact logo, all Russian text and the end card are added afterwards in our own compositing pipeline (Python/ffmpeg/Playwright), so AI never draws the logo or the text.

## What went wrong in the previous attempt (avoid it)
The client called the last brand film "low quality: the scenario was not reviewed and it has no marketing in it". It had:
- pretty but generic shots (a kiwi tyre on a mountain path, a city aerial, a sunset)
- no hook in the first second, no story, no benefit, no reason to act
- text only at the very end, and no call to action beyond the tagline
- generic prompts, with no research on which Higgsfield model or settings suit which shot.
The film is at kiwi-go-soon/higgsfield/brand-film/kiwi-go-brand-film.mp4, with frames in the same folder.

## Reference the client loves (style and professionalism target)
kiwi-go-soon/brand-reel/research/reference/reference.mp4 (17 s; contact sheets are sheet0.png and sheet1.png in the same folder). Breakdown:
- 0–4.3 s: tilt-shift miniature 3D world; a toy-like character with a backpack walks up a rocky mountain path, filmed by a follow-cam from behind; opens from a white light leak.
- ~4.3–5.3 s: an orange light-leak flash covers the cut.
- 5.3–9 s: miniature aerial view of a city in front of mountains, slow drift, sun flare.
- 9–11.5 s: one continuous crane up into golden clouds (the camera move IS the transition).
- 11.5–12.8 s: the brand mascot appears in the sky, inside the scene.
- 13–15.3 s: clean off-white card; the logo icon, then the wordmark types on, then a small tagline.
- 15.3–17 s: flare, then black.
- Sound: one smooth music bed that swells with the camera rise and peaks at the logo reveal. There are no sound effects.
- Why it works: one story and few shots; invisible transitions; one consistent grade (golden, bloom, miniature depth of field); no text until the brand moment; the logo appears inside the world first.

## Company — PUBLIC facts only (from kiwigo.kg; full page text in research/site/*.txt)
- Kiwi Go (ОсОО «Киви Го», Osh) is an express door-to-door parcel delivery service between cities of Kyrgyzstan: «Экспресс-доставка посылок между городами Кыргызстана». Bishkek—Osh plus the regions (about 80 destinations).
- It is ALREADY OPERATING (launched November 2026).
- Price is per parcel ("за место"); weight and size don't change it. Bishkek—Osh 350 сом; regions 300–500 сом. Delivery within a city is "coming soon". Public wording to use: «от 350 сом».
- Courier picks up from the sender's door in the evening; the parcel leaves the same evening; it is delivered by lunchtime the next day (Bishkek→Osh flow). Do NOT promise exact times on screen ("Обещаем только измеренное").
- Shops use the app «Kiwi Go для магазинов» (also app.kiwigo.kg in the browser): create order, print labels, hand over to the courier, track status. Cash on delivery (наложенный платёж) is paid out on the next working day.
- Recipient gets an SMS code and gives it to the courier on handover.
- Digital and transparent: «Посылку видно на каждом шаге», «Без звонков «где моя посылка»».
- Main customers: online shops and Instagram/WhatsApp/Telegram sellers. Secondary: private senders.
- Positioning idea from the company: «Отправить посылку по Кыргызстану так же просто, как написать сообщение». You pay only for delivery; no percentage of the goods' value.
- Second business, Kiwi Cargo: cargo to Moscow and Wildberries, 1 500 сом per box. NOT the focus of this Reel.
- The website shows a "truck with kiwi wheels" illustration: a delivery truck whose wheels are kiwi slices.
- Never show: salaries, margins, internal strategy, competitor names, city names as text, delivery-time promises, and never «Скоро запуск».

## Brand
- Colours:
  - lime #B8F03C (signature)
  - ink #111410
  - paper #FFFDF7
  - cream #F6F1E4
  - sand #ECE6D6
  - kiwi-skin brown #7A5A3C
  - green ink #3F6212
  - logo rim #6BA82B
  Lime + ink is what sets the brand apart from green competitors.
- Logo: a kiwi slice that reads as a WHEEL. Tyre r100 #111410, rim r86 #6BA82B, flesh r80.5 #B8F03C, 12 seeds (ellipse cy -56.3, rx 5, ry 14, rotate i*30), cream centre r26 #F6F1E4, dot r8.5 ink. The files are kiwi-go-soon/logo/kiwi-go-logo.svg and kiwi-go-logo-1024.png. NEVER let AI draw or alter it; we composite it.
- Fonts: the website uses Onest; our assets so far use Inter. Either is fine; recommend one.
- Tone: friendly, confident, modern, local (Kyrgyzstan: mountains, roads, yurts, bazaars, cities), never "generic success-green".

## Constraints for the AI footage
- Higgsfield credits cost money. Research and planning agents must NOT generate anything; using estimate/cost tools and model catalog lookups is fine.
- No text, letters, signage or logos in AI frames. Vans and trucks unbranded, OR left with clean blank panels where we can composite the brand later.
- The client has about 489 credits. Kling 3.0 Pro costs 7.5 credits per 5 s 1080p silent clip; GPT Image 2.6 start frames cost 0.25 each; Cinema Studio 3.0 costs 65 per 5 s; Seedance 2.5 1080p costs 80 per 5 s.
- Proven workflow: generate a start image (gpt_image_2_6), check it, then image-to-video (kling3_0 pro, sound off). Clips come out 1076×1924 at 24 fps, 5 s.

## Deliverable folder
kiwi-go-soon/brand-reel/ — each agent writes its own markdown file there (named in its task). Write in English, but keep all on-screen copy in Russian.

## Client contact details (confirmed 2026-11-18)
- WhatsApp and phone for ads: **+996 224 222 221**. This replaces +996 506 016 199 everywhere.
