A graph draws what the device does to the sound, on a quiet grid.

## Spec
- Boxed graph (Saturator): 1 px border and centre crosshair in `grid`; curve `curve` 1.5 px in `teal`.
- Frequency axis: log 20 Hz–20 kHz with 100 / 1k / 10k lines (Channel EQ), running from the display top to just above the axis labels.
- Grid lines are translucent (Live's SpectrumGridLines): decade lines and the 0 dB line in `grid-decade`, ±12 dB lines in `grid-level` (half opacity). Level lines start right of the dB labels and break around the frequency labels.
- A spectrum (`spectrum`, translucent in light themes) is drawn over the grid lines and under the curve.
- Saturator's drive band (`teal-shade`) fills the graph inside its border (y 26–91) and is drawn over the crosshair, which shows through it as #3c6d71.
- Axis labels in `text-axis`, right of their line and flipped to the left near the edge (10k was clipped otherwise); a label cuts a gap in the line behind it.
- Curves stay inside the border. A curve that runs to the graph's edge has round caps that poke over the border, so the kit clips curves to the area inside it. In Max, keep them inside the same way (see In Max).
- Draw order: grid and labels first, then fills and curves, then handles. Curves never sit under grid lines.
- Solid lines only. No dashed or dotted lines.
- Full-height (3a) displays are full bleed: no border box.
- Show drive on a curve with Saturator's driven-range band (the range the signal covers).

## Reference detail (Saturator, measured in Live 12.4 dark)
Measurements for a graph that already shows a driven band or a drive-dependent curve. They describe how Saturator behaves; they don't call for either element.

- **Band edge:** the recent input peak times the drive gain, on the same x axis as the curve.
- **Band ballistics:** rises at once on a peak, falls exponentially with a 0.30 s time constant, and is gone in silence.
- **Band colour:** the theme teal at about 27 % over the display, drawn after the crosshair so the crosshair shows through it. This was measured against a Max band of known opacity in the same screen recording. Screen-recording colours are shifted, so compare inside one recording.
- **Zoom with drive:** above 0 dB of drive, the x axis zooms out by the square root of the drive gain, so half of each dB bends the curve inward and half widens the band. At 0 dB and below it doesn't zoom (the curve's corner sat at 0.66 of the half-width at both −6 and 0 dB).
  - From +6 to +18 dB, the corner moved from 0.37 to 0.23 of the half-width, and the widest band grew from 0.46 to 0.89. Without the zoom the band would grow 4×, and it pins to the edges with mastered material.

## In Max
`v8ui` with `live_spectrum_grid_lines` for the grid and `live_value_arc` for curves. `live_display_line_one` is orange in the default theme; it is not the curve colour.

Details that only matter if you build one:
- `v8ui` has no `mgraphics.clip()`: clamp the curve's points inside the border instead.
- `v8ui` doesn't route messages to plain top-level functions ("no function …"): dispatch in `anything()`.
- Max rounds a `v8ui`'s size up (9 → 10 px): draw from the design's numbers, not `mgraphics.size`.
- Explicit RGB is colour-managed to the screen, while `max.getcolor` theme colours land on the kit's measured values. Prefer theme colours, with an alpha or a scale, over hard-coded hex.
- For a live band, a `peakamp~ 33` per channel → `maximum 0.` → `* 0.` drive gain → `v8ui` is enough; animate the fall inside the `v8ui`. Max's `*` and `maximum` do integer maths without a float argument.
