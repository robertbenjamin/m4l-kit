Mode buttons choose a mode inside a display.

## Spec
- `box-h` 13 px with a 3 px gap, together spanning the display width minus 4 px each side. Phaser-Flanger: three 65 × 13 buttons at x = 8, 76, 144, y = 63, with readouts under them. Auto Pan-Tremolo: two 116 × 13 buttons at the top of the display.
- Selected: `orange` fill, no border, text `on-accent` (the colour of the surface behind).
- Unselected in a display: 1 px `orange` outline, `orange` text.
- On the body: `box` fill, 1 px `ring` border, `text`.

## In Max
`live.tab` in Live mode; `live.text` with output on mouse up.

## When to use

- **Use** for two or three modes that change the whole picture, at the top of the display.
- **Don't** when settings that leave the picture alone.
- **Live 12 uses it** 7 times: Auto Pan-Tremolo, Phaser-Flanger, Chorus-Ensemble, Echo, Auto Shift.
- **Max:** `live.tab`, appearance 1 LCD; livemode 1. Status: docs.
