const {Base64} = require("js-base64")
const md5 = require("blueimp-md5")
window.addEventListener('load', () => {
    var ClipboardJS = window["ClipboardJS"];
    var clipboard = new ClipboardJS('#bu');
    clipboard["on"]('success', function (e) {
        e["clearSelection"]();
    });
    clipboard["on"]('error', function (e) {
        console.error('Action:', e["action"]);
        console.error('Trigger:', e["trigger"]);
    });
    /**@type {HTMLInputElement}*/
    var pas = document.getElementById('pas');
    /**@type {HTMLInputElement}*/
    var sal = document.getElementById('sal');
    /**@type {HTMLInputElement}*/
    var sel = document.getElementById('sel');
    /**@type {HTMLButtonElement}*/
    var cl = document.getElementById('cl');
    /**@type {HTMLTextAreaElement}*/
    var o = document.getElementById('o');
    /**@type {HTMLInputElement}*/
    var loc = document.getElementById('loc');
    /**@type {HTMLInputElement}*/
    var base = document.getElementById('base');
    /** 将散列值转换为Uint8Array
     *  @param {string} s
     * @returns {Uint8Array}
    */
    function hashtounit8(s) {
        var l = [];
        var t = s;
        if (t.length % 2 == 1) t = '0' + t;
        for (var i = 0; i < t.length; i += 2) {
            var ts = s.substr(i, 2);
            l.push(parseInt(ts, 16));
        }
        return new Uint8Array(l);
    }
    /** 将散列值转换为base64
     * @param {string} s
     * @returns {string}
    */
    function base64(s) {
        return Base64.fromUint8Array(hashtounit8(s));
    }
    cl.addEventListener('click', () => {
        if (pas.validationMessage != "") {
            alert(pas.validationMessage);
            return;
        }
        var pass = pas.value;
        var salt = sal.value;
        var hat = sel.value;
        var cn = loc.checked ? salt + pass : pass + salt;
        var hashs = "";
        var sha512 = window["sha512"];
        if (hat == "md5") hashs = md5(cn);
        else if (hat == "sha224") hashs = sha512["sha512_224"](cn);
        else if (hat == "sha256") hashs = sha512["sha512_256"](cn);
        else if (hat == "sha384") hashs = sha512["sha384"](cn);
        else if (hat == "sha512") hashs = sha512["sha512"](cn);
        else {
            alert("未知的散列算法");
            return;
        }
        o.value = base.checked ? hashs : base64(hashs);
    })
})
