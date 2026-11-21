"""A device's layout, once: where each component sits, in design body px. The design page draws from it
and the Max build places objects from it. Only geometry lives here; drawing and behaviour stay in code."""
import json, os

# Max rect for a component placed at design geometry, measured in Live 12.4 at 100 %
MAX_RECT = {
    'display': lambda e: e['rect'],
    'graph':   lambda e: e['rect'],
    'meter':   lambda e: e['rect'],
    'led':     lambda e: [e['cx'] - 4.5, e['cy'] - 4.5, 9, 9],
    'text':    lambda e: [e['x'] - 4, e['cap'] - 5, 30, 18],                     # live.comment inset
    'button':  lambda e: [e['rect'][0] - 1, e['rect'][1] - 1, e['rect'][2] + 2, e['rect'][3] + 2],  # live.text border inset
    'dial':    lambda e: [e['cx'] - 23, e['cap'] - 1.5, 48, 48],               # live.dial ring and label offsets
}

# boxes to measure per component, in design body px
MEASURE = {
    'display': lambda e: {'': grow(e['rect'], 2)},
    'graph':   lambda e: {'': e['rect']},
    'meter':   lambda e: {'': grow(e['rect'], 2)},
    'led':     lambda e: {'': [e['cx'] - 4.5, e['cy'] - 4.5, 9, 9]},
    'text':    lambda e: {'': [e['x'] - 1, e['cap'] - 1.5, 6 * len(e['text']) + 2, 12]},
    'button':  lambda e: {'': grow(e['rect'], 2)},
    'dial':    lambda e: {' label': [e['cx'] - 18, e['cap'] - 3, 36, 10], ' ring': [e['cx'] - 18.5, e['cap'] + 7, 37, 30],
                          ' value': [e['cx'] - 20, e['cap'] + 31, 40, 12]},
}


def grow(r, n):
    return [r[0] - n, r[1] - n, r[2] + 2 * n, r[3] + 2 * n]


class Layout:
    def __init__(self, path):
        data = json.load(open(path))
        self.path, self.width, self.el = path, data['width'], data['elements']

    def rect(self, name):
        e = self.el[name]
        return MAX_RECT[e['type']](e)

    def elements(self):
        return {name + suffix: box for name, e in self.el.items() for suffix, box in MEASURE[e['type']](e).items()}

    def write_js(self):
        """layout.js beside layout.json, so a design page can load it with <script src> (file:// can't fetch)."""
        js = os.path.join(os.path.dirname(self.path), 'layout.js')
        open(js, 'w').write('window.LAYOUT = ' + json.dumps({'width': self.width, 'elements': self.el}) + ';\n')
