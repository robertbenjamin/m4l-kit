A trigger performs an action once; it shows its state only while the action runs.

## Spec (100 %)
- A text button: `button-off` fill and `button-border` border at rest; `teal` fill while the action is active (Spectral Time's Freeze, 74 × 24 with a ✱ glyph).
- Output on mouse down when it is played live (Freeze), on mouse up otherwise.
- Use a toggle instead when the user needs to see the state afterwards.

## When to use

- **Use** for a one-shot action (Spectral Time Freeze, Drum Buss force-to-note).
- **Don't** when state you need to see afterwards: toggle.
- **Live 12 uses it** 2 times: Drum Buss, Spectral Time.
- **Max:** `live.text`, mode 0 Button; outputmode 0 Mouse down for performance controls. Status: docs.
