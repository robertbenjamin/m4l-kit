Level and gain-reduction meters, always inside a dark display.

## Spec
- Box `meter-w` 11 px, 1 px `grid` border. Stereo: two 4 px bars with a 1 px gap; mono: one 9 px bar.
- `meter-clip` 16 px overload zone at the top, closed by a 1 px tick over each bar.
- Level: `meter-green`, to `meter-yellow` near the top, `meter-red` over 0 dBFS. RMS bright, peak region dimmed, 1 px `meter-hold` peak tick. Background `display`.
- Gain reduction: `meter-gr`, drawn from the top.
- Scale is linear in dB (Compressor: 36 dB level range, 57 dB GR range).
- Marker: grey `text-dim` triangle just right of the box, pointing at a threshold or ceiling; draggable where it is a parameter. Compressor dims the level above its threshold.
- Text: dim label above (cap 11 px above the box), value below (cap 4 px below). A parameter value in a meter display is `teal` (Limiter's Ceiling); a reading stays `text-dim`.
- A meter display runs from label cap 10 to value cap 156.
- Dynamics lines: threshold `line-threshold` (teal), gain reduction `line-gr` (orange). Never swap them.

## Rules
- Never put a meter on the grey body.
- Fill a single-control gain section with a meter rather than empty space.
- Don't use Dynamic Tube or Gate as references; they are old designs.

## In Max
`live.meter~`; Live draws it. Measured in Live 12.4:
- It is mono: a stereo meter is two `live.meter~`, 4 px wide, 1 px apart, inside a 1 px frame drawn by a `v8ui`.
- It draws its own overload zone and paints over anything beneath or above it, so the 1 px `meter-clip` tick can't be added. Draw the whole meter in a `v8ui` where the tick matters.
