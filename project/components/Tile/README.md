Tiles split a device into independent sections (type 4).

## Spec
- Tiles are `body` (or `display`) fields on a `title` ground, `tile-gutter` 2 px gutters and outer margin, `radius-display` 2 px.
- The first label cap sits 8 px into a tile. One large dial leads each tile.
- Bands line up across tiles: label 120, ring 130, value 156.
- Section headers only for sections with several controls, and never repeat a dial's label as a header.

## In Max
`panel` objects with theme colours under the controls.
