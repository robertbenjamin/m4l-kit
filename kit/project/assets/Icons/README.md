Five of Live's own device icons, copied from the Live 12 manual at 100 % zoom as exact anti-aliased coverage (each 0.5 px cell keeps Live's opacity). Single ink: the files are black, so recolour them with the token their device uses. viewBox units are 1x body px.

| Icon | Device | Ink |
|---|---|---|
| eq-filter-shape | Channel EQ filter button | `display` on `orange` |
| lfo-shape | Auto Pan-Tremolo shape dropdown | `on-accent` on `orange` |
| phase-invert (Ø) | Auto Pan-Tremolo phase toggle | `on-toggle` on `orange` |
| swap-direction (↑↓) | Auto Pan-Tremolo outlined toggle | `orange` on `display` |
| phase-offset-wave | Auto Pan-Tremolo phase offset | `text-dim` on `display` |

In Max, put an icon on a `live.text` with `pictures`, `usesvgviewbox 1` and `remapsvgcolors 1` so it follows the theme.
