/**
 * 按map替换内容
 * @param {string} value 
 * @param {Object.<string, string>} map 
 */
function i18nReplace(value, map) {
    Object.getOwnPropertyNames(map).forEach((key) => {
        var keyt = "<" + key + ">";
        while (value.includes(keyt)) {
            value = value.replace(keyt, map[key]);
        }
    })
    return value;
}
module.exports = { i18nReplace };
