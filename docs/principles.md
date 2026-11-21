# Principles

- **Make errors visible first.** Read Max's console (in Live's log) and your scripts' `error()` output before changing anything. Most "it doesn't draw" problems announce themselves there.
- **Measure, don't assume.** Every offset, colour, padding and timing is one capture away. Treat a number you haven't measured as a guess, and mark it as one.
- **Test what ships.** Iterate on the real `.amxd` in Live, not a stand-in, wrapper or browser mock-up.
- **Native devices are the ground truth.** When your design and Live disagree, measure Live's own device in the same capture, and fix the design.
- **One variable at a time.** Isolate devices (one processing at a time, same input) and change one thing per loop.
- **Fix the biggest offset first.** Later offsets often disappear once the big one is right.
- **Leave the set as you found it.** Snapshot what you touch, restore it, and stop when you see changes you didn't make.
- **Keep restarts one-off.** Anything that needs a Live restart belongs in setup. Logic that changes goes where it reloads by itself.
- **Write findings as reference, not rules.** "If a graph shows a driven band, Saturator fades it with a 0.3 s time constant" informs later designs without steering them.
