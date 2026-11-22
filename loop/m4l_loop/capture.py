"""Screenshots of Live, renders of the design, and finding the device in a screenshot."""
import os, subprocess

import cv2
import numpy as np

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SIDE_PAD = 2       # a Max device's body is 2 px wider than its content on each side (native devices: 0)
ZOOMS = (1.0, 1.1, 1.25, 1.5, 1.75, 2.0)
HERE = os.path.dirname(os.path.abspath(__file__))


def live_window(out_dir):
    """(window id, (x, y, w, h) in screen points) of Live's main window."""
    exe = os.path.join(out_dir, 'winlist')
    if not os.path.exists(exe):
        os.makedirs(out_dir, exist_ok=True)
        subprocess.run(['swiftc', '-O', os.path.join(HERE, 'winlist.swift'), '-o', exe], check=True)
    rows = [l.split('\t') for l in subprocess.run([exe], capture_output=True, text=True).stdout.splitlines()]
    rows = [r for r in rows if r[1] == 'Live' and r[2]]
    if not rows:
        raise SystemExit('Live window not found')
    wid, _, _, bounds = max(rows, key=lambda r: int(r[3].split(',')[2]) * int(r[3].split(',')[3]))
    return wid, tuple(int(v) for v in bounds.split(','))


def screenshot(out_dir):
    wid, bounds = live_window(out_dir)
    path = os.path.join(out_dir, 'window.png')
    subprocess.run(['screencapture', '-x', '-o', f'-l{wid}', path], check=True)
    return cv2.imread(path), bounds


def render_reference(page, width, height, zoom, theme, out):
    """Render the design's reference page and crop it to the device body (page background is magenta)."""
    raw = out + '.raw.png'
    subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--force-device-scale-factor=1',
                    f'--window-size={int(width * zoom) + 40},{int(height * zoom) + 40}', f'--screenshot={raw}',
                    f'file://{os.path.abspath(page)}?ref=1&zoom={zoom}&theme={theme}'],
                   capture_output=True, check=True)
    im = cv2.imread(raw)
    ys, xs = np.nonzero(~np.all(im == (255, 0, 255), axis=2))
    ref = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(out, ref)
    return ref


def locate(win, render, out_dir, side_pad=SIDE_PAD):
    """Find the device in the window at whichever zoom Live uses; returns (zoom, x, y, ref) with x, y the
    content origin in window px. The last zoom found is tried first."""
    zf = os.path.join(out_dir, 'zoom.txt')
    zooms = ZOOMS
    if os.path.exists(zf):
        z0 = float(open(zf).read())
        zooms = (z0,) + tuple(z for z in zooms if z != z0)
    best = None
    for z in zooms:
        ref = render(2 * z)
        _, score, _, loc = cv2.minMaxLoc(cv2.matchTemplate(win, ref, cv2.TM_CCOEFF_NORMED))
        if best is None or score > best[0]:
            best = (score, z, loc, ref)
        if score > 0.7:
            break
    score, z, (x, y), ref = best
    open(zf, 'w').write(str(z))
    ref = render(2 * z)
    x, y = content_origin(win, x, y, 2 * z, side_pad)
    return z, x, y, ref, score


def content_origin(win, x, y, scale, side_pad=SIDE_PAD):
    """Snap a rough match to the device's real edges by walking out through the plain body colour
    in the side pad and above the dial row, whatever the content looks like."""
    row = y + int(140 * scale)
    left = x + int(2 * scale)
    body = win[row, left].astype(int)
    same = lambda px: int(abs(px.astype(int) - body).max()) < 4
    while same(win[row, left - 1]):
        left -= 1
    top = row
    while same(win[top - 1, left + 1]):
        top -= 1
    return left + int(side_pad * scale), top
