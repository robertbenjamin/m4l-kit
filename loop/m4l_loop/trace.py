"""Screen recordings of a device for animated behaviour (meters, lights, bands), traced frame by frame.

Recorded colours are shifted by the video encoder: compare colours only inside one recording,
against something whose true colour you know."""
import os, subprocess

import cv2


def record(seconds, path, region):
    """region: (x, y, w, h) in screen points."""
    if os.path.exists(path):
        os.remove(path)   # screencapture won't overwrite a recording
    subprocess.run(['screencapture', '-x', '-v', '-V', str(seconds), '-R', ','.join(str(int(v)) for v in region),
                    path], check=True)


def frames(path):
    """Yields (seconds, frame) for each frame of a recording."""
    cap = cv2.VideoCapture(path)
    while True:
        ok, f = cap.read()
        if not ok:
            return
        yield cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, f
