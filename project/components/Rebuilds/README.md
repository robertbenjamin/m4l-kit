Saturator, Channel EQ and Auto Pan-Tremolo rebuilt from this system's components and compared pixel by pixel with the Live 12 manual at 100 % zoom.

## What is traced, what is built
Only live data is copied from the reference image: curves, the spectrum, the wave picture, the LED levels, pointer angles and the five icons (which are Live's own glyphs, see `assets/Icons`). Everything else is drawn by `LiveKit` with the tokens: displays, dials, buttons, boxes, choosers, grids, text and positions.

## Result (pixels within 60 summed RGB of Live, body only, 2x)
| Device | Theme | Old kit | Now | Exact pixels |
|---|---|---|---|---|
| Saturator | Light Neutral | 97.4 % | 98.3 % | 95.0 % |
| Channel EQ | Light Neutral | 93.9 % | 97.0 % | 93.4 % |
| Auto Pan-Tremolo | Light Cool | n/a | 98.7 % | 92.1 % |

Every element sits at 0 px offset.

Regression check against Live itself (Live 12.4, dark, 100 %, measured with m4l-loop against a native Saturator set to the same state, without the band since it was silent): 96.0 % within 60 summed RGB, 93.5 % exact, every element at 0 px. The curve and dial angles are traced from the light-theme manual, so some of the gap is the trace. What remains is anti-aliasing: Chrome and Live shape glyph edges and curve edges differently (88 % of Auto Pan-Tremolo's remaining error is inside text).

The card renders in the page's current theme; the scores above are for each device's own theme.
