/**
 * 显示元素
 * @param {HTMLElement} e 网页元素
 * @param {string?} n 新display内容
 */
function showElement(e, n = null) {
    e.style.display = n;
}
/**
 * 隐藏元素
 * @param {HTMLElement} e 网页元素
 */
function hideElement(e) {
    e.style.display = "none";
}
