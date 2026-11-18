# Kiwi Go hero Reel «Отправлено»: edit and compositing pipeline

This folder builds both exports from the clips plus our own graphics. It needs no AI generation and spends no credits.

## Re-render (one command)

```bash
cd kiwi-go-soon/brand-reel
python3 edit/build.py
```

This command:
1. renders the graphics through Playwright (Chromium canvas with Onest);
2. renders the master and the cut-down at 24 fps (1080×1920);
3. encodes them with H.264;
4. writes the beat sheets and the poster;
5. builds the storyboards and runs QA.

It takes about 4 minutes on 4 cores. No temporary frames are written to disk, because frames are piped straight to ffmpeg.

Options:
- `--only master|cutdown` renders one edit.
- `--preview master 0,60,336` writes single frames to `build/preview/`.
- `--gfx` forces a graphics re-render. Graphics are rebuilt automatically when `config.json` or `gfx/*` changes.

Requirements:
- python3 with numpy, scipy, opencv-python-headless, Pillow and fontTools
- ffmpeg and ffprobe
- node with `playwright` (Chromium)

`build.py` looks for Playwright in `/opt/node-tools/node_modules` and in `edit/node_modules`. To install it there: `npm i playwright && npx playwright install chromium` in `edit/`.

## When new or replacement clips arrive
- Put the clips in `brand-reel/gate3/` as `S1.mp4` … `S5.mp4`. Each shot's `shots.<S>.clip` list is searched in order, and the first file that exists is used. If none exists, the placeholder still with a Ken-Burns push is used.
- Clips are cover-fitted to 1080×1920: a 1912-px-tall clip is scaled by 1920/1912 and centre-cropped. Use `reframe` (zoom/dx/dy) to nudge the framing.
- Set the timing in `config.json`:
  - `edits.<edit>.segments[]`: `in` (source seconds), `speed`, and `retime: "ease"` (a speed ramp that never drops below `min_speed`, so frames are only dropped, never duplicated).
  - `shots.<S>.window`: the QA-approved usable range. QA fails if an edit reads outside it.
- **S6** is not a clip. Both AI takes failed, so S6 is the 2.5D fallback built from `gate2/S6-c.png` (`shots.S6.plate`):
  - A GrabCut matte splits the truck from the inpainted background.
  - The plate is shifted up so the rear wheel sits at (490, 800), with the paving extended below and the background mirrored on the right.
  - A parallax pan moves the background at 0.6×, the truck and paving at 1.0× and the foreground bush at 1.3×. The pan lands at 14.00 s (cut-down: 6.00 s).
  - HoughCircles finds the wheels once on the still. After that the plate transform gives them exactly.
  - Do **not** list `gate3/S6.mp4` or `S6-take1.mp4`. To use a future real S6 clip anyway, set `wheels.mode: "manual"` and fill in `wheels.keys`.
- **S3 trail**: `shots.S3.trail` holds:
  - `path`: the road centreline in native clip pixels of frame 0;
  - `head_keys_idx`: [source seconds, path index] for the trail head;
  - `fade_out`.

  An ORB+RANSAC homography (smoothed with Savitzky–Golay) keeps the trail glued to the ground. If S3 is replaced, re-place `path` on the new frame 0.
- **Copy, positions and timings** are all in `config.json`: `ui.*` holds the text and layout, and `edits.*` holds the in and out times. QA checks the copy against 07 §1.3–1.4 and the client decisions.

## Outputs (`edit/out/`)
- `kiwigo_reel_master_20s.mp4` (480 f) and `kiwigo_reel_cutdown_10s.mp4` (240 f):
  - H.264 High, yuv420p, Rec.709 tags, 24 fps, crf 16, `+faststart`
  - no audio stream
- `kiwigo_reel_master_20s_beats.txt` and `kiwigo_reel_cutdown_10s_beats.txt` (07 §1.5 and §1.6)
- `kiwigo_reel_poster.png`: the card at f420
- `storyboard_master.png` and `storyboard_cutdown.png`: 16 frames each, with the cyan text-safe box at x 80–900, y 270–1250
- `qa_report.json`, which checks:
  - copy, ё, NBSP and the single ✓
  - no lime text
  - Onest glyphs and measured widths against the plan
  - the 12-seed SVG, and that the card logo is pixel-exact against the SVG render
  - safe area and face overlap for every frame
  - clip windows
  - ffprobe spec, duplicate-frame ratio and the loop fog state

## Layout
- `config.json`: the single source for timing, copy, grade and transitions
- `gfx/`: `gfx.html` holds the canvas components (bubbles, supers, PiP and chips, card), and `render_gfx.js` drives them with Playwright
- `reel/`:
  - `sources.py`: clips, Ken-Burns stills, the S6 2.5D plate
  - `look.py`: the R6 grade, bloom, grain, fog, the R2 leak, whip, haze, glow and focus pull
  - `inworld.py`: the trail, the kiwi wheels and the sweep
  - `compose.py`: the layer order from 07 §5.2, the UI and the card
  - `qa.py` and `beats.py`
- `fonts/`: `onest-600.ttf` and `onest-700.ttf` (OFL; `OFL.txt`)
- `build/`: the cache (graphics PNGs, the S6 matte). It is safe to delete.
