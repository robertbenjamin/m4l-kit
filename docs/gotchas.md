# Gotchas

Facts that decide whether a device renders, loads or measures correctly. Verified with Live 12.4 and Max 9.1 on macOS.

## Live
- **Remote scripts:**
  - Must be real folders. Live skips symlinked ones, so `setup` copies them.
  - Live loads the scripts in the **User Library you've set it to use** (`Library.cfg`), which may not be `~/Music/Ableton/User Library`.
  - Live loads a script's modules once per launch. M4LLoop re-imports `handler.py` on every message; `__init__.py` changes need a restart.
- **Swapping devices:** load the real `.amxd`. A `bpatcher` that reloads its contents doesn't redraw `v8ui` objects inside Live.
- **A new file or folder in the User Library** takes Live's browser a few seconds to index. `build` retries for up to 20 s.
- **`browser.load_item`:** adds the device at the end of the chain, at default values. `reload` moves it back and copies the settings by parameter name.
- **New tracks** get the devices from your Default Track template.
- **A track monitoring "In"** plays its input, not its clips. Use Auto to hear clips.
- **The LOM value of a Max parameter** is linear in dial position, even when the parameter has an exponent. Set positions, not display values.
- **Native device names** in the chain carry their preset name, for example "Default Saturator".
- **Max's console:** every line appears in `~/Library/Preferences/Ableton/Live <version>/Log.txt` as "Message from Max".

## Max objects
- `*` and `maximum` without a float argument do integer maths: write `* 0.` and `maximum 0.`.
- `expr` has no `?:` operator. Write `($i2 != 0) * a + ($i2 == 0) * b`.
- `live.text`:
  - Draws its border 1 px inside its rect: make the rect 1 px larger on every side than the visible box.
  - `mode 1` is a toggle; `mode 0` is a momentary button.
- `live.meter~`:
  - It is mono: a stereo meter is two of them.
  - It paints over anything beneath or above it, including `v8ui` and `panel` objects.
  - It draws its own overload zone.
- A display `panel` needs `background 1`. Otherwise it covers the objects drawn inside the display.
- **`live.dial`:**
  - The ring centre sits at rect x + 23, and the label cap at rect y + 1.5 (100 % zoom).
  - With an exponent and an initial value of exactly 0, it can show "-0.0 dB".
- Theme colours: use `saved_attribute_attributes` expressions such as `themecolor.live_lcd_bg`, so every Live theme works.

## v8ui
- There's no `mgraphics.clip()`: clamp coordinates instead.
- Messages reach only `anything()` and the built-in handlers, not plain top-level functions. Dispatch on `messagename`.
- Max rounds the box size up (a 9 px box becomes 10). Draw from your design's numbers, not `mgraphics.size`.
- `autowatch` doesn't follow a symlinked script. m4l-loop copies scripts and rebuilds on change.
- Max only indexes a file it hasn't seen before when it launches. Restart Live once after adding a new script or external.
- Call `mgraphics.redraw()` at load, so a reloaded script paints straight away.

## Capture and colour
- `screencapture -l<window id>` captures Live even when other windows cover it. `-v -V <seconds> -R x,y,w,h` records video, and refuses to overwrite an existing file.
- **Max colour-manages explicit RGB** to the display (P3 on recent Macs), so a hex you set isn't the hex you see. `max.getcolor()` theme colours come out as Live's on-screen colours: prefer them, with an alpha or a scale.
- Live's grid colour (`live_spectrum_grid_lines`) is translucent, so it tints whatever is under it.
- Headless Chrome renders text at the same weight as Live but with softer edges. Expect a residual of 5–9 on text.
- Video encoding shifts colours. Measure colours in stills, or relative to a known colour in the same video.
