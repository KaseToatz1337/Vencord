import struct
import requests

from io import BytesIO
from typing import Generator, Tuple
from typing_extensions import Self

class OggPage:
    header = struct.Struct('<xBQIIIB')

    def __init__(self, stream: BytesIO) -> None:
        header = stream.read(struct.calcsize(self.header.format))
        self.flag, self.gran_pos, self.serial, self.pagenum, self.crc, self.segnum = self.header.unpack(header)
        self.segtable: bytes = stream.read(self.segnum)
        bodylen = sum(struct.unpack("B" * self.segnum, self.segtable))
        self.data: bytes = stream.read(bodylen)

    def iterPackets(self) -> Generator[Tuple[bytes, bool], None, None]:
        packetlen = offset = 0
        partial = True
        for seg in self.segtable:
            if seg == 255:
                packetlen += 255
                partial = True
            else:
                packetlen += seg
                yield self.data[offset : offset + packetlen], True
                offset += packetlen
                packetlen = 0
                partial = False
        if partial:
            yield self.data[offset:], False

class OggStream:
    def __init__(self, stream: BytesIO) -> None:
        self.stream: BytesIO = stream

    def nextPage(self) -> OggPage | None:
        head = self.stream.read(4)
        if head == b"OggS":
            return OggPage(self.stream)
        elif not head:
            return None

    def iterPages(self) -> Generator[OggPage, None, None]:
        page = self.nextPage()
        while page:
            yield page
            page = self.nextPage()

    def iterPackets(self) -> Generator[bytes, None, None]:
        partial = b""
        for page in self.iterPages():
            for data, complete in page.iterPackets():
                partial += data
                if complete:
                    yield partial
                    partial = b""

    @classmethod
    def fromStream(cls, url: str) -> Self:
        return cls(BytesIO(requests.get(url).content))