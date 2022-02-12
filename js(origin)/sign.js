const { SHA512 } = require('@stablelib/sha512');
const arrayBufferToHex = require('array-buffer-to-hex');
const { URLParams } = require('./url_params');

/**
 * Hash data
 * @param {string} data Data
 * @returns {string} hexdigest
 */
function sha512(data) {
    let enc = new TextEncoder();
    let arr = enc.encode(data);
    let h = new SHA512();
    h.update(arr)
    let re = h.digest();
    return arrayBufferToHex(re);
}

/**
 * Generate sign for data
 * @param {Object<string, string | Array<string>>|FormData} data Data
 * @param {string} secret Secret
 * @param {(data: string) => string|undefined} hash The hash function
 * @returns {string}
 */
function genGetSign(data, secret, hash) {
    if (!hash) hash = sha512;
    /**@type {Array<{k: string, v: string}>} */
    let arr = [];
    if (data.constructor.name == "FormData") {
        for (let pair of data.entries()) {
            if (typeof pair[1] != "string") continue;
            arr.push({ k: pair[0], v: pair[1] });
        }
    } else {
        Object.getOwnPropertyNames(data).forEach((key) => {
            let v = data[key];
            if (typeof v == "string") arr.push({ k: key, v: v });
            else if (Array.isArray(v)) {
                v.forEach((v) => {
                    if (typeof v == "string") arr.push({ k: key, v: v });
                })
            }
        })
    }
    arr.sort((a, b) => {
        return a.k == b.k ? a.v == b.v ? 0 : a.v > b.v ? 1 : -1 : a.k > b.k ? 1 : -1;
    })
    let par = new URLParams();
    arr.forEach((v) => {
        par.append(v.k, v.v);
    })
    return hash(secret + par.toString());
}

module.exports.genGetSign = genGetSign;
module.exports._sha512 = sha512;
