# Sharing a device

A device you hand to someone else must be **one frozen file** that carries its scripts and its externals for **every system** they might use.

## 1. Freeze
```bash
python -m m4l_loop freeze DEVICE            # ~/Desktop/<NAME>.amxd
python -m m4l_loop inspect ~/Desktop/<NAME>.amxd
```
`inspect` lists every embedded file and, for each external, the systems it covers:
```
  aw.mackity~: macOS, Windows
```
Ship only when every external says both.

## 2. Cover every system
| System | External | Notes |
|---|---|---|
| macOS (Apple Silicon and Intel) | `.mxo` bundle, universal (`arm64` + `x86_64`) | Build with `-mmacosx-version-min=11.0` and ad-hoc sign it (`codesign --force --sign -`) |
| Windows x64 | `.mxe64` DLL | Without it, Max on Windows reports the object as not found, in every Max version. Built on a Mac as in §3, it loads and passes audio on Windows 11 (confirmed in Live 12 and the Live beta) |
| Windows on ARM running native Live | ARM64 build | Not covered. Most Windows PCs run x64 |

List both in the spec's `EXTERNALS`. `freeze` refuses to run while one is missing.

## 3. Build the Windows external on a Mac
Install the cross-compiler once (`brew install mingw-w64`), then compile and link against the Max SDK's x64 import libraries:
```bash
x86_64-w64-mingw32-g++ -std=gnu++17 -O3 -shared -DWIN_VERSION -DWIN64 \
  -I<sdk>/c74support/max-includes -I<sdk>/c74support/msp-includes  <your sources> \
  <sdk>/c74support/max-includes/x64/MaxAPI.lib <sdk>/c74support/msp-includes/x64/MaxAudio.lib \
  -static -static-libgcc -static-libstdc++ -s -o myobject~.mxe64
```
- `gnu++17`, not `c++17`: mingw's `math.h` only defines `M_PI` outside strict ANSI mode.
- `-static…` builds the C++ runtime in, so the DLL needs nothing installed.
- `-s` strips debug info. Without it, a 230 KB external comes out around 2.4 MB.

Check the result:
```bash
x86_64-w64-mingw32-objdump -p myobject~.mxe64 | grep -E "DLL Name|ext_main"
```
- It should export `ext_main`.
- It should import only Windows system DLLs (`KERNEL32`, `api-ms-win-crt-*`) plus `MaxAPI.dll` and `MaxAudio.dll`.

Check the Mac build the same way:
```bash
lipo -info myobject~.mxo/Contents/MacOS/*
otool -l myobject~.mxo/Contents/MacOS/* | grep minos
```

## 4. Prove it's self-contained
| Test | How | Proves |
|---|---|---|
| **Structure** | `inspect` | Every file is inside |
| **macOS, real** | Quit Live. Hide installed copies of the externals and scripts. Delete Max's unpack caches (`~/Library/Application Support/Cycling '74/Max 9/Settings/temp64-live/mxt/<name>` and `temp64-Max/mxt/<name>`). Start Live and load the file. | Live's log shows no "not found" error, and `lsof -p $(pgrep -x Live) \| grep <name>` shows the external loading from `temp64-live/mxt` |
| **Windows** | Someone on Windows loads it | No dashed red object box; audio passes |

Things that don't prove it:
- Loading into a Live that **already** loaded the external: Max keeps it in memory.
- Opening the file in standalone Max: that unpacks it into a project folder (`~/Documents/Max 9/Max for Live Devices/<Name> Project`) and loads from there. Delete that folder afterwards; it's on Max's search path.
- Marking the file as downloaded (quarantine) changed nothing on macOS 27 with an ad-hoc signed external.

## 5. How a frozen file is laid out
- An `ampf` header, then a `ptch` chunk holding an `mx@c` container: a 16-byte header, the files back to back, then a `dlst` directory of `dire` entries (type, name, size, offset, flags, date).
- The patch is the first entry (flag 17).
- Scripts are `TEXT`.
- A macOS external is four entries: a marker, a zip of the whole bundle, its executable and its `Info.plist`.
- A Windows external is one `mx64` entry.
- Max looks inside the frozen file before its search path.
