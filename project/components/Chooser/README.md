Choosers pick one of a list inside a display.

## Spec
- Dropdown: 13 px box in `teal` (Saturator) or `orange` (Auto Pan-Tremolo), text `on-accent` 2 px in, a 7 × 4.75 triangle 9 px from the right edge and 4 px from the top. A dropdown may hold an icon instead of text (Auto Pan-Tremolo's LFO shape).
- Inline chooser: `teal` or `orange` text with a 5 × 2.5 triangle (45° sides) whose top is 3.5 px below the text cap. Its x is set by the control, not by the text width: Saturator's No Clip at 70.5, Auto Pan-Tremolo's Rate at 111.

## In Max
`live.menu`. Leave colours dynamic.

## When to use

- **Chooser.** **Use** for a choice inside the display that the picture depends on (Scale, Algorithm, Routing, Lookahead).
- **Don't** when choices unrelated to the picture.
- **Live 12 uses it** 13 times: Roar, Auto Shift, Hybrid Reverb, Saturator, Auto Pan-Tremolo.
- **Max:** `live.menu`, appearance 1 LCD; triangle 5 × 2.5 after the text. Status: docs.
- **Menu.** **Use** for four or more choices on the body.
- **Don't** when a choice that belongs to the picture: chooser.
- **Live 12 uses it** 18 times: Auto Filter, Echo, EQ Eight, Hybrid Reverb, Saturator.
- **Max:** `live.menu`, appearance 0 Default; pictures optional (EQ Eight filter shapes). Status: docs.
