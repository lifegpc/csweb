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
    /**@type {HTMLInputElement} Button: First page*/
    let fp = document.getElementById('fp');
    /**@type {HTMLInputElement} Button: Previous page*/
    let pp = document.getElementById('pp');
    /**@type {HTMLInputElement} Button: Next page*/
    let np = document.getElementById('np');
    /**@type {HTMLInputElement} Button: Last page*/
    let lp = document.getElementById('lp');
    /**@type {HTMLDivElement} Page <num>, <total> in total.*/
    let pn = document.getElementById('pn');
    let page_now = 0;
    /**@type {Array<{c: InputList, h: InputList}}*/
    let inputs_list = [];
    /**@type {HTMLTableSectionElement}*/
    let listd = document.getElementById('list');
    /**@type {HTMLTemplateElement}*/
    let listt = document.getElementById('listt');
    /**@type {Object<string, {cookies: Object<string, string>, headers: Object<string, string>}>}*/
    let datas = {};
    /**@type {HTMLInputElement} Button: Delete all proxies*/
    let dab = document.getElementById('da');
    /**
     * The callback when serect is changed
     * @param {string} str The new secret
     */
    function key_change_callback(str) {
        if (str.length) {
            glb.disabled = false;
            addb.disabled = false;
            caddb.disabled = false;
            dab.disabled = false;
        } else {
            glb.disabled = true;
            addb.disabled = true;
            caddb.disabled = true;
            dab.disabled = true;
        }
    }
    function get_time() {
        return (Math.floor(new Date().getTime() / 1000)).toString();
    }
    /**
     * Render proxy
     * @param {string} id The ID of proxy
     */
    function render_proxy(id) {
        /**@type {HTMLInputElement}*/
        let t = listt.content.firstElementChild.cloneNode(true);
        /**@type {HTMLTableCellElement}*/
        let ide = t.querySelector('.id');
        ide.innerText = id;
        let d = { c: undefined, h: undefined };
        /**@type {HTMLInputElement}*/
        let sc = t.querySelector('.sc');
        let cookies = t.querySelector('.cookies');
        /**@type {HTMLInputElement}*/
        let sh = t.querySelector('.sh');
        let headers = t.querySelector('.headers');
        let del = t.querySelector('.del');
        /**
         * @param {Element} source
         * @param {HTMLInputElement} button Button
         * @param {Object<string, string>} data Data
         * @returns {InputList}
        */
        function create_list(source, button, data) {
            let tmp = new InputList(source, undefined, undefined, data, false);
            button.style.display = 'none';
            return tmp;
        }
        /**
         * @param {()=>void} callback 
         */
        function get_data(callback) {
            let p = { "a": "get", "t": get_time(), "id": id };
            p['sign'] = genGetSign(p, keyinp.value);
            post('/proxy/get', p, (da) => {
                let d = JSON.parse(da);
                let code = d['code'];
                if (code == -500) {
                    console.warn('Server error: ', d['msg']);
                    alert(i18n['SEVERR']);
                } else if (code == -401) {
                    alert(i18n['UNAUTH']);
                } else if (code == 0) {
                    datas[id] = {};
                    datas[id].cookies = JSON.parse(d['result']['cookies'] || "{}");
                    datas[id].headers = JSON.parse(d['result']['headers'] || "{}");
                    callback();
                } else {
                    alert(d['msg']);
                    if (code == -5) {
                        get_proxy_list();
                    }
                }
            })
        }
        sc.addEventListener('click', () => {
            if (!d.c) {
                if (datas.hasOwnProperty(id)) {
                    d.c = create_list(cookies, sc, datas[id].cookies);
                } else {
                    get_data(() => {
                        d.c = create_list(cookies, sc, datas[id].cookies);
                    })
                }
            }
        })
        sh.addEventListener('click', () => {
            if (!d.h) {
                if (datas.hasOwnProperty(id)) {
                    d.h = create_list(headers, sh, datas[id].headers);
                } else {
                    get_data(() => {
                        d.h = create_list(headers, sh, datas[id].headers);
                    })
                }
            }
        })
        del.addEventListener('click', () => {
            if (!confirm(i18n['CODEL'] + '\n' + i18n['UNDOW'])) return;
            let p = { "a": "delete", "t": get_time(), "id": id };
            p['sign'] = genGetSign(p, keyinp.value);
            post("/proxy/delete", p, (da) => {
                let d = JSON.parse(da);
                let code = d['code'];
                if (code == -500) {
                    console.warn('Server error: ', d['msg']);
                    alert(i18n['SEVERR']);
                } else if (code == -401) {
                    alert(i18n['UNAUTH']);
                } else if (code == 0) {
                    if (d['result']) {
                        alert(i18n['SUCDEL']);
                        get_proxy_list();
                    } else {
                        alert(i18n['FADEL']);
                    }
                } else {
                    alert(d['msg']);
                }
            })
        })
        inputs_list.push(d);
        listd.append(t);
    }
    /**
     * Render proxy list
     * @param {number} page Page number
     */
    function render_proxy_list(page) {
        page = Math.floor(page);
        let total_page = Math.ceil(data.length / 10);
        if (inputs_list.length) {
            inputs_list.forEach((d) => {
                if (d.c) d.c.destory();
                if (d.h) d.h.destory();
            })
            inputs_list = [];
        }
        if (total_page <= 0) {
            pn.innerText = i18nReplace(i18n['PN'], { "num": 0, "total": 0 });
            fp.disabled = true;
            pp.disabled = true;
            np.disabled = true;
            lp.disabled = true;
            listd.innerHTML = '';
            return;
        }
        if (page <= 0) page = 1;
        if (page > total_page) page = total_page;
        pn.innerText = i18nReplace(i18n['PN'], { "num": page, "total": total_page });
        if (page != 1) {
            fp.disabled = false;
            pp.disabled = false;
        } else {
            fp.disabled = true;
            pp.disabled = true;
        }
        if (page != total_page) {
            lp.disabled = false;
            np.disabled = false;
        } else {
            lp.disabled = true;
            np.disabled = true;
        }
        listd.innerHTML = '';
        page_now = page;
        let data_list = data.slice((page - 1) * 10, Math.min(page * 10, data.length));
        data_list.forEach((d) => {
            render_proxy(d);
        })
    }
    function get_proxy_list() {
        let p = { 'a': "list", 't': get_time() };
        p['sign'] = genGetSign(p, keyinp.value);
        post('/proxy/list', p, (da) => {
            let d = JSON.parse(da);
            let code = d['code'];
            if (code == -500) {
                console.warn('Server error: ', d['msg']);
                alert(i18n['SEVERR']);
            } else if (code == -401) {
                alert(i18n['UNAUTH']);
            } else if (code == 0) {
                data = d['result'];
                datas = {};
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
            alert(i18nReplace(i18n['REQ'], { 'a': 'ID' }));
            return;
        } else if (input_cookies.isEmpty() && input_headers.isEmpty()) {
            alert(i18nReplace(i18n['REQ'], { 'a': i18nReplace(i18n['OR'], { 'a': 'Cookies', 'b': 'Headers' }) }))
            return;
        }
        let p = { "a": "exists", "t": get_time(), "id": id.value }
        p['sign'] = genGetSign(p, keyinp.value);
        post("/proxy/exists", p, (da) => {
            let d = JSON.parse(da);
            let code = d['code'];
            if (code == -500) {
                console.warn('Server error: ', d['msg']);
                alert(i18n['SEVERR']);
            } else if (code == -401) {
                alert(i18n['UNAUTH']);
            } else if (code == 0) {
                if (d['result']) {
                    if (!confirm(i18n['COADD'] + '\n' + i18n['UNDOW'])) return;
                }
                let p = { "a": "add", "t": get_time(), "id": id.value }
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
                        alert(i18n['SUCADD']);
                        get_proxy_list();
                    } else {
                        alert(d['msg']);
                    }
                })
            } else {
                alert(d['msg']);
            }
        })
    })
    fp.addEventListener('click', () => {
        render_proxy_list(1);
    })
    pp.addEventListener('click', () => {
        render_proxy_list(page_now - 1);
    })
    np.addEventListener('click', () => {
        render_proxy_list(page_now + 1);
    })
    lp.addEventListener('click', () => {
        let pc = Math.ceil(data.length / 10);
        render_proxy_list(pc);
    })
    dab.addEventListener('click', () => {
        if (!confirm(i18n['CODEA'] + '\n' + i18n['UNDOW'])) return;
        let p = { "a": "deleteAll", "t": get_time() };
        p['sign'] = genGetSign(p, keyinp.value);
        post("/proxy/deleteAll", p, (da) => {
            let d = JSON.parse(da);
            let code = d['code'];
            if (code == -500) {
                console.warn('Server error: ', d['msg']);
                alert(i18n['SEVERR']);
            } else if (code == -401) {
                alert(i18n['UNAUTH']);
            } else if (code == 0) {
                if (d['result']) {
                    alert(i18n['SUCDEL']);
                    get_proxy_list();
                } else {
                    alert(i18n['FADEL']);
                }
            } else {
                alert(d['msg']);
            }
        })
    })
    input_cookies = new InputList(cookie);
    input_headers = new InputList(headers);
})
