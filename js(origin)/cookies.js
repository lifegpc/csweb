/**
 * Parse cookies string
 * @param {string} cookies The string of cookies. Such as `f=23; d=23`
 * @returns {Object<string, string> | undefined}
 */
function parseCookies(cookies) {
    let cs = cookies.split(';');
    let r = {};
    let iv = false;
    cs.forEach((c) => {
        if (iv) return;
        c = c.trim();
        let d = c.split('=');
        if (d.length == 1) {
            iv = true;
            return;
        }
        r[d[0]] = d.slice(1).join("=");
    })
    if (iv) return undefined;
    return r;
}

module.exports = { parseCookies }
