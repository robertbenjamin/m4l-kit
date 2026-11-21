"""M4LLoop: a Live remote script that lets m4l-loop drive Live over UDP 127.0.0.1:39123.

Select it once in Settings > Link, Tempo & MIDI > Control Surface. This file only owns the socket;
commands live in handler.py, which is re-imported per message so it can change without a restart.
"""
import importlib, json, socket

from _Framework.ControlSurface import ControlSurface

PORT = 39123


def create_instance(c_instance):
    return M4LLoop(c_instance)


class M4LLoop(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('127.0.0.1', PORT))
        self._sock.setblocking(False)
        self.schedule_message(1, self._poll)
        self.log_message('M4LLoop listening on %d' % PORT)

    def disconnect(self):
        self._sock.close()
        ControlSurface.disconnect(self)

    def _poll(self):
        try:
            while True:
                data, addr = self._sock.recvfrom(65536)
                try:
                    from . import handler
                    importlib.reload(handler)
                    reply = handler.handle(self, json.loads(data.decode('utf8')))
                except Exception as e:
                    reply = {'ok': False, 'msg': repr(e)}
                self._sock.sendto(json.dumps(reply).encode('utf8'), addr)
        except (BlockingIOError, socket.error):
            pass
        self.schedule_message(1, self._poll)
