#!/usr/bin/env python3
"""Turn a kit-built design page into m4l-loop's reference: ?ref=1&zoom=Z&theme=T renders the device body
alone, at its default state, in silence (no band, silent meter), on magenta for cropping.

usage: make_ref.py design.html design.ref.html"""
import sys

ANCHORS = [   # must match the design page's script exactly
    ("var zoom=Math.min(2,main.clientWidth/(W+4));", "var zoom=REF?+REF.get('zoom'):Math.min(2,main.clientWidth/(W+4));"),
    ("LiveKit.device(stage,{w:W,zoom:zoom})", "LiveKit.device(stage,{w:W,zoom:zoom,title:!REF})"),
    ("state.drive=0.16;state.auto=true;", "if(!REF){state.drive=0.16;state.auto=true;}"),
    ("  var DEF={", "  var REF=new URLSearchParams(location.search);REF=REF.has('ref')?REF:null;\n"
                    "  if(REF){document.documentElement.classList.add('ref');"
                    "document.getElementById('devices').className='th-'+(REF.get('theme')||'dark');}\n  var DEF={"),
    ("function meter(d,y,h,L){var o=toDb(L.out);", "function meter(d,y,h,L){var o=REF?-120:toDb(L.out);"),
    ("reach=Math.min(DOM,L.into);", "reach=REF?0:Math.min(DOM,L.into);"),
]
CSS = ("html.ref,html.ref body{background:#f0f!important;margin:0!important;padding:0!important}\n"
       "html.ref header,html.ref .bar,html.ref .copy,html.ref .variant+.variant{display:none!important}\n"
       "html.ref .variant{display:block!important;border:0!important;padding:0!important}\n"
       "html.ref main{gap:0!important;max-width:none!important}\n"
       "html.ref .lk-wrap{padding:0!important}\n")

src, dst = sys.argv[1:3]
s = open(src).read()
for a, b in ANCHORS:
    if s.count(a) != 1:
        sys.exit(f'anchor not found once: {a}')
    s = s.replace(a, b)
i = s.rfind('</style>')
open(dst, 'w').write(s[:i] + CSS + s[i:])
print('wrote', dst)
