A graph handle is a draggable point on a curve that edits two parameters at once.

## Spec
- `handle` 13 px outer diameter, 1.5 px ring in `orange`, filled with `display` (Auto Filter). Grab radius `handle-grab` 9 px.
- Only the handle is grabbable; clicks elsewhere in the display do nothing. It follows the mouse absolutely: x is frequency on the log axis, y is level.
- The axis spans the parameter's range. A 25–200 Hz parameter on a 20 Hz–20 kHz axis gets about 60 px of travel; the axis must shrink to fit (here 20–400 Hz).
- Both values show in a strip next to the graph as readouts you drag or type into (Delay's filter: Freq, Width). Those parameters get no separate dials.

## In Max
The `v8ui` writes to the two parameters, so automation records. Shift drags fine. The readouts are `live.numbox` controls kept in sync through the parameter.

## When to use

- **Use** for a point on the picture that edits two parameters (frequency and gain/width).
- **Don't** when a single value: display value or dial.
- **Live 12 uses it** 6 times: Erosion, Delay, Echo, Auto Shift, EQ Eight.
- **Max:** `v8ui`, radius 13 px outer, 1.5 px ring; grab 9 px; writes two parameters (x, y). Status: verified.
