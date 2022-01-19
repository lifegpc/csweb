const { post } = require('../xhr')
const { genGetSign } = require('../sign')
const { i18nReplace } = require('../i18n');
const { InputList } = require('../input_list');

window.addEventListener('load', () => {
    /**@type {HTMLInputElement}*/
    let keyinp = document.getElementById('pas');
    /**@type {HTMLInputElement} The button: Get proxy list*/
    let glb = document.getElementById('gl');
    /**@type {HTMLInputElement} The button: Add a new proxy*/
    let addb = document.getElementById('add');
    /**@type {HTMLDivElement}*/
    let addd = document.getElementById('addd');
    /**@type {HTMLInputElement} The button: Add a new proxy*/
    let caddb = document.getElementById('cadd');
    /**@type {HTMLInputElement}*/
    let id = document.getElementById('id');
    /**@type {HTMLDivElement}*/
    let cookie = document.getElementById('cok');
    /**@type {InputList}*/
    let input_cookies = undefined;
    /**@type {HTMLDivElement}*/
    let headers = document.getElementById('hea');
    /**@type {InputList}*/
    let input_headers = undefined;
    let show_add = false;
    let i18n = window['i18n'];
    /**@type {Array<string>}*/
    let data = [];
    /**
     * The callback when serect is changed
     * @param {string} str The new secret
     */
    function key_change_callback(str) {
        if (str.length) {
            glb.disabled = false;
            addb.disabled = false;
            caddb.disabled = false;
        } else {
            glb.disabled = true;
            addb.disabled = true;
            caddb.disabled = true;
        }
    }
    function get_time() {
        return (Math.floor(new Date().getTime() / 1000)).toString();
    }
    /**
     * Render proxy list
     * @param {number} page Page number
     */
    function render_proxy_list(page) {
        page = Math.floor(page);
    }
    function get_proxy_list() {
        let p = {'a': "list", 't': get_time()};
        p['sign'] = genGetSign(p, keyinp.value);
        post('/proxy/list', p, (data) => {
            let d = JSON.parse(data);
            let code = d['code'];
            if (code == -500) {
                console.warn('Server error: ', d['msg']);
                alert(i18n['SEVERR']);
            } else if (code == -401) {
                alert(i18n['UNAUTH']);
            } else if (code == 0) {
                data = d['result'];
                render_proxy_list(0);
            } else {
                alert(d['msg']);
            }
        })
    }
    keyinp.addEventListener('input', () => {
        key_change_callback(keyinp.value);
    })
    glb.addEventListener('click', () => {
        get_proxy_list();
    })
    addb.addEventListener('click', () => {
        if (show_add) {
            addd.style.display = 'none';
        } else {
            addd.style.display = null;
        }
        show_add = !show_add;
    })
    caddb.addEventListener('click', () => {
        if (!id.value.length) {
            alert(i18nReplace(i18n['REQ'], {'a': 'ID'}));
            return;
        } else if (input_cookies.isEmpty() && input_headers.isEmpty()) {
            alert(i18nReplace(i18n['REQ'], {'a': i18nReplace(i18n['OR'], {'a': 'Cookies', 'b': 'Headers'})}))
            return;
        }
        let p = {"a": "add", "t": get_time(), "id": id.value}
        if (!input_cookies.isEmpty()) {
            p['c'] = JSON.stringify(input_cookies.toObject());
        }
        if (!input_headers.isEmpty()) {
            p['h'] = JSON.stringify(input_headers.toObject());
        }
        p['sign'] = genGetSign(p, keyinp.value);
        post("/proxy/add", p, (data) => {
            let d = JSON.parse(data);
            let code = d['code'];
            if (code == -500) {
                console.warn('Server error: ', d['msg']);
                alert(i18n['SEVERR']);
            } else if (code == -401) {
                alert(i18n['UNAUTH']);
            } else if (code == 0) {
                get_proxy_list();
            } else {
                alert(d['msg']);
            }
        })
    })
    input_cookies = new InputList(cookie);
    input_headers = new InputList(headers);
})
