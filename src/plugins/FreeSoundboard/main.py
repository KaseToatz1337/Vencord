from voice import Voice

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "35.214.211.3"
port = 50006
ssrc = 564001
key = bytes([88,129,175,6,143,5,14,52,214,20,180,163,255,108,207,178,145,254,183,59,182,255,113,31,182,17,53,85,205,42,98,126])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        voice.play(sound)