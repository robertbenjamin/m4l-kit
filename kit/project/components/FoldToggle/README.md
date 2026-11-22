The fold control opens or closes part of a device. Live's title-bar arrow isn't available to Max devices, but Live uses two other expand controls inside device bodies, and both can be built in Max.

## Native precedents (100 %)
- **Disclosure triangle in a display.** Delay's "▶ LFO" (6 × 7 triangle, then the section name) opens the LFO row; Echo's "▲" (7 × 6.5, then the section's checkbox) folds its filter section. The triangle is `text-dim` and points to where the content will go.
- **Round button on the body.** Auto Filter, Roar and Auto Shift open their sidechain and MIDI panels with a 13 px circle: `button-off` fill, 1 px `button-border` ring, a dark triangle inside (▼ closed, ▶ open sideways). Saturator's title-bar arrow is the same drawing.

## When to use
- Disclosure triangle: to reveal an extra row or section inside a display.
- Round button: to widen the device with a side panel or a second set of controls, at the top-left of the body.
- Use a fold-out only for controls you set once, when the device would otherwise pass about 20 controls or its type's width range.

## In Max
- Disclosure triangle: `live.text` with every background and border colour transparent and the triangle as text or an SVG picture in `live_lcd_control_fg_zombie`.
- Round button: `live.text` (toggle) with transparent background and an SVG picture of the circle and triangle, `remapsvgcolors 1`.
- Resizing: set the patcher's `devicewidth` to 0, then send `setwidth` to `live.thisdevice`. Keep the state in a hidden parameter and re-apply it on the init bang.
