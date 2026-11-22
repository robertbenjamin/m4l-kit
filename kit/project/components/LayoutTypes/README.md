Six layout types cover all 22 current Live 12 audio effects; where the display goes decides the type.

| Type | Devices | Width | Structure |
|---|---|---|---|
| 1 Display over band | Saturator, Channel EQ, Auto Pan-Tremolo, Erosion | 207–251 | Full-width display on top, one control band under it. Single-purpose processors |
| 2 Display + mix column | Phaser-Flanger, Chorus-Ensemble | 245–273 | Display top-left, band under it; globals stacked in a right column on the 56 px module, behind a divider |
| 3a Full-height centre display | Limiter, Delay, Echo, Auto Shift, Multiband Dynamics, EQ Eight, Drum Buss | 268–586 | The display is the instrument and runs full height, full bleed; columns either side |
| 3b Centre display over band | Compressor, Shifter, Hybrid Reverb, Spectral Resonator, Spectral Time | 371–627 | Display top-centre, a band under it, side columns |
| 4 Tiled | Auto Filter, Roar | 443–585 | Sections as `body` tiles on the `title` ground, `tile-gutter` 2 px, `radius-display`; one large dial leads each tile |
| 5 Controls only | Redux, Utility | 139–147 | No display; two columns split by a full-height divider |

## Choosing
Pick the type from the control count and from whether there is a picture (see **Design logic**, question 6):
- 6–12 controls and one picture: type 1. Add a mix column (type 2) when there are three globals (Output, a character control, Dry/Wet).
- 8–12 controls and nothing to draw: type 5.
- A picture that needs height, 9–27 controls: type 3a. Display plus side columns, 8–26: type 3b.
- Independent stages that can each be off, 22–30 controls: type 4 tiles.
- Past about 20 controls, add a second level: pages, a fold-out, or one editor for the selected item.
- Use a type only inside its measured width range, and size the device to its content (Redux 147, Utility 139).
- Exception: a device with 1–3 controls sizes to its content below the range. Mackity is type 1 at 131 px: two dials at the 52 px `dial-pitch`, centred 39.5 px from each edge, with the display strip holding its extra controls. This was a design review decision, not a Live measurement; no Live 12 effect is narrower than Utility.

The skeletons above are wireframes of each type's structure, not devices.
