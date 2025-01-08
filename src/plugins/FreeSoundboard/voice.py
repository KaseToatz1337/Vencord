import socket
import struct
import nacl.secret

from player import Player
from reader import Reader

class Voice:
    def __init__(self, ip: str, port: int, ssrc: int, key: bytes) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((ip, port))
        self.sock.setblocking(False)
        self.ip = ip
        self.port = port
        self.ssrc = ssrc
        self.key = key
        self.sequence = 0
        self.timestamp = 0
        self.increment = 0
        self.player = None
        self.reader = Reader(self)
        self.reader.start()

    def add(self, attr: str, value: int, limit: int) -> None:
        val = getattr(self, attr)
        if val + value > limit:
            setattr(self, attr, 0)
        else:
            setattr(self, attr, val + value)

    def createPacket(self, data: bytes) -> bytes:
        header = bytearray(12)
        header[0] = 0x80
        header[1] = 0x78
        struct.pack_into(">H", header, 2, self.sequence)
        struct.pack_into(">I", header, 4, self.timestamp)
        struct.pack_into(">I", header, 8, self.ssrc)
        return self.encrypt(header, data)
    
    def encrypt(self, header: bytes, data: bytes) -> bytes:
        box = nacl.secret.Aead(bytes(self.key))
        nonce = bytearray(24)
        nonce[:4] = struct.pack(">I", self.increment)
        self.add("increment", 1, 4294967295)
        return header + box.encrypt(bytes(data), bytes(header), bytes(nonce)).ciphertext + nonce[:4]
    
    def sendPacket(self, data: bytes) -> None:
        self.add("sequence", 1, 65535)
        packet = self.createPacket(data)
        self.sock.sendall(packet)
        self.add("timestamp", 960, 4294967295)

    def sendSilence(self) -> None:
        for _ in range(5):
            self.sendPacket(b"\xF8\xFF\xFE")

    def play(self, url: str) -> None:
        if self.player and self.player.playing.is_set():
            self.player.stop()
        self.player = Player(self, url)
        self.player.start()