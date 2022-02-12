const { _sha512: sha512 } = require('../sign');
const { i18nReplace } = require('../i18n');
const { copyToClipboard } = require('../clipboard')

const RE = /^((https?:\/\/)?(www\.)?pixiv\.net\/artworks\/)?(\d+)/i;

/**
 * @param {string} s
 * @returns {string?}
 */
function parseID(s) {
    let r = s.match(RE);
    if (r == null) return null;
    return r[4];
}

/**
 * @param {Object<string, Any>} s
 * @param {string} k key
 * @param {string | undefined} a 多余的数据
 * @returns {string}
 */
function genPara(s, k, a) {
    let pa = '';
    Object.getOwnPropertyNames(s).forEach((k) => {
        let v = s[k];
        if (typeof v != "string") v = v.toString();
        pa += '/' + encodeURIComponent(k) + '=' + encodeURIComponent(v);
    })
    if (typeof a == "string" && a) pa += '/' + a;
    if (k) {
        sign = sha512(k + pa.substring(1));
        pa = '/sign=' + sign + pa;
    }
    return pa;
}

window.addEventListener('load', () => {
    /**@type {HTMLInputElement}*/
    let pas = document.getElementById('pas');
    /**@type {HTMLInputElement}*/
    let sc = document.getElementById('sc');
    /**@type {HTMLInputElement}*/
    let gen = document.getElementById('gen');
    /**@type {HTMLInputElement}*/
    let o = document.getElementById('o');
    /**@type {HTMLSelectElement}*/
    let typ = document.getElementById('typ');
    /**@type {HTMLInputElement}*/
    let add = document.getElementById('add');
    /**@type {HTMLInputElement}*/
    let pagee = document.getElementById('page');
    /**@type {HTMLInputElement}*/
    let ser = document.getElementById('ser');
    /**@type {HTMLInputElement}*/
    let lan = document.getElementById('lan');
    /**@type {HTMLSelectElement}*/
    let sizee = document.getElementById('size');
    /**@type {HTMLInputElement}*/
    let oint = document.getElementById('oint');
    /**@type {HTMLInputElement}*/
    let cpclip = document.getElementById('cpclip');
    /**@type {HTMLInputElement}*/
    let afn = document.getElementById('afn');
    let i18n = window['i18n'];
    sc.addEventListener('paste', (ev) => {
        let data = (ev.clipboardData || window.clipboardData).getData("text");
        let re = parseID(data);
        if (re) {
            sc.value = re;
        }
        ev.preventDefault();
    })
    gen.addEventListener('click', () => {
        if (!sc.value) {
            alert(i18nReplace(i18n['ND'], { 'a': 'ID' }));
            return;
        }
        let id = sc.valueAsNumber;
        let type = typ.value;
        let d = { id };
        if (type != 'url') {
            d['t'] = type;
        } else {
            let page = pagee.valueAsNumber;
            if (isNaN(page) || page < 1) page = 1;
            if (page != 1) d['p'] = page;
        }
        let lang = lan.value;
        if (lang) {
            d['lang'] = lang;
        }
        let size = sizee.value;
        if (size != 'original' && size) {
            d['size'] = size;
        }
        d['f'] = afn.checked ? 1 : 0;
        let s = genPara(d, pas.value, add.value);
        let server = ser.value;
        if (!server) {
            server = window.location.origin;
        }
        o.value = server + '/pixiv/proxy' + s;
    })
    oint.addEventListener('click', () => {
        if (o.value) window.open(o.value, '_blank');
    })
    cpclip.addEventListener('click', () => {
        if (o.value) copyToClipboard(o, o.value);
    })
})
