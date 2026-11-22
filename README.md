# m4l-kit

Design Max for Live devices that look native to Ableton Live, then build them and prove they match.

| Folder | What | Start at |
|---|---|---|
| [`kit/`](kit) | Design: a design system for HTML mocks that look exactly like Live 12 devices | `kit/project/README.md` |
| [`loop/`](loop) | Build: turn a mock into a real `.amxd`, compare it in a running Live, freeze it for macOS and Windows | `loop/README.md` |

The two halves meet at one point: the mock page. `loop/` opens it with `?ref=1` and compares Live against it. Nothing in `kit/` depends on Max.

Devices themselves live in their own repos and use this one.
