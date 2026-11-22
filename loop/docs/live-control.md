# Live control

The M4LLoop remote script listens on UDP `127.0.0.1:39123`. Send it a command from the shell:
```bash
python -m m4l_loop live '{"cmd": "state"}'
```
or from Python:
```python
from m4l_loop import live
live.send({'cmd': 'param', 'device': 'Mackity', 'name': 'Drive', 'value': -24})
```
Devices under test live on a track named **M4L Loop**, which is created on first use.

| Command | Fields | Does |
|---|---|---|
| `ping` | | Checks that Live is listening |
| `reload` | `folder`, `file`, `device` | Swaps the device for the fresh file, in its slot and keeping its settings. If it isn't loaded yet, loads it on M4L Loop |
| `native` | `name` | Loads a Live audio effect on M4L Loop, for comparison |
| `remove` | `name` | Deletes a device from M4L Loop, using the name Live shows (e.g. "Default Saturator") |
| `only` | `keep` | Deletes every other device from M4L Loop |
| `param` | `device` | Lists its parameters: `[name, value, min, max]` |
| `param` | `device`, `name`, `value` | Sets one parameter. `value` is the LOM value |
| `transport` | `play`, `from_loop` | Plays (optionally from the loop start) or stops |
| `song` | | Returns whether it's playing, the position and the loop |
| `state` | | Lists tracks and their devices |
| `clips` | | Lists session and arrangement clips |
| `levels` | | Returns track output levels |
| `routing` / `route` | `in`, `out`, `monitor` | Reads or sets M4L Loop's routing. `monitor`: 0 In, 1 Auto, 2 Off |

To add a command, add a function to `remote_script/M4LLoop/handler.py` and register it in `COMMANDS`. Then run any command once: `send` copies the script into Live, and the next message loads it.
