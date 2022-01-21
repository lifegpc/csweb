const { i18nReplace } = require('./i18n');
const { Base64 } = require("js-base64")
const md5 = require("lifegpc-md5")
const sha256m = require("@stablelib/sha256")
const sha224m = require("@stablelib/sha224")
const arrayBufferToHex = require('array-buffer-to-hex')
const sha1 = require("lifegpc-sha1")
const hmac = require("@stablelib/hmac");
const sha512_224 = require("sha512-224");
const sha512_256m = require("@stablelib/sha512_256");
const sha384m = require("@stablelib/sha384");
const sha512m = require("@stablelib/sha512");
const { showElement, hideElement } = require('./element');
const { copyToClipboard } = require('./clipboard');
const { URLParams } = require('./url_params');

/**
 * Calculate sha224
 * @param {string} s Input string
 * @returns {string}
 */
function sha224(s) {
    let enc = new TextEncoder();
    let arr = enc.encode(s);
    let h = sha224m.hash(arr);
    return arrayBufferToHex(h.buffer);
}

/**
 * Calculate sha256
 * @param {string} s Input string
 * @returns {string}
 */
function sha256(s) {
    let enc = new TextEncoder();
    let arr = enc.encode(s);
    let h = sha256m.hash(arr);
    return arrayBufferToHex(h.buffer);
}

/**
 * Calculate sha512/256
 * @param {string} s Input string
 * @returns {string}
 */
function sha512_256(s) {
    let enc = new TextEncoder();
    let arr = enc.encode(s);
    let h = sha512_256m.hash(arr);
    return arrayBufferToHex(h.buffer);
}

/**
 * Calculate sha384
 * @param {string} s Input string
 * @returns {string}
 */
function sha384(s) {
    let enc = new TextEncoder();
    let arr = enc.encode(s);
    let h = sha384m.hash(arr);
    return arrayBufferToHex(h.buffer);
}

/**
 * Calculate sha512
 * @param {string} s Input string
 * @returns {string}
 */
function sha512(s) {
    let enc = new TextEncoder();
    let arr = enc.encode(s);
    let h = sha512m.hash(arr);
    return arrayBufferToHex(h.buffer);
}


/**
 * @param {Uint8Array} key 
 * @param {Uint8Array} data 
 * @returns {Uint8Array}
 */
function hmacSHA224R(key, data) {
    return hmac.hmac(sha224m.SHA224, key, data);
}

/**
 * @param {String} key 
 * @param {String} data 
 * @returns {String}
 */
function hmacSHA224(key, data) {
    let enc = new TextEncoder();
    let k = enc.encode(key);
    let d = enc.encode(data);
    let h = hmacSHA224R(k, d);
    return arrayBufferToHex(h.buffer);
}

/**
 * @param {Uint8Array} key 
 * @param {Uint8Array} data 
 * @returns {Uint8Array}
 */
function hmacSHA256R(key, data) {
    return hmac.hmac(sha256m.SHA256, key, data);
}

/**
 * @param {String} key 
 * @param {String} data 
 * @returns {String}
 */
function hmacSHA256(key, data) {
    let enc = new TextEncoder();
    let k = enc.encode(key);
    let d = enc.encode(data);
    let h = hmacSHA256R(k, d);
    return arrayBufferToHex(h.buffer);
}

/**
 * @param {Uint8Array} key 
 * @param {Uint8Array} data 
 * @returns {Uint8Array}
 */
function hmacSHA512_256R(key, data) {
    return hmac.hmac(sha512_256m.SHA512_256, key, data);
}

/**
 * @param {String} key 
 * @param {String} data 
 * @returns {String}
 */
function hmacSHA512_256(key, data) {
    let enc = new TextEncoder();
    let k = enc.encode(key);
    let d = enc.encode(data);
    let h = hmacSHA512_256R(k, d);
    return arrayBufferToHex(h.buffer);
}

/**
 * @param {Uint8Array} key 
 * @param {Uint8Array} data 
 * @returns {Uint8Array}
 */
function hmacSHA384R(key, data) {
    return hmac.hmac(sha384m.SHA384, key, data);
}

/**
 * @param {String} key 
 * @param {String} data 
 * @returns {String}
 */
function hmacSHA384(key, data) {
    let enc = new TextEncoder();
    let k = enc.encode(key);
    let d = enc.encode(data);
    let h = hmacSHA384R(k, d);
    return arrayBufferToHex(h.buffer);
}

/**
 * @param {Uint8Array} key 
 * @param {Uint8Array} data 
 * @returns {Uint8Array}
 */
function hmacSHA512R(key, data) {
    return hmac.hmac(sha512m.SHA512, key, data);
}

/**
 * @param {String} key 
 * @param {String} data 
 * @returns {String}
 */
function hmacSHA512(key, data) {
    let enc = new TextEncoder();
    let k = enc.encode(key);
    let d = enc.encode(data);
    let h = hmacSHA512R(k, d);
    return arrayBufferToHex(h.buffer);
}

/**
 * 比较Query
 * @param {Array<string>|string} ele1
 * @param {Array<string>|string} ele2
*/
function comparePara(ele1, ele2) {
    let e1 = typeof ele1 == "string" ? ele1 : ele1[0];
    let v1 = typeof ele1 == "string" ? "" : ele1[1];
    let e2 = typeof ele2 == "string" ? ele2 : ele2[0];
    let v2 = typeof ele2 == "string" ? "" : ele2[1];
    return e1 == e2 ? v1 == v2 ? 0 : v1 > v2 ? 1 : -1 : e1 > e2 ? 1 : -1;
}

/**
 * 生成Query
 * @param {Array<Array<string>|string>|Object.<string, string>} para 参数
 */
function genParaStr(para) {
    var r = new URLParams();
    if (para == undefined) return r.toString();
    else if (Array.isArray(para)) {
        para.sort(comparePara)
        for (let i = 0; i < para.length; i++) {
            let pair = para[i];
            if (Array.isArray(pair)) {
                r.append(pair[0], pair.length > 1 ? pair[1] : "");
            } else if (typeof pair == "string") {
                r.append(pair, "");
            }
        }
    }
    else {
        Object.getOwnPropertyNames(para).forEach((key) => {
            if (typeof para[key] == "string")
                r.append(key, para[key]);
        })
    }
    return r.toString()
}

window.addEventListener('load', () => {
    let bu = document.getElementById('bu');
    /**@type {HTMLInputElement}*/
    var pas = document.getElementById('pas');
    /**@type {HTMLInputElement}*/
    var sal = document.getElementById('sal');
    /**@type {HTMLSelectElement}*/
    var sel = document.getElementById('sel');
    let skeyd = document.getElementById('skeyd');
    /**@type {HTMLInputElement}*/
    let skey = document.getElementById('skey');
    /**
     * 检查选择的散列算法
     * @returns {boolean} true if is HMAC
     */
    function checkTypeSelect() {
        if (sel.selectedIndex > -1) {
            let e = sel.selectedOptions;
            if (e.length) {
                let ele = e[0];
                if (ele.parentElement.constructor.name == 'HTMLOptGroupElement') {
                    /**@type {HTMLOptGroupElement}*/
                    let p = ele.parentElement;
                    if (p.label == 'HMAC') {
                        return true;
                    }
                }
            }
        }
        return false;
    }
    sel.addEventListener('input', () => {
        if (checkTypeSelect()) showElement(skeyd); else hideElement(skeyd);
    })
    if (checkTypeSelect()) showElement(skeyd); else hideElement(skeyd);
    /**@type {HTMLButtonElement}*/
    var cl = document.getElementById('cl');
    /**@type {HTMLTextAreaElement}*/
    var o = document.getElementById('o');
    /**@type {HTMLInputElement}*/
    var loc = document.getElementById('loc');
    /**@type {HTMLInputElement}*/
    var base = document.getElementById('base');
    /**@type {HTMLInputElement}*/
    var api = document.getElementById('api');
    /**@type {HTMLDivElement}*/
    var apid = document.getElementById('apid');
    /**@type {HTMLDivElement}*/
    let apidl = document.getElementById('apidl');
    /**@type {Array<Array<string|number>>}*/
    let paral = [];
    /**@type {number} 输入框行数*/
    let inputc = 0;
    /**@type {number} 输入框id*/
    let inputi = 0;
    /**@type {HTMLLabelElement}*/
    let apipre = document.getElementById('apipre');
    /**@type {HTMLInputElement}*/
    let apiop = document.getElementById('apiop');
    /**@type {HTMLSpanElement}*/
    let apiopd = document.getElementById('apiopd');
    /**@type {HTMLInputElement}*/
    let apiopn = document.getElementById('apiopn');
    bu.addEventListener('click', () => {
        copyToClipboard(o, o.value);
    })
    api.checked ? showElement(apid) : hideElement(apid);
    api.addEventListener('input', () => {
        sal.disabled = api.checked;
        api.checked ? showElement(apid) : hideElement(apid);
        apiop.disabled = !api.checked;
        checkApiop();
        if (api.checked) {
            if (inputc == 0) {
                initializeApidl();
            }
        }
    })
    apiop.addEventListener('input', () => {
        checkApiop();
    })
    function checkApiop() {
        api.checked && apiop.checked ? showElement(apiopd) : hideElement(apiopd);
        apiopn.disabled = !api.checked || !apiop.checked;
    }
    /**
     * 增加输入框
     * @param {number?} index 位置
     */
    function addInputDiv(index = null) {
        let div = document.createElement('div');
        div.setAttribute('i', inputi);
        let para = ["", "", inputi];
        paral.push(para);
        let inp1 = document.createElement('input');
        inp1.style.width = "20%";
        inp1.style.minWidth = "50px";
        inp1.addEventListener('input', () => {
            para[0] = inp1.value;
            preview();
        })
        div.append(inp1);
        div.append(" = ");
        let inp2 = document.createElement('input');
        inp2.style.width = "60%";
        inp2.style.minWidth = "150px";
        inp2.addEventListener('input', () => {
            para[1] = inp2.value;
            preview();
        })
        div.append(inp2);
        let minus = document.createElement('input');
        minus.type = "button";
        minus.value = "-";
        minus.className = "minusb";
        minus.addEventListener('click', () => {
            removeInputDiv(div);
        })
        div.append(minus);
        let add = document.createElement('input');
        add.type = "button";
        add.value = "+";
        ((inputi) => {
            add.addEventListener('click', () => {
                addInputDiv(inputi);
            })
        })(inputi);
        div.append(add);
        /**@type {Element}*/
        let child = null;
        if (index != null) {
            for (let i = 0; i < apidl.childElementCount; i++) {
                child = apidl.children[i];
                if (parseInt(child.getAttribute("i")) == index) {
                    child = child.nextElementSibling
                }
            }
        }
        child ? apidl.insertBefore(div, child) : apidl.append(div);
        inputc++;
        inputi++;
        checkButtonStatus();
        preview();
    }
    function preview() {
        apipre.innerText = genParaStr(paral);
    }
    function initializeApidl() {
        addInputDiv();
    }
    function checkButtonStatus() {
        /**@type {HTMLCollectionOf<HTMLInputElement>} */
        let minusl = document.getElementsByClassName('minusb');
        for (let i = 0; i < minusl.length; i++) {
            minusl[i].disabled = inputc < 2;
        }
    }
    /**
     * 移除输入框
     * @param {HTMLDivElement} ele 父级div元素
     */
    function removeInputDiv(ele) {
        let ind = parseInt(ele.getAttribute("i"));
        ele.parentElement.removeChild(ele);
        for (let i = 0; i < paral.length; i++) {
            let para = paral[i];
            if (ind == para[2]) {
                paral.splice(i, 1);
                inputc--;
                preview();
                checkButtonStatus();
                return;
            }
        }
    }
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
        var i18n = window["i18n"];
        if (pas.validationMessage != "") {
            alert(pas.validationMessage);
            return;
        }
        var pass = pas.value;
        var salt = api.checked ? genParaStr(paral) : sal.value;
        var hat = sel.value;
        let isHMAC = checkTypeSelect();
        let key = "";
        if (isHMAC) {
            if (!skey.value.length) {
                alert(i18n['NOSKEY']);
                return;
            }
            key = skey.value;
        }
        var cn = loc.checked ? salt + pass : pass + salt;
        var hashs = "";
        if (hat == "md5") hashs = md5.md5(cn);
        else if (hat == "sha1") hashs = sha1.sha1(cn);
        else if (hat == "sha224") hashs = sha224(cn);
        else if (hat == "sha512-224") hashs = sha512_224.sha512_224(cn);
        else if (hat == "sha256") hashs = sha256(cn);
        else if (hat == "sha512-256") hashs = sha512_256(cn);
        else if (hat == "sha384") hashs = sha384(cn);
        else if (hat == "sha512") hashs = sha512(cn);
        else if (hat == "hmac-md5") hashs = md5.HmacMD5(key, cn);
        else if (hat == "hmac-sha1") hashs = sha1.HmacSHA1(key, cn);
        else if (hat == "hmac-sha224") hashs = hmacSHA224(key, cn);
        else if (hat == "hmac-sha512-224") hashs = sha512_224.HmacSHA512_224(key, cn);
        else if (hat == "hmac-sha256") hashs = hmacSHA256(key, cn);
        else if (hat == "hmac-sha512-256") hashs = hmacSHA512_256(key, cn);
        else if (hat == "hmac-sha384") hashs = hmacSHA384(key, cn);
        else if (hat == "hmac-sha512") hashs = hmacSHA512(key, cn);
        else {
            alert(i18n["UKNHASH"]);
            return;
        }
        o.value = base.checked ? hashs : base64(hashs);
        if (api.checked && apiop.checked) {
            let sp = new URLSearchParams(salt);
            sp.append(apiopn.value, o.value);
            o.value = sp.toString();
        }
    })
    /**@type {HTMLCollectionOf<HTMLInputElement>} */
    let showpasl = document.getElementsByClassName('showpas');
    for (let i = 0; i < showpasl.length; i++) {
        let showpas = showpasl[i];
        showpas.addEventListener('click', (ev) => {
            /**@type {HTMLInputElement}*/
            let t = ev.target;
            let targetN = t.getAttribute('target');
            if (!targetN) {
                console.error('Can not find "target" attribute.', t);
                return;
            }
            /**@type {HTMLInputElement}*/
            let target = document.getElementById(targetN);
            if (!target) {
                console.error('Can not find target "' + targetN + '".', t);
                return;
            }
            let tranKey = t.getAttribute('tran-key');
            if (!tranKey) {
                console.error('Can not find "tarn-key" attribute.', t);
                return;
            }
            let i18n = window['i18n'];
            let i18nN = Object.getOwnPropertyNames(i18n);
            if (i18nN.indexOf(tranKey) == -1) {
                console.error('Can not find translate key "' + tranKey + '".', t);
                return;
            }
            if (target.type == "password") {
                target.type = 'text';
                t.value = i18nReplace(i18n['HIDEX'], { 'sth': i18n[tranKey] });
            } else if (target.type == 'text') {
                target.type = 'password';
                t.value = i18nReplace(i18n['SHOWX'], { 'sth': i18n[tranKey] });
            } else {
                console.error('Unknown type "' + target.type + '".', t, target);
            }
        })
    }
})
