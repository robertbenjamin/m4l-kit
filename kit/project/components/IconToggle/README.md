An icon toggle is an on/off switch shown as a glyph: audition (headphones), spectrum, sidechain, link, freeze, and shape choices that have a standard icon.

## Spec (100 %)
- 13 px tall like every button; the glyph is single-ink and takes the theme colour.
- Off: `button-off` fill, `button-border` border, glyph in `text`. On: `orange` fill, glyph in `on-toggle`.
- Use Live's own icons from `assets/Icons` where they exist; never draw a lookalike of a Live icon.
- Use words instead when the word is short and clearer (Mono, Auto).

## When to use

- **Use** for audition, spectrum, sidechain, link and freeze switches; Ø next to a dial.
- **Don't** when when a word is clearer than an icon.
- **Live 12 uses it** 23 times: Roar, Delay, Auto Shift, EQ Eight, Auto Filter.
- **Max:** `live.text`, mode 1 Toggle; usepicture 1; pictures SVG; usesvgviewbox 1; remapsvgcolors 1. Status: docs.
