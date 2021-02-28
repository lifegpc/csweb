/**
 * 发送POST请求
 * @param {string} url 网站
 * @param {FormData|Object<string, string>} data 字典
 * @param {(content: string)=>void} callback 回调函数
 * @param {()=>void} failedCallback 失败回调函数
 */
function post(url, data, callback, failedCallback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    if (callback != undefined) xhr.onloadend = () => {
        callback(xhr.responseText);
    };
    if (failedCallback != undefined) xhr.onerror = failedCallback;
    /**@type {FormData}*/
    var form = null;
    if (data.constructor.name == "Object") {
        form = new FormData();
        Object.getOwnPropertyNames(data).forEach((key) => {
            form.append(key, data[key]);
        })
    } else form = data;
    xhr.send(form);
}
