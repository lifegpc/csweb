/**
 * Change selection to specify node.
 * @param {Node=} e 
 * @returns {boolean} true if successed.
 */
function changeSelection(e) {
    let se = window.getSelection();
    if (!se) return false;
    se.removeAllRanges();
    if (!e) return true;
    let r = document.createRange();
    r.selectNode(e);
    se.addRange(r);
    return true;
}

/**
 * Copy a node's data to clipboard
 * @param {Node} e 
 * @returns {boolean} true if successed.
 */
function copyToClipboardOld(e) {
    if (!changeSelection(e)) return false;
    let re = document.execCommand('copy');
    changeSelection();
    return re;
}

/**
 * Set clipboard's data to a node
 * @param {Node} e
 * @returns {boolean} true if successed.
 */
function readFromClipboardOld(e) {
    if (!changeSelection(e)) return false;
    let re = document.execCommand('paste');
    changeSelection();
    return re;
}

/**
 * Copy data to clipboard
 * @param {Node} e Target node (used to select)
 * @param {string} v Text (used in new api)
 * @returns {Promise<boolean>} true if successed.
 */
function copyToClipboard(e, v) {
    return new Promise((resolve, reject) => {
        if (!!navigator.clipboard) {
            navigator.clipboard.writeText(v).then(() => {
                resolve(true);
            }).catch((r) => {
                console.warn(r);
                resolve(copyToClipboardOld(e));
            })
        } else {
            resolve(copyToClipboardOld(e));
        }
    })
}


/**
 * Read data from clipboard
 * @param {HTMLInputElement|HTMLTextAreaElement} e Target note
 * @returns {Promise<boolean>} true if successed.
 */
function readFromClipboard(e) {
    return new Promise((resolve, reject) => {
        if (!!navigator.clipboard) {
            navigator.clipboard.readText().then((s) => {
                e.value = s;
                resolve(true);
            }).catch((r) => {
                console.warn(r);
                resolve(readFromClipboardOld(e));
            })
        } else {
            resolve(readFromClipboardOld(e));
        }
    })
}

module.exports = { copyToClipboard, readFromClipboard }
