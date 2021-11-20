Module.version = Module['cwrap']('version', 'string', []);

/**
 * @param {number} ptr The pointer to char*
 * @param {number} le string's length
 * @returns {string}
 */
function ptr2str(ptr, le) {
    let HEAP8 = Module['HEAP8'];
    let free = Module['_free'];
    let tmp = new Int8Array(le);
    tmp.set(HEAP8['subarray'](ptr, ptr + le));
    free(ptr);
    let d = new TextDecoder();
    return d.decode(tmp);
}

/**
 * @param {string} s string
 * @returns {number}
 */
function str2ptr(s) {
    let e = new TextEncoder();
    let ar = e.encode(s);
    /**@type {Uint8Array}*/
    let HEAPU8 = Module['HEAPU8'];
    let malloc = Module['_malloc'];
    let ptr = malloc(ar.length + 1);
    if (ptr == 0) return 0;
    HEAPU8.set(ar, ptr);
    HEAPU8[ptr + ar.length] = 0;
    return ptr;
}

Module.get_all_extensions = () => {
    let free = Module['_free'];
    let malloc = Module['_malloc'];
    let HEAP32 = Module["HEAP32"];
    let ptr = malloc(4);
    if (ptr == 0) {
        return null;
    }
    HEAP32[ptr / 4] = 0;
    let li = Module['_get_all_extensions']();
    if (li == 0) {
        free(ptr);
        return null;
    }
    let s = 0;
    let re = []
    do {
        s = Module['_get_next_extension_name'](li, ptr);
        if (s != 0) {
            re.push(ptr2str(s, HEAP32[ptr / 4]));
        }
    } while (s != 0);
    free(ptr);
    Module['_free_extension_list'](li);
    return re;
}

/**
 * @param {Uint8Array|string} inp
 * @param {Number} options
 * @param {Array<string>?} exts
 * @returns {string?}
 */
Module.md_to_html = (inp, options, exts) => {
    if (typeof inp == "string") {
        let e = new TextEncoder();
        inp = e.encode(inp);
    }
    let free_extension_list = Module['_free_extension_list'];
    let malloc = Module['_malloc'];
    let free = Module['_free'];
    let HEAPU8 = Module['HEAPU8'];
    let ex = 0
    if (exts && Array.isArray(exts)) {
        ex = Module['_new_extension_list']();
        if (ex == 0) {
            return null;
        }
        for (let i = 0; i < exts.length; i++) {
            let ptr = str2ptr(exts[i]);
            if (ptr == 0) {
                free_extension_list(ex);
                return null;
            }
            if (Module['_append_extension_to_list'](ex, ptr)) {
                free(ptr);
                free_extension_list(ex);
                return null;
            }
            free(ptr);
        }
    }
    let sptr = malloc(inp.length);
    if (sptr == 0) {
        if (ex != 0) free_extension_list(ex);
        return null;
    }
    HEAPU8.set(inp, sptr);
    let re = Module['_md_to_html'](sptr, inp.length, options, ex);
    if (ex != 0) {
        free_extension_list(ex);
    }
    free(sptr);
    if (re == 0) return null;
    let s = ptr2str(re, Module['_strlen'](re));
    return s;
}

Module.CMARK_OPT_DEFAULT = 0;
Module.CMARK_OPT_SOURCEPOS = 1 << 1;
Module.CMARK_OPT_HARDBREAKS = 1 << 2;
Module.CMARK_OPT_SAFE = 1 << 3;
Module.CMARK_OPT_UNSAFE = 1 << 17;
Module.CMARK_OPT_NOBREAKS = 1 << 4;
Module.CMARK_OPT_NORMALIZE = 1 << 8;
Module.CMARK_OPT_VALIDATE_UTF8 = 1 << 9;
Module.CMARK_OPT_SMART = 1 << 10;
Module.CMARK_OPT_GITHUB_PRE_LANG = 1 << 11;
Module.CMARK_OPT_LIBERAL_HTML_TAG = 1 << 12;
Module.CMARK_OPT_FOOTNOTES = 1 << 13;
Module.CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE = 1 << 14;
Module.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES = 1 << 15;
Module.CMARK_OPT_FULL_INFO_STRING = 1 << 16;

module.exports = Module;
