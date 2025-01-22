from voice import Voice

sound = "https://cdn.discordapp.com/soundboard-sounds/1239639522384547910"

ip = "66.22.199.102"
port = 50009
ssrc = 376590
key = bytes([249,114,95,245,93,111,148,224,202,166,101,150,106,50,17,27,3,112,160,176,44,15,122,76,169,20,3,41,165,107,6,237])

if __name__ == "__main__":
    voice = Voice(ip, port, ssrc, bytes(key))
    while True:
        input()
        voice.play(sound)