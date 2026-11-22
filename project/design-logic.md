# Design logic

How Live's developers decide what goes on a device and where. Read from all 370 controls on 23 Live 12 audio effects; the full case study, with counts and images, is at https://claude.ai/artifact/RdsKkG66wELJxQXCsZWAXu. Answer these six questions in order; each answer narrows the next.

## 1. What can be drawn?
- The picture of what the device does gets the display. No picture, no display (Redux, Utility).
- Values that change the picture go inside it: display values, choosers and graph handles live only in displays (48 / 13 / 6 of 6).
- Small devices put about half their controls in the display (Saturator 4 of 7); large ones 5–35 %.
- A value takes the colour of what it controls in the picture (Hybrid Reverb: orange = convolution, teal = algorithm).
- Mix and output stay out of the display.

## 2. What is the device for?
- One control is the reason to load the device. It goes first or in the middle of the band, or gets the large dial when there is room.
- Large dial: at most one per section, leading it. 9 of 11 control the core sound; the others set the gain that drives it.
- A device whose picture is the point (Delay, Echo, Compressor) has no large dial.

## 3. Which way does the signal go?
- Left: input gain, timing (sync, divisions, attack, release), detection, sidechain, MIDI.
- Middle: the display, the band under it and section tiles: core sound, tone, modulation.
- Right: output, mode switches, stereo, then Dry/Wet at the bottom. Globals stack upward from Dry/Wet.
- Dry/Wet is the last control whenever it exists (16 of 23). Correction and utility devices have none (EQs, Limiter, Utility, Auto Pan-Tremolo, Erosion, Multiband Dynamics).

## 4. What kind of value is it?
| Kind | Element | Max object (see Max objects) |
|---|---|---|
| Continuous, played | dial | `live.dial` |
| Continuous, set once or refining a dial | number box | `live.numbox` 2 |
| Continuous, shapes the picture | display value | `live.numbox` 4 |
| ± with a natural zero | notched dial | `live.dial` triangle 1 |
| ± set once | bipolar number box | `live.numbox` 3 |
| On / off | text toggle; icon toggle for view, audition, link; checkbox to enable a section | `live.text`, `live.toggle` |
| 2 choices | segmented pair | `live.tab` |
| 3 choices | radio stack | `live.tab` |
| 2–3 modes that change the picture | mode buttons in the display | `live.tab` LCD |
| 4+ choices | menu; chooser when it belongs to the picture | `live.menu`, `live.menu` LCD |
| Few fixed hardware-like steps | stepped dial with printed values | `live.dial` + `live.comment` |
| Tempo-synced time | dial plus a Hz \| ♪ or ms \| ♪ pair | `live.dial` + `live.tab` |
| One-shot action | trigger button | `live.text` button |
| Auto-gain (output follows drive) | text toggle named Gain Comp (Makeup only for a compressor's make-up gain); a display button in the display strip when there is one | `live.text` |
| A state the device reports (clipping) | indicator light, in the display strip | `v8ui` |

## 5. What modifies what?
- A modifier toggle sits against its dial: under it (Auto under Release, Mono under Width), or beside it tied by a short line in a full band (Ø beside Feedback, Hz | ♪ beside Rate). A toggle about the picture goes in the display strip.
- A section that can be off gets a checkbox; its values dim while it is off.
- Repeated units are aligned rows (Multiband bands) or one editor for the selected item (EQ Eight).

## 6. How many controls?
| Controls | Layout |
|---|---|
| 6–12, one picture | Type 1, display over band |
| 13 with three globals | Type 2, mix column |
| 8–12, nothing to draw | Type 5, controls only |
| 9–27, the picture needs height | Type 3a, full-height display |
| 8–26, display plus side columns | Type 3b |
| 22–30, independent stages | Type 4, tiles |
| 1–3, one picture | Type 1 sized to content, extras in the display strip (Mackity, 131 px) |
- Past about 20 controls, add a second level: pages, fold-outs, or a selected-item editor. Live's title-bar pages and side panels aren't available to Max devices (see Max objects).
- Independent stages get their own tile with an on/off header; stages that feed one picture share a band.

## Known exceptions
- Dry/Wet as a number box where its column is made of boxes (Auto Shift, Roar, Redux); inside the meter display in Drum Buss.
- Bipolar dials without a notch where centre isn't a resting point (Shifter LFO Amount, Roar Bias, Auto Shift Pitch).
