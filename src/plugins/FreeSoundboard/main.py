from voice import Voice

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "35.214.213.113"
port = 50008
ssrc = 793604
key = bytes([58,17,100,192,185,45,231,164,17,250,80,171,159,75,208,111,62,104,146,87,159,158,90,63,85,137,236,62,131,7,53,123])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        voice.play(sound)