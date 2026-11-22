Build Max for Live devices that look and behave like Ableton's own Live 12 devices. Every value here was measured from Live at **100 % zoom**: the body is 169 px tall and a standard dial ring is 26 px. Coordinates are 1x px in body coordinates, (0, 0) at the top-left of the body under Live's title bar. Previews and reference images are shown at 2x.

## How to use this system
- Pick a layout type first (`LayoutTypes`), then place controls on the grid (`DeviceGrid`): margin `margin`, rows on `module`, the band at `band-label` / `band-ring` / `band-value`.
- Build only from components listed here. Every element needs a reference device before it goes in a design; don't invent headers, dashed lines, ticks or new controls.
- In Max, use Live's own objects (`live.dial`, `live.numbox`, `live.text`, `live.tab`, `live.menu`, `live.comment`, `live.line`, `live.meter~`) for every control. Live draws them, so look, drag, double-click reset, automation and themes are native by construction. See **Building in Max**.
- Decide what goes where with **Design logic** (six questions, from all 370 controls on Live's audio effects), then pick each Max object and its settings from **Max objects**. Tools can read the same table from `max-objects.json`.
- Draw previews and mockups with `window.LiveKit` (see `components/index.d.ts`).
- Every colour token carries a `status` per theme: `measured` (sampled from Live or the manual at 100 %), `theme-file` (raw from Live's theme file, not checked on screen) or `estimated` (a guess). Measure an `estimated` value before you rely on it; `tokens.json` explains each status in `statusLegend`.
- Open any page built with `LiveKit` with `?ref=1&zoom=Z&theme=T` to get a reference image for pixel comparison (m4l-loop uses it): the first device draws alone, body only, at zoom Z on `#ff00ff`. While `LiveKit.ref` is set, a page should draw its default state in silence.
- Check every measurement against a 100 % reference. Screenshots taken at another Live zoom (110 % was the trap) make everything 10 % too big.

## Content fundamentals
- Labels are short nouns in title case as Live writes them: "Drive", "Dry/Wet", "Output", "Freq", "Res". No sentences, no punctuation, no emoji.
- Values follow Live's formats exactly: "50 %" (space before %, no decimal unless Live shows one), "6.0 dB", "+3.0 dB" for ± controls, "0.0 dB" at zero, "1.20 kHz", "120 Hz", "C" for a centred pan, "90°".
- Never repeat a label: no section header that repeats a dial's name, and no control shown twice.
- Order controls by the signal path, left to right or top to bottom. Output, then Dry/Wet, always last.
- A gain that only boosts starts at 0 dB, not below: its range is 0 to the maximum, its default 0 dB. Cutting is Output's job.
- Every control has Info View text, written like Live's own: the control's name as the title, then one or two plain sentences on what it does and what turning it changes ("Adjusts the output level of the device."). The device gets one too: what it is, then what it sounds like. No marketing, no jargon the label doesn't already use.

## Visual foundations
**Type.** One face, one size: Ableton Sans Small 10 px (`label`, `value`) for everything on a device, number boxes included. Hierarchy comes from colour, never size or weight. Centred and right-aligned text starts on a whole pixel of the device's own grid (a device can sit on a half pixel); left-aligned text is not rounded. Glyph spacing is the font's own: Live doesn't round advances or add tracking. The title bar's `title-bar` style is Live's own. Ableton Sans ships with Live and Max but may not be redistributed; previews here fall back to Helvetica Neue or Arial.

**Colour.** Three themes: Default Dark Neutral Medium (`dark`, Live's default), Light Neutral (`light`, most manual images) and Light Cool (`light-cool`, the manual's 12.3+ images such as Auto Pan-Tremolo). Each token maps to a role in Live's theme files (display = RetroDisplayBackground, ring = Poti, number-box fill = RangeEditField, grid lines = SpectrumGridLines), so new themes follow from the `.ask` file. Meter and dynamics-line colours are raw theme-file values.
- `body` ground, `text` for every label and value on it.
- `display` for every display; inside it, labels are `text-axis` or `text-dim`. An editable value takes the colour of what it controls in the picture: `orange` by default, `teal` when it belongs to a teal curve, line or engine (Compressor's threshold, Hybrid Reverb's algorithm).
- `teal` is the value colour: dial arcs, graph curves, choosers.
- `orange` marks what you can edit in a display, and what is selected or on.
- Lines: `divider` between groups; `grid`, `grid-decade`, `grid-level` in graphs. Solid lines only.
- Text on an accent fill takes the colour of the surface behind it (`on-accent`).
- `text-dim` on `display` is Live's own pair at 3.9:1 in the dark theme, below 4.5:1. It is kept exact.

**Spacing and shape.** Whole pixels everywhere; dial centres on half pixels. `radius-display` (2 px) for displays and tiles; everything else is square. No shadows, gradients (except meters) or outlines on the body.

**Layout.** Six types, chosen by where the display goes (`LayoutTypes`). Rules that hold in every type:
1. The display explains, the body acts. Pictures, modes and secondary values live in the display, next to what they change, in their LCD look (**Max objects**).
2. One band, one baseline: bottom controls share label, ring and value rows, also across sections.
3. Global controls last. Output, then Dry/Wet, far right behind a divider; Dry/Wet centred `mix-inset` from the right edge. Extra globals stack upward on the 56 px module (Phaser-Flanger: Output, Warmth, Dry/Wet).
4. Links are drawn: a triangle from a display region to its dial; a 1 px connector from a toggle to its dial.
5. ± controls get a notch above the ring.
6. Graphs stay quiet: few lines, labels beside their line, curves on top of the grid.
7. At most one large dial per section, for the control that defines the device.
8. Each control sits beside the picture it changes.
9. Size the device to its content. The control count picks the layout type; past about 20 controls add pages, a fold-out or a selected-item editor (**Design logic**).

**Motion.** None of Live's static devices animate their chrome. Meters, curves and handles move with the signal and the parameters only.

## Iconography
Live devices use almost no icons. The ones that exist are glyphs drawn by Live: the fold triangle (▶ / ◀), menu triangles, the pointer triangle, and Ø for phase. In Max, an icon is a `live.text` with `pictures`, `usesvgviewbox 1` and `remapsvgcolors 1`, so the SVG takes the theme colour. `assets/Icons` holds five of Live's own icons, copied exactly from the manual; its README names each one's ink.

## Reference images
`assets/Reference` holds the 24 Live 12 audio effects from the Live 12 manual, at 100 % zoom (2x pixels, light theme). Measure from these. `assets/Accuracy` holds the kit-against-Live comparisons that prove the component values.
