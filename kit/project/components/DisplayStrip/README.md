A display strip is one 13 px row along the bottom of a display, under its graph. It holds the display's few small controls and readings.

## Spec (Saturator, 100 %)
- The graph ends 4 px above the strip: graph bottom 92, strip row y 96–109, display bottom 113.
- Buttons are 13 px tall at the strip top (y 96). Text caps sit 2.5 below it (98.5).
- No line between the graph and the strip.
- Order, left to right: an indicator light with its name, then choosers and buttons, then readings.
- Buttons are the text plus about 8 px a side (Saturator's Color: 41 × 13).
- Buttons take the display look: 1 px `orange` outline and `orange` text when off, `orange` fill with `on-accent` text when on (Saturator's Color).
- Mapped to a Macro or MIDI, a button turns grey and stops taking clicks: outline and text `text-dim` when off, `text-dim` fill with `on-accent` text when on. Measured in Live 12.4, light theme, on Saturator's Color and Glue Compressor's Soft: #a5a5a5, Live's `text-dim`. Dark theme not measured yet. Live draws its own green mapping dot at the top-left corner; a design doesn't draw it.
- Draw every state a button can be in: off, on, mapped, mapped and on.
- Readings: label in `text-dim`, value after it (Saturator's Amt Lo 0.0 %).

## Example: Mackity (131 px)
- Display at (4, 4), 123 × 109. Graph at (8, 8), 98 × 84, with the meter beside it at (112, 8).
- Clip light at (14.5, 102.5), "Clip" at x 22. Gain Comp button 69 × 13 at (54, 96), its right edge 4 px in from the display. Checked against Live with m4l-loop, mapped states included.

## In Max
Buttons: `live.text` toggle with the LCD look (see **Mode buttons**). Choosers: `live.menu` LCD. Values: `live.numbox` 4. The light: see **Clip light**.

## When to use

- **Use** when a display needs one to three small controls or readings that belong to the picture but aren't the picture: a clip light, a colour or gain-compensation switch, a mode chooser.
- **Don't** for the device's main controls (they go on the band), or for more than fits one row.
- **Live 12 uses it** in Saturator; Erosion's bottom row is the same idea with readouts only.
- **Max:** `live.text` LCD, `live.menu` LCD, `live.numbox` 4. Status: docs.
