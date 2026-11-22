"""Write a frozen (self-contained) .amxd: the patch plus every file it needs in one file, laid out the way
Max freezes devices, so it loads on a machine without the externals or scripts installed.

Layout: 'ampf' header, then a 'ptch' chunk holding an 'mx@c' container: a 16-byte header, the files back to
back, and a 'dlst' directory of 'dire' entries (type, name, size, offset, flags, date). A macOS external is
stored as four entries: a marker plus the bundle's zip, executable and Info.plist; a Windows x64
external (.mxe64) is one entry. Ship both so the device loads on either system."""
import copy, io, json, os, plistlib, struct, time, zipfile

MXO_MARKER = b'\x00\x00\x00\xd0'
MAC_EPOCH = 2082844800        # seconds from 1904 (Mac) to 1970 (Unix)


def chunk(tag, data):
    return tag + struct.pack('>I', 8 + len(data)) + data


def name_field(name):
    raw = name.encode('utf8') + b'\x00'
    return raw + b'\x00' * (-len(raw) % 4)


def mxo_parts(path):
    """(executable, plist, zip of the bundle) for a .mxo bundle."""
    base = os.path.basename(path.rstrip('/'))
    plist_path = os.path.join(path, 'Contents', 'Info.plist')
    plist = open(plist_path, 'rb').read()
    exe = open(os.path.join(path, 'Contents', 'MacOS', plistlib.loads(plist)['CFBundleExecutable']), 'rb').read()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(path):
            r = os.path.relpath(root, path)
            rel = base if r == '.' else os.path.join(base, r)
            z.writestr(rel + '/', b'')
            for f in sorted(files):
                z.write(os.path.join(root, f), os.path.join(rel, f))
    return exe, plist, buf.getvalue()


def ext_type(path):
    return b'mx64' if path.endswith('.mxe64') else b'iLaX'


def freeze(patch, name, out, scripts=(), externals=(), device_type=b'aaaa'):
    """patch: the device's patcher dict. scripts: .js paths. externals: .mxo bundle paths."""
    patch = copy.deepcopy(patch)
    p = patch['patcher']
    p['dependency_cache'] = (
        [{'name': os.path.basename(s), 'bootpath': os.path.dirname(s), 'type': 'TEXT', 'implicit': 1} for s in scripts]
        + [{'name': os.path.basename(e.rstrip('/')), 'type': ext_type(e).decode()} for e in externals])
    p['project']['contents'] = {
        'patchers': {},
        'code': {os.path.basename(s): {'kind': 'javascript', 'local': 1} for s in scripts},
        'externals': {os.path.basename(e.rstrip('/')): {'kind': 'object', 'local': 1} for e in externals}}

    files = [(name + '.amxd', b'JSON', json.dumps(patch, indent='\t').encode('utf8') + b'\n\x00', 17)]
    files += [(os.path.basename(s), b'TEXT', open(s, 'rb').read(), 0) for s in scripts]
    for e in externals:
        if e.endswith('.mxe64'):
            files.append((os.path.basename(e), b'mx64', open(e, 'rb').read(), 0))
            continue
        stem = os.path.basename(e.rstrip('/'))[:-4]
        exe, plist, zipped = mxo_parts(e)
        files += [(stem + '.mxo', b'iLaX', MXO_MARKER, 0), (stem + '/zipfile', b'\x00' * 4, zipped, 0),
                  (stem + '/executable', b'\x00' * 4, exe, 0), (stem + '/plist', b'\x00' * 4, plist, 0)]

    now = int(time.time()) + MAC_EPOCH
    body, entries, offset = b'', b'', 16
    for fname, ftype, data, flag in files:
        entries += chunk(b'dire', chunk(b'type', ftype) + chunk(b'fnam', name_field(fname))
                         + chunk(b'sz32', struct.pack('>I', len(data))) + chunk(b'of32', struct.pack('>I', offset))
                         + chunk(b'vers', struct.pack('>I', 0)) + chunk(b'flag', struct.pack('>I', flag))
                         + chunk(b'mdat', struct.pack('>I', now)))
        body += data
        offset += len(data)
    container = b'mx@c' + struct.pack('>III', 16, 0, 16 + len(body)) + body + chunk(b'dlst', entries)
    head = b'ampf' + struct.pack('<I', 4) + device_type + b'meta' + struct.pack('<I', 4) + struct.pack('<I', 7)
    with open(out, 'wb') as f:
        f.write(head + b'ptch' + struct.pack('<I', len(container)) + container)
    return [(fname, len(data)) for fname, _, data, _ in files]
