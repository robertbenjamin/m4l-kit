The large dial is the 37 px version of the dial, kept for the one control that defines the device.

## Spec
- Ring `dial-large` (37 px), the same `dial-stroke` and `pointer-w` as the standard dial; only the ring grows. Travel ±148°.
- Label cap `label-gap-large` (11.5 px) above the ring top; value cap 39 px below it. The pointer starts 4.2 px from the centre.
- 7 large dials in 6 devices (Auto Filter, Roar, Redux, Shifter, Erosion and others). Never scale a small dial up; these are measured values.

## Rules
- **A band with a large dial sits higher** (Erosion): the display ends at 95 instead of 113, plain dials' labels move to cap 111 and the large dial's label to 103.5, so all rings share one centre (about y 134) and the large dial's value (cap about 154) still fits above the body's bottom edge. On the standard band its value would run off the device.
- Erosion spaces the three dials 61 px apart.
- At most one large dial per section, and only for the control the device is loaded for.
- Mixed sizes in one band share a ring centre line; their labels do not share a row (Erosion).
- In tiled devices (type 4) one large dial leads each tile.

## In Max
`live.dial` appearance 3 (Large) is ELPHNT's 50 × 63 size, bigger than native. Check the size in Live before you use it.

## When to use

- **Use** for the control the device exists for; at most one per section, leading it.
- **Don't** when two in one section, or a device with one band and ≤ 5 controls.
- **Live 12 uses it** 11 times: Roar, Redux, Glue Compressor, Erosion, Shifter.
- **Max:** `live.dial`, appearance 3 Large (50 × 63 box, bigger than Live's 37 px ring) or a larger appearance-0 box; showname 1; shownumber 1. Status: docs.
