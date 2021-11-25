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
function copyToClipboard(e) {
    if (!changeSelection(e)) return false;
    let re = document.execCommand('copy');
    changeSelection();
    return re;
}

module.exports = { copyToClipboard }
