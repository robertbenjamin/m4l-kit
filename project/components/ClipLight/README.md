An indicator light is a 5 px dot that shows a state the device reports, such as clipping. You read it; you never click it.

## Spec (Saturator, 100 %)
- 5 px dot (r 2.5). Off: `led-off`, all but invisible on the display. On: `led-on`, the theme teal at about 65 %.
- It fades, it doesn't switch: brightness follows how hard the device works (Mackity: 0 dB past its clamp is dark, 6 dB past is full), rises at once and falls with a 0.3 s time constant. Measured on Saturator in Live 12.4 from screen video.
- In a display strip: centre 10.5 px right of the display's left edge, on the strip row's centre (Saturator: 14.5, 102.5 with the display at x 4).
- Its name follows at 18 px from the display's edge (x 22 in Saturator), cap 2.5 below the strip top, in `text-dim`.
- The light comes first in the strip, before any button or reading (Saturator: light, No Clip, Color, Amt Lo).

## Measured (Live 12.4, dark, Saturator Soft Clip)
- Lit at full: #117f8b. Unlit: #141414 on the #181818 display. Fade time constant 0.30 s (Mackity's v8ui: 0.39 s gives the same on screen).
- The name stays `text-dim`; only the dot lights.
- Light themes are not measured yet.

## In Max
No `live.*` object draws a round light. Draw it in a `v8ui` with colours from `max.getcolor`: off `live_lcd_bg` x 0.83, on `live_value_arc` x 0.65, blended by the glow, and the name as a `live.comment`. The audio object reports the state (Mackity: an extra outlet on `aw.mackity~`).

## When to use

- **Use** for a state the device reports: clipping, overload.
- **Don't** for anything you click (toggle, checkbox), or for a level (meter).
- **Live 12 uses it** once: Saturator.
- **Max:** `v8ui` + `live.comment`. Status: custom.
