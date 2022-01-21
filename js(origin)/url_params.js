/**
 * encodeURIComponent as python's quote_plus behavoir
 * @param {string} str 
 * @returns 
 */
function py_quote(str) {
    let s = encodeURIComponent(str);
    while (s.includes('%20')) {
        s = s.replace('%20', '+');
    }
    while (s.includes('!')) {
        s = s.replace('!', '%21');
    }
    while (s.includes("'")) {
        s = s.replace("'", '%27');
    }
    while (s.includes('(')) {
        s = s.replace('(', '%28');
    }
    while (s.includes(')')) {
        s = s.replace(')', '%29');
    }
    while (s.includes('*')) {
        s = s.replace('*', '%2A');
    }
    return s;
}

class URLParams extends URLSearchParams {
    toString() {
        let r = "";
        for (let p of this.entries()) {
            if (r.length) r += "&";
            r += py_quote(p[0]) + "=" + py_quote(p[1]);
        }
        return r;
    }
}

module.exports = { URLParams }
