from voice import Voice
from ogg import OggStream

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "35.214.225.36"
port = 50007
ssrc = 556535
key = bytes([135,170,83,5,237,57,242,87,243,62,232,208,43,135,194,125,50,214,135,152,188,8,36,6,248,22,123,35,87,13,41,107])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        ogg = OggStream.fromStream(sound).iterPackets()
        for frame in ogg:
            voice.sendPacket(frame)
        voice.sendSilence()