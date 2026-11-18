#!/usr/bin/env python3
"""Kiwi Go hero Reel «Отправлено» — one-command build.

    python3 edit/build.py                 # graphics -> master + cut-down -> beats, poster, storyboards, QA
    python3 edit/build.py --only master   # one edit
    python3 edit/build.py --preview master 0,60,336   # write single frames to edit/build/preview/
    python3 edit/build.py --gfx           # force re-render of the Playwright graphics

Clips in brand-reel/gate3/S1..S5.mp4 are picked up automatically (config.json: shots.*.clip);
in-points, speeds and windows live in edit/config.json.
"""
import argparse
import json
import multiprocessing as mp
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel.common import EDIT_DIR, ROOT, BUILD, GFX_DIR, W, H, FPS, load_config, rp  # noqa: E402

NODE_PATHS = ['/opt/node-tools/node_modules', os.path.join(EDIT_DIR, 'node_modules')]
REEL = None


def render_gfx(force=False):
    meta = os.path.join(GFX_DIR, 'meta.json')
    cfgp = os.path.join(EDIT_DIR, 'config.json')
    srcs = [cfgp, os.path.join(EDIT_DIR, 'gfx', 'gfx.html'), os.path.join(EDIT_DIR, 'gfx', 'render_gfx.js')]
    if not force and os.path.exists(meta) and all(os.path.getmtime(meta) > os.path.getmtime(s) for s in srcs):
        return
    env = dict(os.environ)
    env['NODE_PATH'] = os.pathsep.join([p for p in NODE_PATHS if os.path.isdir(p)] + [env.get('NODE_PATH', '')])
    subprocess.run(['node', os.path.join(EDIT_DIR, 'gfx', 'render_gfx.js'), ROOT, GFX_DIR], check=True, env=env)


def _init():
    pass


def _work(args):
    edit, f = args
    img, meta = REEL.render(edit, f)
    return f, img.tobytes(), meta


def ffmpeg_writer(path):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '16',
           '-maxrate', '16M', '-bufsize', '32M', '-g', '48',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-pix_fmt', 'yuv420p',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
           '-r', str(FPS), '-an', '-movflags', '+faststart', path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def render_edit(cfg, name, workers, keep_frames=()):
    E = cfg['edits'][name]
    out = rp(E['out'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    p = ffmpeg_writer(out)
    metas = []
    t0 = time.time()
    kept = {}
    with mp.get_context('fork').Pool(workers) as pool:
        for f, buf, meta in pool.imap(_work, [(name, f) for f in range(E['frames'])], chunksize=2):
            p.stdin.write(buf)
            metas.append(meta)
            if f in keep_frames:
                kept[f] = buf
            if f % 48 == 0:
                print(f'  {name}: f{f:03d}  {time.time() - t0:5.1f}s', flush=True)
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError('ffmpeg failed')
    print(f'  {name}: {E["frames"]} frames in {time.time() - t0:.1f}s -> {out}')
    return metas, kept


def write_beats(cfg):
    from reel.beats import BEATS
    for name, txt in BEATS.items():
        path = rp(cfg['edits'][name]['beats'])
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', choices=['master', 'cutdown'])
    ap.add_argument('--preview', nargs=2, metavar=('EDIT', 'FRAMES'))
    ap.add_argument('--gfx', action='store_true')
    ap.add_argument('--workers', type=int, default=max(1, min(4, os.cpu_count() or 1)))
    ap.add_argument('--no-qa', action='store_true')
    a = ap.parse_args()
    global REEL
    cfg = load_config()
    print('graphics (Playwright/Onest)...')
    render_gfx(a.gfx)
    from reel.compose import Reel
    print('sources:')
    REEL = Reel(cfg)
    if a.preview:
        from PIL import Image
        d = os.path.join(BUILD, 'preview')
        os.makedirs(d, exist_ok=True)
        for f in [int(x) for x in a.preview[1].split(',')]:
            img, meta = REEL.render(a.preview[0], f)
            Image.fromarray(img).save(os.path.join(d, f'{a.preview[0]}_{f:03d}.png'))
            print(f, json.dumps(meta, ensure_ascii=False, default=str)[:300])
        return
    from reel import qa
    edits = [a.only] if a.only else ['master', 'cutdown']
    pf = cfg['poster']
    results = {}
    for name in edits:
        print(f'render {name}...')
        keep = (pf['frame'],) if name == pf['edit'] else ()
        metas, kept = render_edit(cfg, name, a.workers, keep)
        results[name] = metas
        if kept:
            from PIL import Image
            import numpy as np
            Image.fromarray(np.frombuffer(kept[pf['frame']], np.uint8).reshape(H, W, 3)).save(rp(pf['out']))
            print('  poster ->', rp(pf['out']))
    write_beats(cfg)
    if not a.no_qa:
        qa.run(cfg, REEL, results)


if __name__ == '__main__':
    main()
