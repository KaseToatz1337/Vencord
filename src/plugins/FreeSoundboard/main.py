from voice import Voice

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "35.214.243.21"
port = 50004
ssrc = 545370
key = bytes([76,245,253,112,244,77,251,108,62,119,217,221,16,115,234,149,251,105,191,176,241,186,124,15,37,89,72,76,13,114,171,12])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        voice.play(sound)