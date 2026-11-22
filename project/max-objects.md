# Max objects

Which Max object builds each element, with its settings, when Live 12 uses it and when not to. Settings come from the reference docs bundled with Live 12.4 (Max 9.1.5). **Verified** means checked in Live by screenshot; **docs** means taken from the reference but not yet compared with Live; **custom** means no `live.*` object draws it. The same table is in `max-objects.json` for tools.

## The LCD rule
Most `live.*` controls have two looks: `appearance 0` for the device body and `appearance 1`/`4` (**LCD**) for inside a display. Use the LCD look for every control that sits in a display: `live.numbox` 4 for values, `live.menu` 1 for choosers, `live.tab` 1 for mode buttons, `live.toggle` 1 for checkboxes.

## Controls

| Element | Object | Settings | Use when | Don't use when | Live uses | Status |
|---|---|---|---|---|---|---|
| Dial | `live.dial` | `appearance` 0 Vertical; `showname` 1; `shownumber` 1; `needlemode` 0 Automatic | A continuous value you play. | The value is set once (number box) or shapes the picture (display value). | 92 (Spectral Time, Hybrid Reverb, Echo, Phaser-Flanger) | verified |
| Notched dial | `live.dial` | `appearance` 0 Vertical; `triangle` 1; `needlemode` 2 Bipolar; `placement` 4 px higher than a plain dial | A ± value whose centre means "unchanged": gains, EQ bands, pan, width. | Centre is not a resting point (LFO amount, bias): use needlemode 2 without the triangle. | 15 (Channel EQ, Multiband Dynamics, Utility, EQ Eight) | verified |
| Large dial | `live.dial` | `appearance` 3 Large (50 × 63 box, bigger than Live's 37 px ring) or a larger appearance-0 box; `showname` 1; `shownumber` 1 | The control the device exists for; at most one per section, leading it. | Two in one section, or a device with one band and ≤ 5 controls. | 11 (Roar, Redux, Glue Compressor, Erosion) | docs |
| Stepped dial | `live.dial + live.comment` | `parameter` enum (parameter_type 2) with the steps; `labels` live.comment per step around the ring | A few fixed steps that read like hardware (Glue attack/ratio, Limiter lookahead). | More than about 7 steps (menu) or no hardware precedent. | 4 (Glue Compressor, Limiter) | custom |
| Number box | `live.numbox` | `appearance` 2 Slider; `size` 45 × 13 | A continuous value you set, or one that refines a dial (Fine, Trim, Window); columns that would overflow with dials. | The device's main controls. | 35 (Spectral Resonator, Auto Shift, Roar, Shifter) | verified |
| Bipolar number box | `live.numbox` | `appearance` 3 Bipolar; `size` 45 × 13 | A ± value you set (offsets, modulation depth, shift). | A ± value you play: notched dial. | 10 (Delay, Echo, Spectral Resonator, Auto Pan-Tremolo) | docs |
| Choice in a number box | `live.numbox` | `appearance` 2 Slider; `parameter` enum | An ordered choice that reads like an amount (Hybrid Reverb Vintage: Off → Oldest). | Unordered choices: menu. | 1 (Hybrid Reverb) | docs |
| Display value | `live.numbox` | `appearance` 4 LCD; `lcdbgcolor` transparent; `unit style` Custom (e.g. "%.0f %", "%.1f Hz") | A value that shapes the picture, placed inside the display next to it. | Mix and output. | 48 (Hybrid Reverb, Phaser-Flanger, Delay, Echo) | verified |
| Graph handle | `v8ui` | `radius` 13 px outer, 1.5 px ring; `grab` 9 px; `writes` two parameters (x, y) | A point on the picture that edits two parameters (frequency and gain/width). | A single value: display value or dial. | 6 (Erosion, Delay, Echo, Auto Shift) | verified |
| Text toggle | `live.text` | `mode` 1 Toggle; `appearance` 0 Default; `outputmode` 1 Mouse up | On/off on the body, named by what it switches on (Auto, Ping Pong, Mono). | View or audition switches (icon toggle); enabling a section (checkbox). | 48 (Utility, Multiband Dynamics, Shifter, Echo) | verified |
| Icon toggle | `live.text` | `mode` 1 Toggle; `usepicture` 1; `pictures` SVG; `usesvgviewbox` 1; `remapsvgcolors` 1 | Audition, spectrum, sidechain, link and freeze switches; Ø next to a dial. | When a word is clearer than an icon. | 23 (Roar, Delay, Auto Shift, EQ Eight) | docs |
| Checkbox | `live.toggle` | `appearance` 0 Default on the body, 1 LCD in a display; `outputmode` 1 Mouse up | Enabling a section or feature; its values dim when off. Also legends in a display (Compressor GR / Output). | Switching a mode (text toggle or segmented). | 14 (Auto Shift, Compressor, Spectral Time, Roar) | docs |
| Segmented pair | `live.tab` | `appearance` 0 Default; `livemode` 1; `mode` 0 Equal spaced; `rows` 1 | Two (sometimes three) short options side by side: 12 | 24, Pre | Post, Hz | ♪. | Options that change the whole picture: mode buttons in the display. | 11 (Shifter, Spectral Resonator, Spectral Time, Chorus-Ensemble) | docs |
| Radio stack | `live.tab` | `appearance` 0 Default; `livemode` 1; `stacking` one option per row (num_lines_presentation = N) | Three to four device modes in a column (Peak / RMS / Expand). | Five or more: menu. | 12 (Delay, Spectral Time, Limiter, Echo) | docs |
| Mode buttons | `live.tab` | `appearance` 1 LCD; `livemode` 1 | Two or three modes that change the whole picture, at the top of the display. | Settings that leave the picture alone. | 7 (Auto Pan-Tremolo, Phaser-Flanger, Chorus-Ensemble, Echo) | docs |
| Menu | `live.menu` | `appearance` 0 Default; `pictures` optional (EQ Eight filter shapes) | Four or more choices on the body. | A choice that belongs to the picture: chooser. | 18 (Auto Filter, Echo, EQ Eight, Hybrid Reverb) | docs |
| Chooser | `live.menu` | `appearance` 1 LCD; `triangle` 5 × 2.5 after the text | A choice inside the display that the picture depends on (Scale, Algorithm, Routing, Lookahead). | Choices unrelated to the picture. | 13 (Roar, Auto Shift, Hybrid Reverb, Saturator) | docs |
| Trigger | `live.text` | `mode` 0 Button; `outputmode` 0 Mouse down for performance controls | A one-shot action (Spectral Time Freeze, Drum Buss force-to-note). | State you need to see afterwards: toggle. | 2 (Drum Buss, Spectral Time) | docs |

## Structure and pictures

| Element | Object | Settings | Use | Status |
|---|---|---|---|---|
| Divider | `live.line` | `orientation` vertical; `note` draws at the left edge of its rect | Between control groups; behind the mix column. | verified |
| Label / section header | `live.comment` | `font` Ableton Sans Small 10; `colour` dynamic; `rect` (text x − 4, cap − 5) | Section names (Input, Smoothing, Mode) and display labels. | docs |
| Level meter | `live.meter~` | `orientation` 0 Vertical; `mode` 0 deciBel; `clip_size` 0 Normal; `stereo` two meters, 4 px wide, 1 px apart (it is mono) | Inside a display only. | docs |
| Display ground | `panel` | `bgfillcolor` themecolor.live_lcd_bg; `rounded` 2; `background` 1 | Behind every display; the picture is a v8ui over the graph area only. | verified |
| Section tile | `panel` | `bgfillcolor` body colour on the title-colour ground; `rounded` 2 | Tiled devices (type 4). | docs |
| Picture | `v8ui` | `colours` max.getcolor live_* theme ids; `size` the design's size (Max rounds the box up) | Curves, spectra, waves, segment meters. | verified |
| Prev / next arrows | `live.arrows` | — | Browsing a list of files (Hybrid Reverb IR). | docs |
| File drop | `live.drop` | — | Over a picture that accepts a dropped file (Hybrid Reverb IR). | docs |
| Fold-out arrow | `live.text + live.thisdevice` | `colours` all transparent; `glyph` ▶ / ◀; `resize` devicewidth 0, then setwidth | Past about six controls; Live's title-bar arrow is not available to Max devices. | verified |

## Objects with no audio-effect precedent

| Object | Ruling |
|---|---|
| `live.slider` | Fader. No Live 12 audio effect uses one; gains are dials (Utility, Limiter). |
| `live.gain~` | Fader with a built-in meter. No audio-effect precedent: use a dial plus live.meter~ in a display. |
| `live.grid, live.step` | Step sequencers. MIDI devices only. |
| `live.scope~` | Waveform display. Allowed as a picture inside a display when a v8ui is not needed. |
| `live.adsrui` | Envelope editor. Instruments only; an audio effect with an envelope uses dials (Auto Filter Envelope). |
| `live.button` | Bare flash dot. Live uses text buttons for triggers. |
| `live.dial appearance 1 Tiny / 2 Panel` | No Live 12 audio-effect precedent. |

## Live patterns Max devices cannot use

| In Live | Use instead |
|---|---|
| Page tabs in the title bar (Echo, Hybrid Reverb, Roar) | live.tab at the top of the body, or a fold-out. |
| Expand arrow in the title bar (Saturator, Roar) | Fold-out arrow in the display row. |
| Vertical side panels (Auto Filter, Roar sidechain / MIDI) | A fold-out, or leave the feature out. |

## Behind the scenes

`live.thisdevice` (init, resize), `live.colors` (redraw on theme change), `live.banks` (Push banks), `live.param~`, `live.object` / `live.observer` / `live.path` / `live.remote~` (Live API), `live.modulate~`, `live.routing`, `live.map`. They have no look; use them for behaviour only.
