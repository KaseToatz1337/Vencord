from voice import Voice

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "66.22.199.87"
port = 50022
ssrc = 286567
key = bytes([58,89,125,89,197,95,201,252,18,68,152,213,115,224,141,21,148,82,188,8,227,191,93,129,4,201,23,168,158,67,204,81])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        voice.play(sound)