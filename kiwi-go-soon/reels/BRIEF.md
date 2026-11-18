# Shared brief for every Kiwi Go Reel agent

## Company (public facts only)
Kiwi Go (ОсОО «Киви Го») is a door-to-door courier service that is ALREADY DELIVERING (launched November 2026) across ALL of Kyrgyzstan. Main customers are online shops and Instagram/WhatsApp/Telegram sellers. The promise: «Отправить посылку так же просто, как написать сообщение». You pay only for delivery, never a percentage of the goods' value. Website: kiwigo.kg (never kiwi.kg).

PUBLIC rules:
- Say «по всему Кыргызстану».
- Prices only as «от 350 сом».
- Never show salaries, margins, the full tariff table, strategy, competitors' names, or delivery-time promises.
- Don't name cities.
- Never say «Скоро запуск»: we have launched.

## Format
- 9:16, 1080×1920, 30 fps, H.264 yuv420p + AAC 192k stereo, `-movflags +faststart`. Length as in your Reel spec; at most 15 s.
- Instagram safe zones: keep ALL text and the logo inside x 110–950 and y 260–1480. The top ~220 px, the bottom ~400 px and the right ~120 px are covered by Instagram's UI.
- Text: Russian, spelled correctly; double-check every word. Big and readable on a phone: headlines 90 px or more, other text 48 px or more. One message on screen at a time.
- Colours: lime #B8F03C, ink #111410, paper #FFFDF7, cream #F6F1E4, sand #ECE6D6, kiwi-skin brown #7A5A3C, green ink #3F6212, logo rim #6BA82B. Lime + ink is the signature. Never put lime text on light backgrounds; ink on lime and lime on ink are fine.
- Font: Inter, from /home/user/kyz-uzatuu/kiwi-go-soon/fonts/ (Black, ExtraBold, Bold, SemiBold) or /usr/share/fonts/opentype/inter/ (including Inter Display). Load it with @font-face and wait for document.fonts.ready.

## LOGO — exact; never redraw or recolour (scale, rotate, squash and animate only)
The file is /home/user/kyz-uzatuu/kiwi-go-soon/logo/kiwi-go-logo.svg (viewBox -100 -100 200 200):
- circle r100 #111410 (tyre)
- circle r86 #6BA82B (rim)
- circle r80.5 #B8F03C (flesh)
- 12 seeds: ellipse cx=0 cy=-56.3 rx=5 ry=14 fill #111410, rotate(i*30) for i = 0..11
- circle r26 #F6F1E4
- circle r8.5 #111410

Use this single logo at EVERY size. There is no "small version". After rendering, zoom into a frame and count 12 seeds on one ring.

## Proven technique (copy it)
Reference implementation: /home/user/kyz-uzatuu/kiwi-go-soon/reel/ (reel.html with a deterministic `render(t)`, render.js, audio.py, encode.sh, storyboard.py). Look at it first and reuse its structure, easing helpers and audio synth.
- Build the animation as HTML/SVG driven by `render(t)`. Do NOT use real-time CSS animations.
- Drive it with Playwright in Node: `require('playwright')` works, `chromium.launch()` needs no options, and you must NOT run `playwright install`. Screenshot frame by frame.
- Use at most 2 sub-frames per frame for motion blur, or none. Six agents render at the same time, so keep it lean.
- Encode with /usr/bin/ffmpeg (libx264 + aac).
- Sound: synthesise ORIGINAL audio yourself with Python + numpy (scipy is not installed; write the WAV with the `wave` module). Use whooshes, hits, ticks, bells and a short upbeat groove, with hits synced to the visual beats. Aim for about -14 LUFS, true peak about -1 dBFS (push it louder than the first Reel, which peaked at -5). Add short fades. No downloaded or copyrighted audio.
- Disk is limited. Write frames only inside your own folder's `frames/` directory and DELETE it as soon as the MP4 is encoded.

## Deliverables (inside YOUR folder only)
- `<name>.mp4` (the final file)
- `poster.png` (best frame, for the cover)
- `storyboard.png` (about 8 frames)
- your source files (html/js/py/sh)

## QA before you report
- Look at the storyboard and some single frames with the Read tool (downscale them first). Check clipping, overlaps, safe zones, spelling, and the 12-seed logo.
- Run ffprobe to confirm duration, resolution and that there's an audio stream, and measure loudness.

## Restrictions
- Do NOT touch other folders.
- Do NOT git commit or push.

## Report back
The shot list with the exact copy, the sound sync points, the ffprobe line, file paths, and known weaknesses.
