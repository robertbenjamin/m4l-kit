# Workflow

## 1. Static match
1. **Start from an approved design.** Give it a reference mode (see [device-spec.md](device-spec.md#the-reference-page)).
2. **Build to the numbers.** Copy every rect from the design into the spec. Name the parts you care about in `ELEMENTS`.
3. **Loop.** Run `python -m m4l_loop loop DEVICE`, or `watch` to rerun it on every save.
   - `build` prints any new **Max console messages**. Max's console is hidden inside Live, but Live copies it into its `Log.txt`, and m4l-loop reads it back.
   - Script errors from a `v8ui` appear there too if the script calls `error()`.
4. **Fix the biggest offset first.** If an element is `live_is_off_by [1, -1.5]`, move its rect by (−1, +1.5).
5. **Stop when every element shows `[0, 0]`** and the only residual left is text edges.

## 2. When the device and the design disagree, ask Live
A design is a model of Live, and some of its values may be estimates. When a mismatch could be the design's fault, measure the native device the design copies:
```bash
python -m m4l_loop live '{"cmd": "native", "name": "Saturator"}'   # loads next to yours, on the M4L Loop track
python -m m4l_loop snap DEVICE                                       # window.png now holds both devices
```
Read sizes, positions and colours from `window.png`, where both devices sit in the same capture. If the native device disagrees with the design, the native device wins: update the design and its design system, then rebuild.

Things worth measuring this way:
- button padding
- dim-text colour
- how a light looks when it's off
- the draw order of overlapping layers

## 3. Matching motion
Meters, lights and level-driven graphics are judged in motion.
1. **Same input, one device at a time.** Put a loop on the M4L Loop track. Set each device's `Device On` with `param`, so only one processes at once; devices in series feed each other changed audio.
2. **Play:** `python -m m4l_loop live '{"cmd": "transport", "play": true, "from_loop": true}'`.
3. **Record:** `python -m m4l_loop record DEVICE 5 --extra 300` captures your device plus 300 points to its right (the native device).
4. **Trace** the recording frame by frame with `m4l_loop.trace.frames()`: brightness at a light's centre, a band's edges, and so on. Compare:
   - **ranges** (5th to 95th percentile)
   - **fall time constants:** fit `ln(ratio) / dt` on falling frames
   - **how the shape scales** when you step a parameter
5. **Colours from video:** encoders shift colours. Compare an unknown colour only against a colour you know, in the same recording.

## 4. Leave things as you found them
The person you work for may be using the same Live set.
- Before you change anything, read `state` and the `param` values of anything you'll touch.
- Restore those values when you're done.
- Delete only devices you added.
- If devices or values change without you, someone else is working: stop and ask.

`build` keeps a device's settings and its place in the chain across reloads.

## 5. Write it down where it belongs
- **Facts about Live** (sizes, colours, timing) go in your design system, as reference detail: "if you use X, Live does Y". Phrase them so they don't push future designs toward or away from any element.
- **Facts about the tooling** go in [gotchas.md](gotchas.md).
- **Open questions** go in the tracker.
