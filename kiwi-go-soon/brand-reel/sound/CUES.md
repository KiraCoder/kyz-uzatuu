# Kiwi Go Reel «Отправлено»: sound cue sheet

The sound is built for `edit/out/kiwigo_reel_master_20s.mp4` (20.000 s, 24 fps, 120 BPM). The muxed result is `edit/out/kiwigo_reel_master_20s_sound.mp4`.

`audio.py` synthesises everything with numpy: no samples, no voices. To rebuild, run `python3 audio.py`, then remux with this command:

```
ffmpeg -i edit/out/kiwigo_reel_master_20s.mp4 -i sound/mix.wav -map 0:v:0 -map 1:a:0 -c:v copy \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -t 20.000 edit/out/kiwigo_reel_master_20s_sound.mp4
```

Every time below was read off the frames, using contact sheets plus per-frame luma, lime-pixel and difference analysis. Where the picture differed from the brief, the sound follows the picture; those cues are marked **(frames)**.

## Music bed (`music.wav`), D major, 120 BPM

| Time (s) | Section | What plays |
|---|---|---|
| 0.00–2.50 | Night, tense | A cool drone (D2, A2, F3 with a C#4/D4 rub, plus filtered air), a wooden clock ticking in 8ths (tick/tock, L/R) and a low "lub-dub" pulse on each beat |
| 1.50–2.50 | Riser | A band-noise sweep from 350 Hz to 7 kHz plus a pitched glide from D4 to D6, cut at the hit |
| **2.50** | **HIT** (light leak) | A soft sub boom, a soft cymbal, a Dmaj9 pluck stab and the warm pad bloom. The night drone cuts out here |
| 2.50–6.00 | Warm groove | Marimba arpeggio in 8ths, soft kick on beats 1 and 3, shaker in 16ths, warm bass, and finger snaps from 4.5. Chords: Dmaj9, then Gmaj9 (from 4.5) |
| **6.00–8.00** | **Swell** (crane, dawn) | Bm7, then Asus4, then A. A string-like pad crescendo and an air sweep; the kick goes to every beat from 7.0; a tom fill at 7.50–7.88 |
| **8.00** | Swell top | A soft crash and a Dadd9 stab. Then a gentle continuation with a pluck layer (Dadd9, Gmaj9 at 10.0, A7sus at 11.0) |
| **12.00–12.50** | **BREATH** | The whole music bus drops by about 26 dB for one beat. A faint reverse air swell rises from 12.25 |
| **12.50** | Re-entry | Bm7, then Gmaj9 (13.0), then A (13.5). Kick on every beat, 16th-note marimba from 13.0 and a riser from 13.0 to 14.0 |
| **14.00** | **HIT** (kiwi wheel) | Kick, boom and a Dadd9 stab; a riser from 14.5 to 15.0 |
| **15.00** | **PEAK** (flash to card) | A full D chord (D3 to E5), a kick plus boom, a soft crash, a bell shimmer arpeggio (D6, F#6, A6, D7) and a low D5 bell |
| 15.00–17.00 | Card groove | The same groove, slightly softer |
| 17.00–19.20 | Resolve | Drums out. A G6 chord, then a D chord, with long notes and quarter-note marimba |
| 18.20–20.00 | Loop return | The night drone fades back in (it is at 70 % by 19.0 and 100 % by 19.6). Clock ticks at 19.00, 19.25, 19.50 and 19.75, and a pulse at 19.5. The 20.000 → 0.000 seam is continuous |

## Sound effects (`sfx.wav`)

| Time (s) | Picture | Sound | Pan |
|---|---|---|---|
| 0.000 | Bubble «где моя посылка?» | Bubble pop plus a notification ping at D6 | L 0.3 |
| 0.500 | Bubble «уже отправили?» | Pop plus a ping at Eb6 | L 0.3 |
| 1.000 | Bubble «??» | Pop plus a ping at F6 | L 0.3 |
| 1.39–1.80 (transient at 1.500) | «Отправлено ✓» | An upward "sent" whoosh, a soft tick and an A5→D6 check chime | moves C→R |
| 2.20–3.00 (peak 2.50) | Light leak (frames: bright from 2.29, peak at 2.46–2.62) | A bright noise whoosh plus a shimmer glide | wide |
| 2.68–3.10 | Stairwell door (the door is already open on screen) | A very soft wooden creak (stick-slip) | L 0.45 |
| 2.917, 3.125, 3.333, 3.583, 3.792, 4.000, 4.208, 4.375 **(frames)** | Courier turns and walks out to the right (foot contacts read per frame) | Felt footsteps: a soft thud plus a cloth scuff | moves from C to R |
| 4.28–4.74 (peak 4.50) | Whip pan (blur f102–f113) | A swish | L→R |
| 4.45–7.85 | Truck on the switchbacks, then into the clouds | A low engine (~41 Hz harmonics, low-passed at 380 Hz) plus tyre roll. Loudest at 6.4–6.7, where the truck is closest, then fades under the clouds | follows the truck: R 0.25 → L 0.45 (5.1–5.5) → C → R 0.75 (7.2) |
| 5.04, 6.04, 8.04, 9.04 **(frames)** | PiP chips «Забрали ✓», «В пути», «В городе», «У курьера». Each lime switch starts on 5.00, 6.00, 8.00 and 9.00 and completes 2 frames later | Two-note UI chimes, rising: F#5–A5, A5–D6, B5–E6, D6–F#6 | L 0.45 (the PiP) |
| 6.35–8.80 (crests at 6.95 and 8.50) **(frames)** | The cloud layer covers the frame from about 6.6; the cream haze bloom peaks at 8.50 | An airy two-band cloud whoosh | wide |
| 8.45–11.03 | Courtyard | Distant city (low-passed noise) and sparse bird chirps, very low | random |
| 10.80–11.45 (peak 11.00) | Glow cut (bloom from 10.92, peak 11.00) | A soft tonal glow swell (D6, A6, A5) plus air | C |
| 11.500 | Bubble «получила, спасибо!» | A warm, lower pop at D5 plus a D5→F#5 chime | L 0.15 |
| 13.40–14.35 **(frames)** | The light sweep crosses the truck from left to right (visible from 13.62) | A high shimmer sweep | L→R |
| 13.690 **(frames)** | The front wheel turns kiwi (frames 13.67–13.71) | A "click into place" plus a small sparkle | L 0.6 |
| 14.000 | The rear kiwi wheel is born | A bigger click plus a 4-note sparkle (F#6, A6, D7, F#7) | C |
| 14.75–15.25 (peak 15.00) | Cream flash (f357–f360) | A bright flash whoosh plus a D6 bell with an A6 partner | C |
| 15.06 | The logo settles | A soft pop | C |
| 15.250, 15.333, 15.417, 15.500, 15.625, 15.708 **(frames)** | «Kiwi Go» type-on, glyphs K-i-w-i-G-o | Tiny type ticks | spread L→R |
| 15.80–16.05 | Tagline fades and rises (from 15.92) | A tiny airy lift | C |
| 16.000 | «от 350 сом» | A light "ka-ching": a tick, a B6 then E7 bell (75 ms apart) and a faint coin shimmer | C |
| 16.500 | «Оформите доставку» and the kiwigo.kg pill | A soft pop plus an A5–C#6 chime | C |
| 17.000 | The WhatsApp line | A tiny pop and tick | C |

## Mix and master

- The music is ducked by up to 4 dB under the SFX by an envelope follower. The music bus sits at about 0.52× (−5.7 dB) relative to the SFX.
- Master EQ (circular, so loop-safe): a 32 Hz high-pass, a −2 dB dip at 250 Hz against mud, and a +1 dB air shelf.
- A look-ahead limiter catches transients only. The worst gain reduction is −3.8 dB, at the 15.0 peak, and about 5 % of samples are reduced by more than 1 dB.
- Measured with ffmpeg ebur128:
  - `mix.wav`: −14.1 LUFS integrated, true peak −1.6 dBTP, LRA 4.3 LU.
  - Final mp4 (AAC 192k): −14.1 LUFS, true peak −1.5 dBTP.
- The stems (`music.wav`, `sfx.wav`) carry the same master gain but no limiter. Their sum is the pre-limiter mix.

## QA (numeric)

- **Files.** The mp4 has an h264 stream of 480 frames, bit-identical to the source (same stream MD5), plus AAC stereo 48 kHz at about 192 kb/s. Container duration is exactly 20.000 s, with `moov` before `mdat` (faststart).
- **Sync.** Onset detection on the 2 ms envelope (rise over the previous 20 ms) puts every cue within ±1 frame (±42 ms) in the mix.
- **Loop, first 0.5 s against last 0.5 s of the mix.**
  - RMS is −17.3 dB against −17.4 dB.
  - The octave-band spectral-shape correlation is 0.98.
  - The music stem alone matches within 0.4 dB in every band. It is 1.8 dB louder at the tail only because, at the head, it is ducked under the 0.0 bubble pop.
  - The seam has no sample discontinuity.
