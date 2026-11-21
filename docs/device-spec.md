# Device spec

A device spec is a Python file. `m4l-loop` imports it and reads these names:

| Name | Required | Meaning |
|---|---|---|
| `NAME` | yes | Device name: the `.amxd` file name and the name Live shows |
| `WIDTH` | yes | Device width in px at 100 % (Max `devicewidth`) |
| `HEIGHT` | no | Body height, default 169 (every Live device) |
| `REFERENCE` | yes | Design page, relative to the spec |
| `ELEMENTS` | no | `{name: (x, y, w, h)}` boxes to measure one by one, in body px |
| `JS` | no | `v8ui`/`jsui` scripts the device loads, copied into the `m4l-loop` Max package |
| `EXTERNALS` | no | `.mxo` externals the device uses, copied into the same package |
| `build()` | yes | Returns the patcher dict. Use `m4l_loop.patch.Patch` and `Patch.patcher()` |

Coordinates: Max presentation coordinates equal the design's body coordinates: (0, 0) is the top-left corner of the body, under Live's title bar.

```python
from m4l_loop.patch import Patch

NAME, WIDTH, REFERENCE = 'MyFx', 131, 'design.ref.html'
ELEMENTS = {'drive ring': (21, 127, 37, 30)}

def build():
    P = Patch()
    dial = P.box(maxclass='live.dial', varname='Drive', parameter_enable=1, numoutlets=2,
                 outlettype=['', 'float'], patching_rect=[30, 100, 48, 48],
                 presentation=1, presentation_rect=[16.5, 118.5, 48, 48],
                 saved_attribute_attributes={'valueof': {'parameter_longname': 'Drive'}})
    P.params[dial] = ['Drive', 'Drive', 0]
    return P.patcher(WIDTH)
```
See `examples/mackity/device.py` for a full device: audio, dials, a toggle, meters and `v8ui` displays.

## The reference page
`REFERENCE` is an HTML page that m4l-loop opens in headless Chrome as `page.html?ref=1&zoom=Z&theme=T`. With `ref=1` the page must:
- draw only the device **body**, with no title bar and no frame, at `zoom` screen px per body px
- use the theme named by `theme` (`dark`, `light` or `light-cool`)
- show the device's **default state in silence**: default parameter values, empty meters, nothing that only appears with audio
- paint everything else in `#ff00ff`, which m4l-loop crops away

`examples/mackity/make_ref.py` shows one way to add this mode to an existing design page.

## The report
`m4l-loop-out/<NAME>/report.json`:

| Field | Meaning |
|---|---|
| `match_pct` | Share of pixels within tolerance of the design |
| `elements` | Per `ELEMENTS` box: `live_is_off_by` [dx, dy] in body px (move it by the negative) and `residual`, the mean difference once moved |
| `regions` | Mismatched areas found automatically, each with the same two fields |
| `zoom` | Live's interface zoom, found by matching |
| `where` | The device's content origin in the window capture, in px |

How to read `residual`:
- **0–2:** identical.
- **5–9 on text:** normal. Live and Chrome rasterise glyph edges differently, at the same weight.
- **Above 10:** the element looks different, not just misplaced.
