The number box is Live's compact value field: a 45 × 13 box whose teal fill shows the value, from the left or from the centre.

## Spec (Auto Pan-Tremolo, 100 %)
- `box-w` × `box-h` (45 × 13), 1 px `button-border` (ControlContrastFrame), ground `field` (ControlTextBack), fill `teal-deep` (RangeEditField) inside the border, 11 px tall.
- Unipolar: fill from the left inner edge. Bipolar: fill from the centre, starting at the inner left edge + floor(inner width / 2). Fill edges land on whole pixels.
- Text: `label` style in `text`, centred, cap 3 px below the box top. It sits on top of the fill and does not change colour.
- A label above a pair of boxes reads like "Att | Mod" (Auto Pan-Tremolo).

## In Max
`live.numbox` appearance 2 (Slider) for unipolar, 3 (Bipolar) for ± values. For a value inside a display use appearance 4 (LCD) with a transparent `lcdbgcolor` instead (see Readout).

## When to use

- **Number box.** **Use** for a continuous value you set, or one that refines a dial (Fine, Trim, Window); columns that would overflow with dials.
- **Don't** when the device's main controls.
- **Live 12 uses it** 35 times: Spectral Resonator, Auto Shift, Roar, Shifter, Multiband Dynamics.
- **Max:** `live.numbox`, appearance 2 Slider; size 45 × 13. Status: verified.
- **Bipolar number box.** **Use** for a ± value you set (offsets, modulation depth, shift).
- **Don't** when a ± value you play: notched dial.
- **Live 12 uses it** 10 times: Delay, Echo, Spectral Resonator, Auto Pan-Tremolo, Auto Shift.
- **Max:** `live.numbox`, appearance 3 Bipolar; size 45 × 13. Status: docs.
- **Choice in a number box.** **Use** for an ordered choice that reads like an amount (Hybrid Reverb Vintage: Off → Oldest).
- **Don't** when unordered choices: menu.
- **Live 12 uses it** 1 times: Hybrid Reverb.
- **Max:** `live.numbox`, appearance 2 Slider; parameter enum. Status: docs.
