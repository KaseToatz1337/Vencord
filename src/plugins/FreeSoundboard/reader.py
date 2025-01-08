from __future__ import annotations

import threading
import struct

from scapy.all import sniff, Packet, IP, Raw, UDP
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from voice import Voice

class Reader(threading.Thread):
    def __init__(self, voice: Voice) -> None:
        super().__init__(daemon=True)
        self.voice = voice
        self.end = threading.Event()

    def intercept(self, packet: Packet) -> None:
        if packet[IP].dst == self.voice.ip and packet[UDP].dport == self.voice.port:
            data = packet[Raw].load
            if (data[:2] in [b"\x90\x78", b"\x80\x78"]):
                self.voice.sequence = struct.unpack("!H", data[2:4])[0]
                self.voice.timestamp = struct.unpack("!I", data[4:8])[0]
                self.voice.increment = struct.unpack(">I", data[-4:])[0]

    def run(self) -> None:
        sniff(filter="ip and udp", prn=self.intercept, store=0, stop_filter=lambda _: self.end.is_set())

    def stop(self) -> None:
        self.end.set()