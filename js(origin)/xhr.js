/**
 * 发送POST请求
 * @param {string} url 网站
 * @param {FormData|Object<string, string>} data 字典
 * @param {(content: string)=>void} callback 回调函数
 * @param {()=>void} failedCallback 失败回调函数
 *  * @param {Object<string, string>} headers HTTP头部
 */
function post(url, data, callback, failedCallback, headers) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    if (callback != undefined) xhr.onload = () => {
        callback(xhr.responseText);
    };
    if (failedCallback != undefined) xhr.onerror = failedCallback;
    /**@type {FormData}*/
    var form = null;
    if (data == undefined);
    else if (data.constructor.name == "Object") {
        form = new FormData();
        Object.getOwnPropertyNames(data).forEach((key) => {
            form.append(key, data[key]);
        })
    } else form = data;
    var u = new URL(window.location.href);
    var hl = u.searchParams.get('hl');
    if (hl != null && !form.has("hl") && u.hostname == new URL(url).hostname) form.append("hl", hl);
    if (headers != undefined) {
        Object.getOwnPropertyNames(headers).forEach((key) => {
            if (typeof headers[key] == "string")
                xhr.setRequestHeader(key, headers[key])
        })
    }
    try {
        form != null ? xhr.send(form) : xhr.send();
    } catch (e) {
        if (failedCallback != undefined) failedCallback();
    }
}
/**
 * 发送GET请求
 * @param {string} url 网站
 * @param {Object<string, string>|Array<Array<string>|string>} data 字典
 * @param {(content: string)=>void} callback 回调函数
 * @param {()=>void} failedCallback 失败回调函数
 * @param {Object<string, string>} headers HTTP头部
 */
function get(url, data, callback, failedCallback, headers) {
    var xhr = new XMLHttpRequest();
    var uri = new URL(url, window.location.href);
    if (data == undefined);
    else if (Array.isArray(data)) {
        for (let i = 0; i < data.length; i++) {
            var pair = data[i];
            if (Array.isArray(pair)) {
                uri.searchParams.append(pair[0], pair.length > 1 ? pair[1] : "");
            } else if (typeof pair == "string") {
                uri.searchParams.append(pair, "");
            }
        }
    } else {
        Object.getOwnPropertyNames(data).forEach((key) => {
            if (typeof data[key] == "string")
                uri.searchParams.append(key, data[key]);
        })
    }
    var hl = uri.searchParams.get('hl');
    var louri = new URL(window.location.href);
    var hl2 = louri.searchParams.get('hl');
    if (hl == null && hl2 != null && uri.hostname == louri.hostname) {
        uri.searchParams.append('hl', hl2);
    }
    xhr.open("GET", uri.href);
    if (callback != undefined) xhr.onload = () => {
        callback(xhr.responseText);
    };
    if (failedCallback != undefined) xhr.onerror = failedCallback;
    if (headers != undefined) {
        Object.getOwnPropertyNames(headers).forEach((key) => {
            if (typeof headers[key] == "string")
                xhr.setRequestHeader(key, headers[key])
        })
    }
    try {
        xhr.send();
    } catch (e) {
        if (failedCallback != undefined) failedCallback();
    }
}
