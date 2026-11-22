The device grid: every Live 12 device body is 169 px tall and is laid out on a 4 px margin and a 56 px vertical module.

## Rules
- Body is `body-h` (169 px) under Live's 17 px `title-h` bar. Live adds `max-pad` (2 px) around a Max device, so an `openrect` W wide shows a body W + 4 wide.
- Displays start at x = `margin`, y = `margin` (4, 4). A standard display is `display-h` (109 px) tall and ends 7 px above the band labels.
- Control rows sit on the 56 px `module`: label caps at `row-top` (8), `row-mid` (64), `band-label` (120).
- The bottom band: label cap `band-label` 120, ring top `band-ring` 130, value cap `band-value` 156. 33 of 108 measured dials sit here.
- Dials in one group are `dial-pitch` (52 px) apart. The last control (Dry/Wet) is centred `mix-inset` (26–34 px) from the right edge.
- Positions are whole pixels; dial centres land on half pixels because the ring is centred in a whole-pixel box.

## Do / don't
| Do | Don't |
|---|---|
| Put every row on 8 / 64 / 120 | Centre a row by eye (rows at 40 or 96 look wrong) |
| Keep 4 px on each side of a divider | Leave uneven 1–2 px gaps; they show in Live |
