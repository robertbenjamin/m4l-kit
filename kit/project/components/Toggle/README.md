A text toggle is a 13 px on/off switch named by what it turns on (Auto, Ping Pong, Mono, Ø). Beside a dial it modifies that dial. For a section on/off use **Checkbox**; for view and audition switches use **IconToggle**.

## Spec
- `box-h` 13 px tall, 1 px `button-border`. On: `orange` fill, text `on-toggle`. Off: `button-off` fill, text `text`.
- Place a toggle under the dial it modifies (Compressor's Auto under Release, Utility's Mono under Width). A toggle for something the display shows goes in the **Display strip** as a display button.
- A 1 px `divider` connector ties a toggle to its dial only where Phaser-Flanger uses one: Hz and Ø right beside their dials in a full band. In review, a connector to a lone toggle beside the last dial looked foreign.
- Name it for what it does to the sound. **Makeup** is Live's name for a compressor's make-up gain (Compressor, Glue Compressor). When the output simply follows a drive or gain control back down, **Gain Comp** reads clearer: Makeup there sounds like compression (Mackity).
- Draw the mapped state too: mapped to a Macro or MIDI, a toggle turns grey (see **Display strip**).
- Width: the text plus about 8 px a side (Saturator's Color: 41 × 13). A 45 px box cramps a six-letter word.

## In Max
`live.text` in toggle mode, output on mouse up (mouse down only for performance controls). Leave colours dynamic. `live.text` draws its border 1 px inside its rect, so give the rect 1 px more on every side than the visible box.

## When to use

- **Use** for on/off on the body, named by what it switches on (Auto, Ping Pong, Mono).
- **Don't** when view or audition switches (icon toggle); enabling a section (checkbox).
- **Live 12 uses it** 48 times: Utility, Multiband Dynamics, Shifter, Echo, Delay.
- **Max:** `live.text`, mode 1 Toggle; appearance 0 Default; outputmode 1 Mouse up. Status: docs.
