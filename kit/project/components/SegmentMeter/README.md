A segment meter is a row of small LED cells inside a display, like Auto Pan-Tremolo's pan position strip.

## Spec (Auto Pan-Tremolo, 100 %)
- Cells 3 × 7 px on a 4 px pitch, no radius.
- Two banks of 26 cells, 6 px apart, between an `L` in `teal` and an `R` in `orange`. The left bank is `teal`, the right bank `orange`.
- An unlit cell is its accent at 21.5 % opacity. Lit cells brighten toward full accent near the centre, following the signal.
- Lives inside a display only, like every meter.

## In Max
Draw it in the display's `v8ui` with `live_value_arc` and `live_display_handle_one`, or use `live.meter~` where a level meter fits.
