"""Compare a Live capture with the design render: difference map, mismatch regions, per-element offsets."""
import os

import cv2
import numpy as np

TOLERANCE = 40     # max channel difference that still counts as a match


def offset(ref, live, x, y, w, h, scale, reach=6):
    """Slide the Live patch over the design patch; returns the best shift in body px
    ('live_is_off_by') and how different it still looks after that shift ('residual')."""
    m = int(reach * scale)
    H, W = ref.shape[:2]
    x0, y0, x1, y1 = max(0, x - m), max(0, y - m), min(W, x + w + m), min(H, y + h + m)
    a = ref[y0:y1, x0:x1].astype(int)
    base = float(np.abs(a - live[y0:y1, x0:x1].astype(int)).mean())
    best = (base, 0, 0)
    for dy in range(-m, m + 1):
        for dx in range(-m, m + 1):
            if y0 + dy < 0 or x0 + dx < 0 or y1 + dy > H or x1 + dx > W:
                continue
            e = float(np.abs(a - live[y0 + dy:y1 + dy, x0 + dx:x1 + dx].astype(int)).mean())
            if e < best[0]:
                best = (e, dx, dy)
    e, dx, dy = best
    moved = (dx or dy) and e < base * 0.7
    return {'live_is_off_by': [round(dx / scale, 1), round(dy / scale, 1)] if moved else [0, 0],
            'residual': round(e, 1)}


def elements(boxes, ref, live, scale):
    return {name: offset(ref, live, *(int(round(v * scale)) for v in box), scale, reach=4)
            for name, box in boxes.items()}


def compare(out_dir, ref, live, scale):
    """Writes compare.png (design | Live | difference) and returns match % and mismatch regions."""
    diff = cv2.absdiff(ref, live).max(axis=2)
    bad = cv2.morphologyEx((diff > TOLERANCE).astype(np.uint8), cv2.MORPH_CLOSE,
                           np.ones((int(3 * scale),) * 2, np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(bad)
    regions = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < scale * scale * 2:
            continue
        r = dict(x=round(x / scale, 1), y=round(y / scale, 1), w=round(w / scale, 1), h=round(h / scale, 1),
                 px=int(area))
        r.update(offset(ref, live, x, y, w, h, scale))
        regions.append(r)
    regions.sort(key=lambda r: -r['px'])

    heat = cv2.applyColorMap(cv2.convertScaleAbs(diff, alpha=2.0), cv2.COLORMAP_INFERNO)
    for r in regions[:12]:
        cv2.rectangle(heat, (int(r['x'] * scale), int(r['y'] * scale)),
                      (int((r['x'] + r['w']) * scale), int((r['y'] + r['h']) * scale)), (0, 255, 0), 1)
    gap = np.full((ref.shape[0], 8, 3), 255, np.uint8)
    sheet = np.hstack([ref, gap, live, gap, heat])
    label = np.full((28, sheet.shape[1], 3), 255, np.uint8)
    for i, t in enumerate(('design', 'Live', 'difference')):
        cv2.putText(label, t, (8 + i * (ref.shape[1] + 8), 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)
    cv2.imwrite(os.path.join(out_dir, 'compare.png'), np.vstack([label, sheet]))
    return {'match_pct': round(100 * float((diff <= TOLERANCE).mean()), 2), 'regions': regions[:12]}
