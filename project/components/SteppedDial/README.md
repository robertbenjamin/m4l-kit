A stepped dial chooses one of a few fixed values and prints them around the ring, like the hardware it models.

## Spec (Glue Compressor, Limiter, 100 %)
- A standard dial whose parameter is an enum; the pointer snaps to each step.
- The ring sits about 19 px below the label cap (10 px lower than a plain dial) so the printed steps fit between them; no value under the ring.
- A short tick at each step just outside the ring, the step's value printed beyond it in `text`.
- Up to about 7 steps (Glue's Release has 7). More becomes a menu.
- Use it only where the device models hardware or where the steps are few and ordered (Limiter's 1.5 / 3 / 6 ms).

## When to use

- **Use** for a few fixed steps that read like hardware (Glue attack/ratio, Limiter lookahead).
- **Don't** when more than about 7 steps (menu) or no hardware precedent.
- **Live 12 uses it** 4 times: Glue Compressor, Limiter.
- **Max:** `live.dial + live.comment`, parameter enum (parameter_type 2) with the steps; labels live.comment per step around the ring. Status: custom.
