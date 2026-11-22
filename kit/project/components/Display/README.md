The display is the dark LCD area where the device explains itself: graphs, meters, modes and secondary values.

## Spec
- `display` ground, `radius-display` 2 px, at x = `margin`, y = `margin`. Standard height `display-h` 109 px.
- Full-height (type 3a) displays run 4..165 and are full bleed: no boxed graphs inside.

## Rules
- The display explains, the body acts. Mode choices and secondary numbers live in the display, next to what they change.
- Meters always live inside a display, never on the body.
- In a display, labels are dim (`text-axis`, `text-dim`) and editable values are `orange`. On the body, labels and values share `text`.
- Text on a selected button takes the colour of the surface behind it (`on-accent`).

## In Max
- Ground: a `panel` with bgfillcolor `themecolor.live_lcd_bg`.
- Draw pictures in a `v8ui` over the graph area only, never over a `live.*` control (it hides them and eats their clicks).
- Draw at `mgraphics.size`, not `box.rect` (box.rect is the patching size). Give the v8ui the same patching and presentation size.
- Colours from `max.getcolor`: `live_lcd_bg`, `live_spectrum_grid_lines`, `live_value_arc` (curves), `live_display_handle_one`, `live_display_scale_text`, `live_lcd_control_fg`.
