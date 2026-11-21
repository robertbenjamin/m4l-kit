"""Write Max for Live devices (.amxd) from Python: boxes, patch cords, parameters."""
import json, struct

DEVICE_H = 169


class Patch:
    def __init__(self):
        self.boxes, self.lines, self.params = [], [], {}
        self.n = 0

    def box(self, **kw):
        self.n += 1
        kw.setdefault('id', f'obj-{self.n}')
        kw.setdefault('numinlets', 1)
        kw.setdefault('numoutlets', 0)
        self.boxes.append({'box': kw})
        return kw['id']

    def obj(self, text, rect, ins, outs, outtypes=None):
        return self.box(maxclass='newobj', text=text, patching_rect=rect, numinlets=ins,
                        numoutlets=outs, outlettype=outtypes or [''] * outs,
                        fontname='Arial Bold', fontsize=10.0)

    def connect(self, a, ao, b, bi):
        self.lines.append({'patchline': {'source': [a, ao], 'destination': [b, bi]}})

    def patcher(self, width, banks=None, description=''):
        p = template_patcher(width)
        p['boxes'], p['lines'], p['description'] = self.boxes, self.lines, description
        p['parameters'] = dict(self.params)
        if banks:
            p['parameters']['parameterbanks'] = banks
        return {'patcher': p}


def template_patcher(width, height=DEVICE_H):
    return {
        'fileversion': 1,
        'appversion': {'major': 9, 'minor': 1, 'revision': 5, 'architecture': 'x64', 'modernui': 1},
        'classnamespace': 'box',
        'rect': [100.0, 100.0, 1200.0, 600.0],
        'openrect': [0.0, 0.0, float(width), float(height)],
        'bglocked': 0, 'openinpresentation': 1,
        'default_fontsize': 10.0, 'default_fontface': 0, 'default_fontname': 'Arial Bold',
        'gridonopen': 1, 'gridsize': [8.0, 8.0], 'gridsnaponopen': 1, 'objectsnaponopen': 1,
        'statusbarvisible': 2, 'toolbarvisible': 1, 'lefttoolbarpinned': 0, 'toptoolbarpinned': 0,
        'righttoolbarpinned': 0, 'bottomtoolbarpinned': 0, 'toolbars_unpinned_last_save': 0,
        'tallnewobj': 0, 'boxanimatetime': 500, 'enablehscroll': 1, 'enablevscroll': 1,
        'devicewidth': float(width), 'description': '', 'digest': '', 'tags': '', 'style': '',
        'subpatcher_template': '', 'assistshowspatchername': 0,
        'dependency_cache': [], 'latency': 0, 'autosave': 0,
        'project': {'version': 1, 'creationdate': 3590052493, 'modificationdate': 3590052493,
                    'viewrect': [0.0, 0.0, 300.0, 500.0], 'autoorganize': 1, 'hideprojectwindow': 1,
                    'showdependencies': 1, 'autolocalize': 0, 'contents': {'patchers': {}},
                    'layout': {}, 'searchpath': {}, 'detailsvisible': 0, 'amxdtype': 1633771873,
                    'readonly': 0, 'devpathtype': 0, 'devpath': '.', 'sortmode': 0, 'viewmode': 0},
    }


def write_amxd(path, patch):
    body = json.dumps(patch, indent='\t').encode('utf8') + b'\n\x00'
    head = b'ampf' + struct.pack('<I', 4) + b'aaaa' + b'meta' + struct.pack('<I', 4) + struct.pack('<I', 0)
    with open(path, 'wb') as f:
        f.write(head + b'ptch' + struct.pack('<I', len(body)) + body)
