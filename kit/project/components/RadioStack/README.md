A radio stack is a column of buttons for one choice of three or four device modes.

## Spec (Compressor, 100 %)
- Buttons 43 × 13 with a 3 px gap, stacked; each is a separate box with a 1 px border.
- Selected: `orange` fill, text `on-toggle`. Others: `button-off` fill, `button-border` border, `text`.
- Labels are the mode names in title case (Peak, RMS, Expand; Standard, Soft Clip, True Peak).
- A label above the stack names the choice when it isn't obvious (Mode, Smoothing, Routing).

## When to use

- **Use** for three to four device modes in a column (Peak / RMS / Expand).
- **Don't** when five or more: menu.
- **Live 12 uses it** 12 times: Delay, Spectral Time, Limiter, Echo, Auto Shift.
- **Max:** `live.tab`, appearance 0 Default; livemode 1; stacking one option per row (num_lines_presentation = N). Status: docs.
