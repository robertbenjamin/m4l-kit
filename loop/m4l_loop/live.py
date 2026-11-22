"""Talk to Live: the M4LLoop remote script, Live's User Library and its log."""
import glob, json, os, re, shutil, socket

PORT = 39123
FOLDER = ['Presets', 'Audio Effects', 'Max Audio Effect', 'm4l-loop']
PKG = os.path.expanduser('~/Documents/Max 9/Packages/m4l-loop')
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'remote_script', 'M4LLoop')


def user_library():
    """The User Library Live is set to use (Library.cfg), which may not be ~/Music."""
    for cfg in sorted(glob.glob(os.path.expanduser('~/Library/Preferences/Ableton/Live */Library.cfg')),
                      key=os.path.getmtime, reverse=True):
        block = re.search(r'<UserLibrary>(.*?)</UserLibrary>', open(cfg, errors='ignore').read(), re.S)
        if not block:
            continue
        path = re.search(r'<ProjectPath Value="([^"]*)"', block[1])
        name = re.search(r'<ProjectName Value="([^"]*)"', block[1])
        lib = path and os.path.join(path[1], name[1] if name else 'User Library')
        if lib and os.path.isdir(lib):
            return lib
    return os.path.expanduser('~/Music/Ableton/User Library')


def device_folder():
    return os.path.join(user_library(), *FOLDER)


def install_script():
    """Copy the remote script into both Remote Scripts folders: Live skips symlinked scripts.
    handler.py is re-imported on every command; __init__.py changes need a Live restart."""
    for lib in {user_library(), os.path.expanduser('~/Music/Ableton/User Library')}:
        dst = os.path.join(lib, 'Remote Scripts', 'M4LLoop')
        os.makedirs(dst, exist_ok=True)
        for f in ('__init__.py', 'handler.py'):
            shutil.copy2(os.path.join(SCRIPT, f), os.path.join(dst, f))


def send(msg, wait=5.0):
    """One command to the remote script; returns its JSON reply, or None if Live isn't listening."""
    install_script()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(wait)
    try:
        s.sendto(json.dumps(msg).encode(), ('127.0.0.1', PORT))
        return json.loads(s.recvfrom(65536)[0])
    except (socket.timeout, ConnectionRefusedError):
        return None
    finally:
        s.close()


def live_log():
    return max(glob.glob(os.path.expanduser('~/Library/Preferences/Ableton/Live */Log.txt')), key=os.path.getmtime)


def max_messages(mark):
    """Max's console is hidden inside Live, but Live copies it into Log.txt."""
    with open(live_log(), errors='ignore') as f:
        f.seek(mark)
        return [l.split('Message from Max: ', 1)[1].rstrip() for l in f if 'Message from Max' in l]
