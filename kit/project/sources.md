# Sources and measuring

## Sources
| Source | Use | Trap |
|---|---|---|
| Live 12 manual images, `ableton-production.imgix.net/live-manual/12/<Name>L12.png` | Every device at 100 % zoom, 2x pixels | Light theme. Crop: title bar is the first 34 px at 2x |
| Screenshots from Live | Dark theme | Confirm 100 % zoom first: body 169 px, dial ring 26 px. The first screenshots were at 110 % and made every measurement 10 % too big |
| `Themes/*.ask` in Live's app resources | Plain-XML theme colours | Accents differ from rendered pixels |
| Ableton's Max for Live production guidelines (github.com/Ableton/maxdevtools) | Official rules | |
| Live 12 release notes | Which devices are new or redesigned | |

Live 12 devices to learn from: Roar (12.0), Multiband Dynamics (12.0), Saturator (12.1), Limiter (12.1), Auto Shift (12.1), Auto Filter (12.2), Compressor (12.2), Auto Pan-Tremolo (12.3), Erosion (12.4). Overdrive, Pedal, Redux, Dynamic Tube and Gate are older designs: don't copy their look.

## Method
1. Measure Live renders at 100 % (blob analysis per colour, then slide each element ±6 px to find the lowest error).
2. Encode the values as components.
3. Prove the components by rebuilding real devices and diffing pixels.
4. Extract rules that hold across many devices; design new devices from the rules, not by copying one device.
5. Build in Max, then check in Live by screenshot and by driving the mouse.

## Mistakes not to repeat
- Measuring from 110 % screenshots as if they were 100 %.
- Scaling a small dial up instead of measuring a real large dial.
- Designing from one old device instead of the Live 12 set.
- Bordered boxes in `content-box`, 2 px too large.
- Placing rows by eye, off the 56 px module.
- Using a layout type outside its measured width range.
- Inventing components: bold section headers, dashed lines, extra ticks, meters on the body.
- Grid lines drawn over curves and handles.
- Swapping the threshold (teal) and gain-reduction (orange) line colours.
- Calling a design native before seeing it rendered in Live.
- Dial travel ±145° (it is ±150°), a square pointer tip (it is round) and a radial gap in the ring (it is a pointer-shaped clearance).
- Measuring plain and notched dials with one shared offset: they need separate ones.
- Flat grey grid lines and spectrum (both are translucent theme colours).
- A 48 px number box (it is 45 px; the 48 came from 110 % screenshots).
