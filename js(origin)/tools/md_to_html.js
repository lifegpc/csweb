const { copyToClipboard, readFromClipboard } = require('../clipboard');
const { showElement, hideElement, addBrToElement } = require('../element');
const _cmark_gfm = require('../_cmark_gfm')

let m_loaded = false;
let cmark_gfm_loaded = false;

/**
 * Handle options
 * @param {HTMLInputElement} e Input element
 * @param {number} opt The option which input element effect
 * @param {number} opts Original options
 * @returns {number} Result options
 */
function handleopts(e, opt, opts) {
    if (e.checked) {
        return opts | opt;
    } else {
        return opts & opt ? opts - opt : opts;
    }
}

function main() {
    let i18n = window['i18n'];
    let d = document.getElementById('ver');
    d.innerText = _cmark_gfm.version();
    /**@type {HTMLInputElement}*/
    let optb = document.getElementById('optb');
    let optd = document.getElementById('optd');
    /**@type {HTMLInputElement}*/
    let opt1 = document.getElementById('opt1');
    let opt2 = document.getElementById('opt2');
    let opt3 = document.getElementById('opt3');
    let opt4 = document.getElementById('opt4');
    let opt5 = document.getElementById('opt5');
    let opt6 = document.getElementById('opt6');
    let opt7 = document.getElementById('opt7');
    let opt8 = document.getElementById('opt8');
    let opt9 = document.getElementById('opt9');
    let opt10 = document.getElementById('opt10');
    let opt11 = document.getElementById('opt11');
    let opt12 = document.getElementById('opt12');
    /**@type {HTMLInputElement}*/
    let extb = document.getElementById('extb');
    let extd = document.getElementById('extd');
    /**@type {HTMLInputElement}*/
    let it = document.getElementById('it');
    /**@type {HTMLTextAreaElement}*/
    let itxt = document.getElementById('itxt');
    /**@type {HTMLInputElement}*/
    let inf = document.getElementById('inf');
    /**@type {HTMLTextAreaElement}*/
    let otxt = document.getElementById('otxt');
    let con = document.getElementById('con');
    let ocp = document.getElementById('ocp');
    let ird = document.getElementById('ird');
    let showopt = false;
    let showext = false;
    let use_file = false;
    let opts = 0;
    /**@type {Array<HTMLInputElement>}*/
    let extds = [];
    optb.addEventListener('click', () => {
        showopt = !showopt;
        if (showopt) {
            optb.value = i18n['HOPTIONS'];
            showElement(optd);
        }
        else {
            optb.value = i18n['SOPTIONS'];
            hideElement(optd);
        }
    })
    extb.addEventListener('click', () => {
        showext = !showext;
        if (showext) {
            extb.value = i18n['HEXT'];
            showElement(extd);
        } else {
            extb.value = i18n['SEXT'];
            hideElement(extd);
        }
    })
    opt1.addEventListener('input', () => {
        opts = handleopts(opt1, _cmark_gfm.CMARK_OPT_SOURCEPOS, opts);
        console.log(opts);
    })
    opt2.addEventListener('input', () => {
        opts = handleopts(opt2, _cmark_gfm.CMARK_OPT_HARDBREAKS, opts);
        console.log(opts);
    })
    opt3.addEventListener('input', () => {
        opts = handleopts(opt3, _cmark_gfm.CMARK_OPT_UNSAFE, opts);
        console.log(opts);
    })
    opt4.addEventListener('input', () => {
        opts = handleopts(opt4, _cmark_gfm.CMARK_OPT_NOBREAKS, opts);
        console.log(opts);
    })
    opt5.addEventListener('input', () => {
        opts = handleopts(opt5, _cmark_gfm.CMARK_OPT_VALIDATE_UTF8, opts);
        console.log(opts);
    })
    opt6.addEventListener('input', () => {
        opts = handleopts(opt6, _cmark_gfm.CMARK_OPT_SMART, opts);
        console.log(opts);
    })
    opt7.addEventListener('input', () => {
        opts = handleopts(opt7, _cmark_gfm.CMARK_OPT_GITHUB_PRE_LANG, opts);
        console.log(opts);
    })
    opt8.addEventListener('input', () => {
        opts = handleopts(opt8, _cmark_gfm.CMARK_OPT_LIBERAL_HTML_TAG, opts);
        console.log(opts);
    })
    opt9.addEventListener('input', () => {
        opts = handleopts(opt9, _cmark_gfm.CMARK_OPT_FOOTNOTES, opts);
        console.log(opts);
    })
    opt10.addEventListener('input', () => {
        opts = handleopts(opt10, _cmark_gfm.CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE, opts);
        console.log(opts);
    })
    opt11.addEventListener('input', () => {
        opts = handleopts(opt11, _cmark_gfm.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES, opts);
        console.log(opts);
    })
    opt12.addEventListener('input', () => {
        opts = handleopts(opt12, _cmark_gfm.CMARK_OPT_FULL_INFO_STRING, opts);
        console.log(opts);
    })
    let ext_list = _cmark_gfm.get_all_extensions();
    for (let i = 0; i < ext_list.length; i++) {
        let ext_name = ext_list[i];
        let bu = document.createElement('input');
        bu.type = 'checkbox';
        bu.id = 'ext_' + ext_name;
        extd.append(bu);
        extds.push(bu);
        let lab = document.createElement('label');
        lab.innerText = ext_name;
        lab.htmlFor = bu.id;
        extd.append(lab);
        addBrToElement(extd);
    }
    function change_to_use_file() {
        it.value = i18n['UT'];
        hideElement(itxt);
        hideElement(ird);
        showElement(inf);
    }
    function change_to_use_textbox() {
        it.value = i18n['UF'];
        hideElement(inf);
        showElement(itxt);
        showElement(ird);
    }
    it.addEventListener('click', () => {
        use_file = !use_file;
        if (use_file) {
            change_to_use_file()
        } else {
            change_to_use_textbox()
        }
    })
    function realConvert(s) {
        let exts = [];
        for (let i = 0; i < extds.length; i++) {
            if (extds[i].checked) exts.push(ext_list[i]);
        }
        let re = _cmark_gfm.md_to_html(s, opts, exts);
        return typeof re == "string" ? re : "";
    }
    function convert(s) {
        otxt.value = realConvert(s);
    }
    con.addEventListener('click', () => {
        if (use_file) {
            if (inf.files.length) {
                inf.files[0].text().then((s) => {
                    convert(s);
                })
            }
        } else {
            convert(itxt.value);
        }
    })
    ocp.addEventListener('click', () => {
        copyToClipboard(otxt, otxt.value);
    })
    ird.addEventListener('click', () => {
        readFromClipboard(itxt).then((r) => {
            if (!r) itxt.value = "";
        })
    })
}

_cmark_gfm['onRuntimeInitialized'] = () => {
    cmark_gfm_loaded = true;
    if (m_loaded) main();
}

window.addEventListener('load', () => {
    m_loaded = true;
    if (cmark_gfm_loaded) main();
})
