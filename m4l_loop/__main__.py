"""m4l-loop: iterate a Max for Live device in a running Live until it matches its design.

  python -m m4l_loop setup  DEVICE      install externals, JS and the remote script; build
  python -m m4l_loop build  DEVICE      write the .amxd and swap it into Live (keeps its settings)
  python -m m4l_loop ref    DEVICE      render the design reference
  python -m m4l_loop snap   DEVICE      capture Live, compare with the design, write the report
  python -m m4l_loop loop   DEVICE      build + snap
  python -m m4l_loop watch  DEVICE      loop on every save of the device or its JS
  python -m m4l_loop record DEVICE SECONDS [--extra PTS]
                                        screen-record the device (plus PTS to its right)
  python -m m4l_loop freeze DEVICE [--out PATH]
                                        one self-contained .amxd with its scripts and externals inside
  python -m m4l_loop live '{"cmd": "state"}'
                                        send a raw command to the remote script

DEVICE is a device spec: a .py file with NAME, WIDTH, REFERENCE, ELEMENTS, build() and optionally
JS, EXTERNALS, HEIGHT. See examples/mackity/device.py. Output goes to ./m4l-loop-out/NAME/.
"""
import argparse, importlib.util, json, os, shutil, sys, time

import cv2

from . import capture, compare, freeze, live, patch, trace

OUT = os.path.abspath('m4l-loop-out')


def load(path):
    spec = importlib.util.spec_from_file_location('device_spec', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DIR = os.path.dirname(os.path.abspath(path))
    mod.HEIGHT = getattr(mod, 'HEIGHT', patch.DEVICE_H)
    mod.OUT = os.path.join(OUT, mod.NAME)
    os.makedirs(mod.OUT, exist_ok=True)
    return mod


def files(dev, attr):
    return [os.path.join(dev.DIR, os.path.expanduser(f)) for f in getattr(dev, attr, [])]


def install_assets(dev):
    """Externals and JS go into a Max package, where Max finds them. Max only indexes new files at
    launch, so a file added for the first time needs one Live restart."""
    for src in files(dev, 'EXTERNALS'):
        if not src.endswith('.mxo'):      # Windows builds are only for freezing
            continue
        dst = os.path.join(live.PKG, 'externals', os.path.basename(src))
        if not os.path.exists(src):
            print('  missing external (build it first):', src)
        elif not os.path.exists(dst):
            shutil.copytree(src, dst)
    for src in files(dev, 'JS'):
        os.makedirs(os.path.join(live.PKG, 'javascript'), exist_ok=True)
        shutil.copy2(src, os.path.join(live.PKG, 'javascript', os.path.basename(src)))


def cmd_setup(dev):
    install_assets(dev)
    live.install_script()
    if live.send({'cmd': 'ping'}, wait=1.0):
        print('M4LLoop is running in Live.')
    else:
        print('Once: restart Live, then pick "M4LLoop" as a Control Surface in Settings > Link, Tempo & MIDI '
              '(Input and Output: None). Then run build.')
    cmd_build(dev)


def cmd_build(dev):
    install_assets(dev)
    path = os.path.join(live.device_folder(), dev.NAME + '.amxd')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    patch.write_amxd(path + '.tmp', dev.build())
    os.replace(path + '.tmp', path)
    mark = os.path.getsize(live.live_log())
    msg = {'cmd': 'reload', 'folder': live.FOLDER, 'file': dev.NAME + '.amxd', 'device': dev.NAME}
    r = live.send(msg)
    for _ in range(20):                       # Live's browser takes a few seconds to index a new file
        if not r or 'not in the browser' not in r['msg']:
            break
        time.sleep(1)
        r = live.send(msg)
    print('built', path, '->', r['msg'] if r else 'Live did not answer (is M4LLoop selected?)')
    time.sleep(1.5)
    for line in live.max_messages(mark):
        print('  max:', line)


def cmd_ref(dev, zoom, theme):
    return capture.render_reference(os.path.join(dev.DIR, dev.REFERENCE), dev.WIDTH, dev.HEIGHT, zoom, theme,
                                    os.path.join(dev.OUT, 'ref.png'))


def cmd_snap(dev, theme):
    win, _ = capture.screenshot(dev.OUT)
    side_pad = 0 if getattr(dev, 'NATIVE', False) else capture.SIDE_PAD
    z, x, y, ref, score = capture.locate(win, lambda zoom: cmd_ref(dev, zoom, theme), dev.OUT, side_pad)
    h, w = ref.shape[:2]
    live_img = win[y:y + h, x:x + w]
    cv2.imwrite(os.path.join(dev.OUT, 'live.png'), live_img)
    report = compare.compare(dev.OUT, ref, live_img, 2 * z)
    report['elements'] = compare.elements(getattr(dev, 'ELEMENTS', {}), ref, live_img, 2 * z)
    report.update(zoom=z, match=round(float(score), 4), where=[int(x), int(y)])
    json.dump(report, open(os.path.join(dev.OUT, 'report.json'), 'w'), indent=1)
    print(f"match {report['match_pct']} %  (sheet: {os.path.join(dev.OUT, 'compare.png')})")
    for name, e in report['elements'].items():
        print(f"  {name:16} off by {e['live_is_off_by']}  residual {e['residual']}")


def cmd_record(dev, seconds, extra):
    """Record the located device (from the last snap) plus `extra` points to its right."""
    report = json.load(open(os.path.join(dev.OUT, 'report.json')))
    _, (bx, by, _, _) = capture.live_window(dev.OUT)
    x, y = report['where']
    s = 2 * report['zoom']
    region = (bx + x / 2 - 4, by + y / 2 - 20 * report['zoom'], dev.WIDTH * s / 2 + 8 + extra, (dev.HEIGHT + 22) * s / 2)
    path = os.path.join(dev.OUT, 'record.mov')
    trace.record(seconds, path, region)
    json.dump({'region_points': region}, open(os.path.join(dev.OUT, 'record.json'), 'w'))
    print('recorded', path, 'region', [round(v) for v in region])


def cmd_freeze(dev, out):
    out = os.path.expanduser(out or os.path.join('~/Desktop', dev.NAME + '.amxd'))
    missing = [f for f in files(dev, 'EXTERNALS') + files(dev, 'JS') if not os.path.exists(f)]
    if missing:
        raise SystemExit('missing: ' + ', '.join(missing))
    parts = freeze.freeze(dev.build(), dev.NAME, out, files(dev, 'JS'), files(dev, 'EXTERNALS'))
    print('froze', out, f'({os.path.getsize(out) // 1024} KB)')
    for name, size in parts:
        print(f'  {name:32} {size:>9} bytes')


def cmd_watch(dev, path, theme):
    watched = [path] + files(dev, 'JS')
    seen = {f: os.path.getmtime(f) for f in watched}
    cmd_build(dev)
    cmd_snap(dev, theme)
    while True:
        time.sleep(0.5)
        if any(os.path.getmtime(f) != seen[f] for f in watched):
            seen = {f: os.path.getmtime(f) for f in watched}
            dev = load(path)
            cmd_build(dev)
            cmd_snap(dev, theme)


def main():
    ap = argparse.ArgumentParser(prog='m4l_loop', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['setup', 'build', 'ref', 'snap', 'loop', 'watch', 'record', 'freeze', 'live'])
    ap.add_argument('target', help='device spec .py, or a JSON command for "live"')
    ap.add_argument('seconds', nargs='?', type=float, default=4)
    ap.add_argument('--theme', default='dark', choices=['dark', 'light', 'light-cool'])
    ap.add_argument('--zoom', type=float, default=2.0, help='ref: screen px per body px')
    ap.add_argument('--extra', type=float, default=0, help='record: screen points to include right of the device')
    ap.add_argument('--out', help='freeze: output path, default ~/Desktop/NAME.amxd')
    a = ap.parse_args()
    if a.cmd == 'live':
        print(json.dumps(live.send(json.loads(a.target)), indent=1))
        return
    dev = load(a.target)
    if a.cmd == 'setup':
        cmd_setup(dev)
    elif a.cmd == 'build':
        cmd_build(dev)
    elif a.cmd == 'ref':
        cmd_ref(dev, a.zoom, a.theme)
        print(os.path.join(dev.OUT, 'ref.png'))
    elif a.cmd == 'snap':
        cmd_snap(dev, a.theme)
    elif a.cmd == 'loop':
        cmd_build(dev)
        cmd_snap(dev, a.theme)
    elif a.cmd == 'watch':
        cmd_watch(dev, a.target, a.theme)
    elif a.cmd == 'freeze':
        cmd_freeze(dev, a.out)
    elif a.cmd == 'record':
        cmd_record(dev, a.seconds, a.extra)


if __name__ == '__main__':
    sys.exit(main())
