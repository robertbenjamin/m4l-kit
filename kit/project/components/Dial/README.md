The standard dial is Live's 26 px rotary control; in Max it is a `live.dial` at appearance 0, which Live draws itself.

## Spec (fitted against Live 12 at 100 %: Saturator, Channel EQ, Auto Pan-Tremolo)
- Ring `dial` (26.125 px outer diameter), stroke `dial-stroke` 2.1 px. Travel **±150°**: Dry/Wet at 62 % points to 35.97°, a maximum value to 149.9°.
- Unlit ring `ring` (Live's Poti); lit arc `teal` from the minimum, or from the centre for ± controls, up to the pointer. The lit side has no gap.
- Gap on the unlit side: the ring is cut by a **pointer-shaped clearance**, 1.125 px each side of the pointer with round ends. The cut runs parallel to the pointer, which gives the ring end its slight curved indent. It is not a radial cut.
- Pointer `pointer` (PotiNeedle), 2.2 px wide, **round at both ends**, from 0.25 px off centre to 1.25 px inside the ring's outer edge.
- Vertical placement, plain dial: label cap at C, ring top at C + 9.5, ring centre 0.44 px below the ring's geometric centre. Value cap at ring top + 26.5.
- Notched (±) dial: ring top at C + 9.5 + 5.4; notch 9 × 4.5 triangle, top 5.375 above the ring top, `ring` at centre and the arc colour off centre.
- Text: the label centres **0.5 px right** of the ring centre (1 px on notched dials); the value centres on the ring (notched: 0.25 px right, 0.5 px lower). Centred text starts on a whole pixel of the device's own grid.

## In Max
- `live.dial`, appearance 0 (Vertical). Ring centre = rect x + 23; label cap = rect y + 1.5, so band dials (cap 120) sit at rect y 118.5 (measured in Live 12.4 with m4l-loop).
- Notched dials: `triangle 1`, placed 4 px higher (`notch-lift`). Clicking the triangle restores the initial value.
- Leave colours on their dynamic defaults so the dial follows every Live theme.
- Number formats: unit style Custom, `%.0f %` → "50 %", `%.1f Hz`, `%.0f Hz`. Max's percent style writes "50.0 %", which Live never does.

## Do / don't
| Do | Don't |
|---|---|
| Keep notched and plain dials' rings on one line | Line up their labels instead |
| Use the `orange` arc only where Live does (a selected or modulated control) | Recolour dials for decoration |

## When to use

- **Dial.** **Use** for a continuous value you play.
- **Don't** when the value is set once (number box) or shapes the picture (display value).
- **Live 12 uses it** 92 times: Spectral Time, Hybrid Reverb, Echo, Phaser-Flanger, Chorus-Ensemble.
- **Max:** `live.dial`, appearance 0 Vertical; showname 1; shownumber 1; needlemode 0 Automatic. Status: verified.
- **Notched dial.** **Use** for a ± value whose centre means "unchanged": gains, EQ bands, pan, width.
- **Don't** when centre is not a resting point (LFO amount, bias): use needlemode 2 without the triangle.
- **Live 12 uses it** 15 times: Channel EQ, Multiband Dynamics, Utility, EQ Eight, Drum Buss.
- **Max:** `live.dial`, appearance 0 Vertical; triangle 1; needlemode 2 Bipolar; placement 4 px higher than a plain dial. Status: verified.
