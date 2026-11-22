"""M4LLoop commands. Re-imported on every message, so edits here need no Live restart.

Every message is JSON {"cmd": ..., ...}; every reply is {"ok": bool, "msg": str, ...}.
Devices you test live on a track named "M4L Loop", created on first use.

  ping
  reload    {"folder": [...], "file": "X.amxd", "device": "X"}   swap device X for the fresh file in its slot,
                                                                keeping its settings; or load it on M4L Loop
  native    {"name": "Saturator"}            load a Live audio effect on M4L Loop, as a reference
  remove    {"name": "Default Saturator"}    delete a device from M4L Loop (Live's name, e.g. "Default ...")
  only      {"keep": ["X"]}                  delete every other device from M4L Loop
  param     {"device": "X"}                  list its parameters [name, value, min, max]
            {"device": "X", "name": "Drive", "value": 0.5}     set one (LOM value: linear in dial position)
  transport {"play": true, "from_loop": true}                 play (from the loop start) or stop
  song                                       playing, position, loop
  state                                      tracks and their devices
  clips                                      session and arrangement clips
  levels                                     track output levels
  routing                                    M4L Loop's routing choices
  route     {"in": "Main", "out": "Sends Only", "monitor": 1}  monitor: 0 In, 1 Auto, 2 Off
"""
import Live

TRACK = 'M4L Loop'


def handle(cs, m):
    song = cs.song()
    cmd = COMMANDS.get(m.get('cmd'))
    if cmd is None:
        return {'ok': False, 'msg': 'unknown cmd %r' % m.get('cmd')}
    return cmd(song, m)


def ping(song, m):
    return {'ok': True, 'msg': 'pong'}


def reload(song, m):
    app = Live.Application.get_application()
    item = find_item(app.browser.user_library, m['folder'], m['file'])
    if item is None:
        return {'ok': False, 'msg': 'not in the browser: %s' % '/'.join(m['folder'] + [m['file']])}
    found = find_device(song, m['device'])
    if found:
        track, index = found
        old = {p.name: p.value for p in track.devices[index].parameters}
        song.view.selected_track = track
        song.view.select_device(track.devices[index])
        app.browser.load_item(item)    # lands at the end of the chain
        track.delete_device(index)
        song.move_device(track.devices[-1], track, index)
        kept = 0
        for p in track.devices[index].parameters:
            if p.name in old:
                try:
                    p.value = max(p.min, min(p.max, old[p.name]))
                    kept += 1
                except Exception:
                    pass
        msg = 'replaced on %s at %d, kept %d settings' % (track.name, index, kept)
    else:
        track = dev_track(song)
        song.view.selected_track = track
        app.browser.load_item(item)
        index = len(track.devices) - 1
        msg = 'loaded on %s' % track.name
    show(song, track, index)
    return {'ok': True, 'msg': msg}


def native(song, m):
    app = Live.Application.get_application()
    item = next((c for c in app.browser.audio_effects.children if c.name == m['name'] and c.is_loadable), None)
    if item is None:
        return {'ok': False, 'msg': 'no audio effect named %s' % m['name']}
    track = dev_track(song)
    song.view.selected_track = track
    if len(track.devices):
        song.view.select_device(track.devices[-1])
    app.browser.load_item(item)
    show(song, track, len(track.devices) - 1)
    return {'ok': True, 'msg': 'loaded %s on %s' % (m['name'], track.name)}


def remove(song, m):
    track = dev_track(song)
    for i, d in enumerate(track.devices):
        if d.name == m['name']:
            track.delete_device(i)
            return {'ok': True, 'msg': 'removed %s' % m['name']}
    return {'ok': False, 'msg': '%s not on %s' % (m['name'], track.name)}


def only(song, m):
    t = dev_track(song)
    for i in reversed(range(len(t.devices))):
        if t.devices[i].name not in m['keep']:
            t.delete_device(i)
    return {'ok': True, 'msg': '%s: %s' % (TRACK, [d.name for d in t.devices])}


def param(song, m):
    found = find_device(song, m['device'])
    if not found:
        return {'ok': False, 'msg': 'no device %s' % m['device']}
    d = found[0].devices[found[1]]
    if 'name' not in m:
        return {'ok': True, 'msg': 'params', 'params': [[p.name, p.value, p.min, p.max] for p in d.parameters]}
    p = next(p for p in d.parameters if p.name == m['name'])
    p.value = max(p.min, min(p.max, m['value']))
    return {'ok': True, 'msg': '%s %s = %s' % (d.name, p.name, p.value)}


def transport(song, m):
    if m['play']:
        if m.get('from_loop'):
            song.loop = True
            song.current_song_time = song.loop_start
        song.start_playing()
    else:
        song.stop_playing()
    return {'ok': True, 'msg': 'playing' if m['play'] else 'stopped'}


def song_state(song, m):
    return {'ok': True, 'msg': 'song', 'playing': song.is_playing, 'time': song.current_song_time,
            'loop': [song.loop, song.loop_start, song.loop_length]}


def state(song, m):
    return {'ok': True, 'msg': 'state', 'selected': song.view.selected_track.name,
            'tracks': [[t.name, [d.name for d in t.devices]] for t in song.tracks]}


def clips(song, m):
    out = []
    for t in song.tracks:
        for i, slot in enumerate(t.clip_slots):
            if slot.has_clip:
                out.append(['session', t.name, i, slot.clip.name, slot.clip.is_audio_clip, slot.is_playing])
        for c in ([] if t.is_foldable else t.arrangement_clips):   # group tracks have no clips
            out.append(['arrangement', t.name, c.name, c.start_time, c.end_time, c.is_audio_clip])
    return {'ok': True, 'msg': 'clips', 'clips': out}


def levels(song, m):
    return {'ok': True, 'msg': 'levels',
            'tracks': [[t.name, round(t.output_meter_level, 3)] for t in list(song.tracks) + [song.master_track]]}


def routing(song, m):
    t = dev_track(song)
    return {'ok': True, 'msg': 'routing', 'in': [r.display_name for r in t.available_input_routing_types],
            'out': [r.display_name for r in t.available_output_routing_types],
            'current': [t.input_routing_type.display_name, t.output_routing_type.display_name],
            'monitor': t.current_monitoring_state}


def route(song, m):
    t = dev_track(song)
    for key, attr, avail in (('in', 'input_routing_type', t.available_input_routing_types),
                             ('out', 'output_routing_type', t.available_output_routing_types)):
        if key in m:
            setattr(t, attr, next(r for r in avail if r.display_name == m[key]))
    if 'monitor' in m:
        t.current_monitoring_state = m['monitor']
    return {'ok': True, 'msg': 'in %s, out %s' % (t.input_routing_type.display_name, t.output_routing_type.display_name)}


def show(song, track, index):
    app = Live.Application.get_application()
    song.view.select_device(track.devices[index])
    app.view.show_view('Detail/DeviceChain')
    app.view.focus_view('Detail/DeviceChain')


def dev_track(song):
    for t in song.tracks:
        if t.name == TRACK:
            return t
    song.create_audio_track(-1)
    t = song.tracks[-1]
    t.name = TRACK
    while len(t.devices):            # the Default Track template adds its own devices
        t.delete_device(0)
    return t


def find_item(node, folder, name):
    for part in folder:
        node = next((c for c in node.children if c.name == part), None)
        if node is None:
            return None
    stem = name.rsplit('.', 1)[0]
    return next((c for c in node.children if c.name in (name, stem) and c.is_loadable), None)


def find_device(song, name):
    for track in list(song.tracks) + list(song.return_tracks) + [song.master_track]:
        for i, d in enumerate(track.devices):
            if d.name == name:
                return track, i
    return None


COMMANDS = {'ping': ping, 'reload': reload, 'native': native, 'remove': remove, 'only': only, 'param': param,
            'transport': transport, 'song': song_state, 'state': state, 'clips': clips, 'levels': levels,
            'routing': routing, 'route': route}
