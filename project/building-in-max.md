# Building in Max

How the components map to Max objects, and what the Live tests taught. Presentation rects use body coordinates directly: Live adds a Max device's 2 px side margin outside the patch, so subtract nothing (measured in Live 12.4 with m4l-loop).

## From Ableton's Max for Live production guidelines
| Rule | Effect |
|---|---|
| Use Ableton Sans (bundled with Max) for all device text | `Ableton Sans Small` 10, the face Live's device text measures as |
| Presentation rects in whole pixels | Half-pixel rects blur on non-retina screens |
| Leave `live.*` colours on their dynamic defaults | Devices follow every Live theme, light themes too |
| `live.tab` in Live mode; `live.text` outputs on mouse up | Mouse down only for performance controls |
| Keep devices narrow; set the initial width exactly | |

## Object facts
| Object | Facts |
|---|---|
| `live.dial` | Appearance 0 (Vertical) ≈ native size. Ring centre = rect x + 23; label cap = rect y + 1.5, so band dials (cap 120) sit at rect y 118.5 (measured in Live 12.4 with m4l-loop). On non-retina screens that half pixel blurs: use 118 or 119 if a device must look sharp there. `triangle 1` for ± controls, placed 4 px higher. Appearance 3 (Large) is 50 × 63, bigger than native |
| `live.numbox` | Appearance 2 = filled box; appearance 4 = LCD readout, with `lcdbgcolor` transparent for plain orange text. Display bottom-row numbox at y 95 |
| `live.line` | Draws at the left edge of its rect |
| `live.text` | Draws its border 1 px inside its rect: the rect is 1 px larger on every side than the visible box. Fold toggle: every bg and border colour transparent, glyph in `live_lcd_control_fg_zombie` |
| `panel` | Display ground: bgfillcolor `themecolor.live_lcd_bg`, and `background 1`. Without it the panel covers the controls in front of it inside the display |
| `live.comment` | A label in a display: rect = (text x − 4, cap − 5), Ableton Sans Small 10 |
| `v8ui` | Only over the graph area, never over a control. Colours via `max.getcolor`. Max rounds the box size up (9 → 10 px), so draw from the design's sizes; `mgraphics.size` can be larger |
| `live.meter~` | All meters. It is mono: a stereo meter is two, 4 px wide and 1 px apart, framed by a `v8ui`. It paints over anything near it, so nothing can draw on top of it (no clip tick) |
| `live.thisdevice` | Fold-out: patcher `devicewidth` 0, then `setwidth` |

## Theme colour ids
`live_lcd_bg` (display), `live_spectrum_grid_lines` (grid), `live_value_arc` (curves, the dial teal), `live_display_handle_one` (handles), `live_display_scale_text` (axis labels), `live_lcd_control_fg`, `live_lcd_control_fg_zombie` (dim labels), `live_control_text_zombie`. `live_display_line_one` is orange in the default theme; don't use it for curves.

## Number formats
Unit style Custom: `%.0f %` ("50 %"), `%.1f %` where Live shows a decimal, `%.0f Hz`, `%.1f Hz`. Max's percent style writes "50.0 %".

## Rules the Live tests added
- Whole-pixel symmetry: every ring 13 px in from its display's edge (`ring-inset`); 4 px each side of a divider. Gaps of 1–2 px are visible.
- A handle's axis spans its parameter's range.
- Keep the approved look when fixing behaviour: a control that "drags weirdly" is more likely covered by a `v8ui` than wrongly styled.
- Live reloads an `.amxd` when the file changes, but not while one of its controls has keyboard focus.
- Live's title-bar fold arrow is not available to Max devices in Live 12.
