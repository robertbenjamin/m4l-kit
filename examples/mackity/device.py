"""Mackity (Airwindows console saturation), built to its approved design in design.html.

Rects are design body px, which are Max presentation coordinates.
Drive dB is the drive gain in dB: (10A)^2 = 10^(dB/20), so A = 10^((dB-40)/40).
Audio needs the aw.mackity~ external, an Airwindows port built outside this repo (point AW_EXTERNALS at it).
Without it the device still loads and draws, so the visual loop works; it just passes no audio.
"""
import os

from m4l_loop.layout import Layout
from m4l_loop.patch import Patch

L = Layout(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'layout.json'))

NAME = 'Mackity'
REFERENCE = 'design.html'
JS = ['mackity_display.js']
EXTERNALS = [os.path.join(os.environ.get('AW_EXTERNALS', '~/Work/airwindows-m4l/dist/externals'), 'aw.mackity~.mxo')]
WIDTH = L.width
FONT = dict(fontname='Ableton Sans Small', fontsize=10.0, fontface=0)
ORANGE = {'expression': 'themecolor.live_display_handle_one'}
LCD_BG = {'expression': 'themecolor.live_lcd_bg'}
LCD_TOGGLE = {k: ORANGE for k in ('bordercolor', 'focusbordercolor', 'textcolor', 'activetextcolor',
                                   'bgoncolor', 'activebgoncolor')}
LCD_TOGGLE.update(textoncolor=LCD_BG, activetextoncolor=LCD_BG)


ELEMENTS = L.elements()


def build():
    P = Patch()
    obj = P.obj
    plugin = obj('plugin~', [30, 20, 60, 20], 2, 2, ['signal', 'signal'])
    aw = obj('aw.mackity~', [30, 400, 120, 20], 2, 3, ['signal', 'signal', ''])
    mk = [obj('*~ 1.', [30 + 80 * i, 440, 50, 20], 2, 1, ['signal']) for i in (0, 1)]
    plugout = obj('plugout~', [30, 500, 60, 20], 2, 2, ['signal', 'signal'])
    for i in (0, 1):
        P.connect(plugin, i, aw, i)
        P.connect(aw, i, mk[i], 0)
        P.connect(mk[i], 0, plugout, i)

    P.box(maxclass='panel', mode=0, border=0, rounded=2, bgfillcolor=[.09, .09, .09, 1.0],
          saved_attribute_attributes={'bgfillcolor': {'expression': 'themecolor.live_lcd_bg'}},
          patching_rect=[600, 20, 40, 20], background=1, presentation=1, presentation_rect=L.rect('display'))
    disp = P.box(maxclass='v8ui', filename='mackity_display.js', jsarguments=['curve'], numinlets=1,
                 numoutlets=1, outlettype=[''], border=0, ignoreclick=1, patching_rect=[600, 60, 100, 84],
                 presentation=1, presentation_rect=L.rect('curve'))
    led = P.box(maxclass='v8ui', filename='mackity_display.js', jsarguments=['led'], numinlets=1,
                numoutlets=1, outlettype=[''], border=0, ignoreclick=1, patching_rect=[720, 60, 9, 9],
                presentation=1, presentation_rect=L.rect('clip light'))
    P.box(maxclass='live.comment', text=L.el['clip label']['text'], textjustification=0, textcolor=[.46, .46, .46, 1.0],
          saved_attribute_attributes={'textcolor': {'expression': 'themecolor.live_lcd_control_fg_zombie'}},
          patching_rect=[740, 60, 40, 18], presentation=1, presentation_rect=L.rect('clip label'), **FONT)
    # live.meter~ is mono and paints over anything near it: two bars, framed by a v8ui, no clip tick
    mx, my, mw, mh = L.rect('meter')
    meters = [P.box(maxclass='live.meter~', numinlets=1, numoutlets=1, outlettype=['list'],
                    patching_rect=[800 + 10 * i, 60, 4, mh - 2], presentation=1, bgcolor=[0, 0, 0, 0],
                    presentation_rect=[mx + 1 + 5 * i, my + 1, 4, mh - 2]) for i in (0, 1)]
    P.box(maxclass='v8ui', filename='mackity_display.js', jsarguments=['meterframe'], numinlets=1,
          numoutlets=1, outlettype=[''], border=0, ignoreclick=1, patching_rect=[820, 60, 11, 84],
          presentation=1, presentation_rect=L.rect('meter'))
    for i in (0, 1):
        P.connect(mk[i], 0, meters[i], 0)

    def param(long, short, rect, **va):
        va.update(parameter_longname=long, parameter_shortname=short)
        return P.box(maxclass='live.dial', varname=long, parameter_enable=1, numinlets=1, numoutlets=2,
                     outlettype=['', 'float'], patching_rect=[30 + 200 * len(P.params), 100, 48, 48],
                     presentation=1, presentation_rect=rect, saved_attribute_attributes={'valueof': va})

    # exponent puts 0 dB at 10 % of the travel, where the design's raw default 0.1 sits
    drive = param('Drive', 'Drive', L.rect('drive'), parameter_type=0, parameter_mmin=-40.,
                  parameter_mmax=40., parameter_initial=[0.001], parameter_initial_enable=1, parameter_unitstyle=4,
                  parameter_exponent=0.30103)   # initial 0.001: the exponent round trip shows 0 as "-0.0 dB"
    out = param('Output', 'Output', L.rect('output'), parameter_type=0, parameter_mmin=-70.,
                parameter_mmax=0., parameter_initial=[0.], parameter_initial_enable=1, parameter_unitstyle=4,
                parameter_exponent=3.)
    P.params[drive] = ['Drive', 'Drive', 0]
    P.params[out] = ['Output', 'Output', 0]
    makeup = P.box(maxclass='live.text', varname='Makeup', text='Makeup', texton='Makeup', mode=1,
                   parameter_enable=1, numinlets=1, numoutlets=2, outlettype=['', ''],
                   patching_rect=[440, 100, 55, 15], presentation=1, presentation_rect=L.rect('makeup'),
                   saved_attribute_attributes={'valueof': dict(parameter_longname='Makeup', parameter_shortname='Makeup',
                                                               parameter_type=2, parameter_enum=['off', 'on'],
                                                               parameter_mmax=1, parameter_initial=[0],
                                                               parameter_initial_enable=1), **LCD_TOGGLE},
                   bgcolor=[0, 0, 0, 0], activebgcolor=[0, 0, 0, 0], **FONT)
    P.params[makeup] = ['Makeup', 'Makeup', 0]

    a = obj('expr pow(10.\\, ($f1 - 40.) / 40.)', [30, 200, 180, 20], 1, 1)
    P.connect(drive, 0, a, 0)
    P.connect(a, 0, obj('prepend param 0', [30, 300, 100, 20], 1, 1), 0)
    P.connect(P.boxes[-1]['box']['id'], 0, aw, 0)
    pd = obj('prepend drive', [230, 200, 90, 20], 1, 1)
    P.connect(a, 0, pd, 0)
    P.connect(pd, 0, disp, 0)
    b = obj('dbtoa', [230, 260, 50, 20], 1, 1)
    P.connect(out, 0, b, 0)
    pb = obj('prepend param 1', [230, 300, 100, 20], 1, 1)
    P.connect(b, 0, pb, 0)
    P.connect(pb, 0, aw, 0)
    comp = obj('expr ($i2 != 0) * pow(10.\\, -$f1 / 20.) + ($i2 == 0)', [440, 200, 200, 20], 2, 1)
    P.connect(makeup, 0, comp, 1)
    P.connect(drive, 0, comp, 0)
    tb = obj('t b i', [440, 160, 40, 20], 1, 2, ['bang', 'int'])
    P.connect(makeup, 0, tb, 0)
    P.connect(tb, 1, comp, 1)
    P.connect(tb, 0, drive, 0)
    for i in (0, 1):
        P.connect(comp, 0, mk[i], 1)

    # stand-in until aw.mackity~ reports its own clamp hits
    pk = [obj('peakamp~ 33', [700 + 90 * i, 300, 80, 20], 2, 1, ['float']) for i in (0, 1)]
    mx = obj('maximum 0.', [700, 330, 60, 20], 2, 1, ['float'])
    for i in (0, 1):
        P.connect(plugin, i, pk[i], 0)
    P.connect(pk[0], 0, mx, 0)
    P.connect(pk[1], 0, mx, 1)
    gain = obj('dbtoa', [800, 230, 50, 20], 1, 1)
    P.connect(drive, 0, gain, 0)
    driven = obj('* 0.', [700, 360, 40, 20], 2, 1)
    P.connect(gain, 0, driven, 1)
    P.connect(mx, 0, driven, 0)
    lv = obj('prepend level', [700, 390, 90, 20], 1, 1)
    P.connect(driven, 0, lv, 0)
    P.connect(lv, 0, led, 0)
    P.connect(lv, 0, disp, 0)
    lb = obj('loadbang', [440, 20, 60, 20], 1, 1, ['bang'])
    P.connect(lb, 0, drive, 0)

    return P.patcher(WIDTH, description='Mackity by Airwindows: console-style saturation.',
                     banks={'0': {'index': 0, 'name': 'Mackity',
                                  'parameters': ['Drive', 'Output', 'Makeup', '-', '-', '-', '-', '-']}})
