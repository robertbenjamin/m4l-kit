A readout is a parameter shown as text inside a display: a dim label with an orange value you drag or type into.

## Spec
- Stacked: label in `text-dim`, value `orange` 14 px below the label cap and 1 px to the right. Phaser-Flanger's columns are 51 px apart, labels at cap 83.5, values at 97.5.
- Inline strip: label in `text-dim`, value `orange` 6 px after it, on one line (Delay, Echo, Erosion). Erosion (12.4) uses `teal` values in its strip.
- A display's bottom-row value cap sits at y 98.5 (Saturator).

## In Max
`live.numbox` appearance 4 (LCD) with `lcdbgcolor` transparent, so the value reads as plain orange text. Bottom-row numbox at y 95. Labels: `live.comment` in `themecolor.live_lcd_control_fg_zombie`, Ableton Sans Small 10.

## When to use

- **Use** for a value that shapes the picture, placed inside the display next to it.
- **Don't** when mix and output.
- **Live 12 uses it** 48 times: Hybrid Reverb, Phaser-Flanger, Delay, Echo, Shifter.
- **Max:** `live.numbox`, appearance 4 LCD; lcdbgcolor transparent; unit style Custom (e.g. "%.0f %", "%.1f Hz"). Status: verified.
