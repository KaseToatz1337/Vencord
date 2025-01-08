from __future__ import annotations

import threading
import time

from typing import TYPE_CHECKING
from ogg import OggStream

if TYPE_CHECKING:
    from voice import Voice

class Player(threading.Thread):

    def __init__(self, voice: Voice, url: str) -> None:
        super().__init__(daemon=True)
        self.voice = voice
        self.source = url
        self.end = threading.Event()
        self.playing = threading.Event()

    def run(self) -> None:
        self.playing.set()
        start = time.perf_counter()
        loops = 0
        packets = OggStream.fromStream(self.source).iterPackets()
        for packet in packets:
            if (self.end.is_set()):
                return
            self.voice.sendPacket(packet)
            loops += 1
            time.sleep(max(0, 0.02 + ((start + 0.02 * loops) - time.perf_counter())))
        self.voice.sendSilence()
        self.playing.clear()

    def stop(self) -> None:
        self.end.set()