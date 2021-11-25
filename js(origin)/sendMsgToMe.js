/// <reference path="xhr.js" />
const { i18nReplace } = require('./i18n')
window.addEventListener('load', () => {
    document.getElementById('submit').addEventListener('click', () => {
        /**@type {HTMLTextAreaElement} */
        var content = document.getElementById('content');
        var i18n = window['i18n'];
        if (content.value == "") {
            alert(i18n['NEEDCON'])
            return;
        }
        /**@type {HTMLInputElement}*/
        var name = document.getElementById('name');
        if (name.value == "") {
            alert(i18n['NEEDN'])
            return;
        }
        var grecaptcha = window['grecaptcha'];
        var res = grecaptcha['getResponse']();
        if (res == "") {
            alert(i18n['RECAP2']);
            return;
        }
        /**@type {string|undefined}*/
        var lan = window['lan'];
        if (lan == undefined) lan = 'en';
        post("/sendMsgToMe", { "g-recaptcha-response": res, "content": content.value, "name": name.value, "lan": lan }, (c) => {
            var c = JSON.parse(c);
            console.log(c);
            if (c['code'] == 0) {
                alert(i18n['OK']);
                grecaptcha['reset']();
                content.value = '';
            } else {
                /**@type {string}*/
                var msg = c.hasOwnProperty("msg") ? c['msg'] : JSON.stringify(c);
                alert(i18nReplace(i18n['FAILED'], { 'info': msg }));
                grecaptcha['reset']();
            }
        }, () => {
            alert(i18nReplace(i18n['FAILED'], { 'info': i18n['NETERR'] }));
            grecaptcha['reset']();
        })
    })
})
