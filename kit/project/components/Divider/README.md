A divider is a 1 px line that separates control groups; the gap between groups is wider than the dial pitch.

## Spec
- `hairline` 1 px in `divider`. About 50 px tall from y ≈ 117 when it splits only the band; near full height when it splits columns (Redux, Utility, type 2's mix column).
- `divider-clear` 4 px of space on each side of it.
- Put the mix group (Output, Dry/Wet) behind the last divider.

## In Max
`live.line`. It draws at the left edge of its rect, not the centre: a divider placed by its centre lands 4 px left.
