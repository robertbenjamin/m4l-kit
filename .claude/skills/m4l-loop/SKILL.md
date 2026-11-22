---
name: m4l-loop
description: Make a Max for Live device match its HTML design in a running Ableton Live, measured pixel by pixel and against Live's native devices. Use when building, polishing or checking the look or behaviour of a Max for Live device.
---

1. Read `README.md` and `docs/workflow.md`. Keep `docs/gotchas.md` open while building.
2. Check that Live is listening: `python -m m4l_loop live '{"cmd": "ping"}'`. If it isn't, run `setup` and walk the user through the one-time Control Surface step.
3. Read `state`, and snapshot the parameters of anything you'll touch. Restore them when you're done, and delete only devices you added. If the set changes without you, stop and ask.
4. Iterate with `python -m m4l_loop loop DEVICE`. Fix the largest `live_is_off_by` first. Read Max's console lines after every build.
5. When the device and the design disagree, measure the native device in the same capture (`native`, then `snap`). Fix the design if Live disagrees with it.
6. Match motion with the same input, one device processing at a time, using `record` and `m4l_loop.trace`.
7. Record new facts about Live in the design system, as neutral reference detail. Add new tooling facts to `docs/gotchas.md`.
8. To share a device, follow `docs/sharing.md`: freeze it with both the macOS and the Windows external, check it with `inspect`, and prove it in a fresh Live with every installed copy and cache removed.
