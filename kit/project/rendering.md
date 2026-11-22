# How Live draws

Live's interface archives are encrypted and are not to be decrypted. A Max build doesn't need them: Live draws every `live.*` object itself. These findings make HTML mockups close enough to design with.

| Finding | Evidence |
|---|---|
| Text is grayscale anti-aliased and blended in a power-1.6 space, between sRGB and linear light: `out = (a·fg^1.6 + (1−a)·bg^1.6)^(1/1.6)` | One exponent fits both themes; text error down about 20 % |
| A text run is centred on its anchor, then its start is rounded to a whole px | Every label and value lands at 0 px offset in the Saturator rebuild |
| Positions are whole pixels; dial centres on half pixels | Phaser-Flanger dials at 56.5 / 108.5 / 160.5 / 243.5, buttons at 8 / 76 / 144 |
| The lit arc runs up to the pointer; the gap is cut only on the unlit side; the pointer's outer end is square | 8x zoom of Phaser-Flanger dials |
| Text on a selected button takes the colour of the surface behind it | #242424 in light displays, #181818 in dark |
| Raw theme-file colours differ from rendered pixels for accents (Live transforms them); neutrals match exactly | Default Dark Neutral Medium.ask |

## Rules found by rebuilding devices
| Finding | Evidence |
|---|---|
| Dial travel is ±150° | Dry/Wet 62 % at 35.97°, Output at maximum at 149.9° (Saturator) |
| The pointer is round at both ends; the ring gap is a pointer-shaped clearance (1.125 px, round ends), cut only from the unlit ring | Fitted on 10 dials in 3 devices; the cut runs parallel to the pointer |
| A dial's label centres 0.5 px right of the ring (1 px on notched dials); its value centres on the ring | Holds across Saturator, Channel EQ and Auto Pan-Tremolo |
| Centred text starts on a whole pixel of the device's grid; left-aligned text is not rounded | Auto Pan-Tremolo sits on a half-pixel grid |
| No rounding of glyph advances, no extra tracking | Rounded advances and ±0.08 px tracking both scored worse |
| Text blends in power 1.6 (1.45–1.6 equally good); no stem darkening | Exponent and coverage sweeps over all three devices |
| Grid lines, spectrum and axis text are translucent theme colours over the display | SpectrumGridLines #a6a6a63f renders #444444; at half opacity #343434; the same values give the dark theme's #3f3f3f / #2b2b2b |

## Checked in Live 12.4, dark (devloop, Mackity next to Saturator)
| Finding | Evidence |
|---|---|
| Kit text weight is right | Text ink, Live ÷ kit: dial labels 0.96–0.97, values 0.82–0.87. Live's text only looks bolder because its edges are sharper |
| Dim display text renders #868686, not #757575 | Saturator's Amt Lo and Max's live_lcd_control_fg_zombie both measure #868686; `text-dim` updated |
| Max colour-manages explicit RGB to the screen (P3 on this Mac); theme colours from max.getcolor land on the kit's measured values | #195a5f set in a v8ui shows #2d595e; live_value_arc shows the kit's #58c0d2 |
| Grid lines are translucent in Max too | live_spectrum_grid_lines over a band tints it; flatten it over live_lcd_bg for a solid crosshair |

## Kit accuracy
Pixels within 60 summed RGB of Live at 2x, body only. Every element sits at 0 px offset; the rest is edge shading between Chrome's and Live's rasterisers, most of it inside glyphs.

| Reference (100 % zoom) | First kit | Now |
|---|---|---|
| Saturator, light, manual | 97.4 % | 98.3 % |
| Channel EQ, light, manual | 93.9 % | 97.0 % |
| Auto Pan-Tremolo, light cool, manual | n/a | 98.7 % |
| Saturator, dark, Live 12.4 | 98.3 % | 96.0 % (re-run with m4l-loop; every element at 0 px) |
| Phaser-Flanger, light, manual | 94.7 % | not re-run |

The images are in `assets/Accuracy` and the live rebuilds in the Rebuilds component.
