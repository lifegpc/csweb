/// <reference path="xhr.js" />
/// <reference path="i18n.js" />
window.addEventListener('load', () => {
    document.getElementById('submit').addEventListener('click', () => {
        /**@type {HTMLTextAreaElement} */
        var content = document.getElementById('content');
        var i18n = window['i18n'];
        if (content.value == "") {
            alert(i18n['NEEDCON'])
            return;
        }
        var grecaptcha = window['grecaptcha'];
        var res = grecaptcha['getResponse']();
        if (res == "") return;
        post("/sendMsgToMe", { "g-recaptcha-response": res, "content": content.value }, (c) => {
            var c = JSON.parse(c);
            console.log(c);
            if (c['code'] == 0) {
                alert(i18n['OK']);
                grecaptcha['reset']();
                content.value = '';
            } else {
                /**@type {string}*/
                var msg = c.hasOwnProperty("msg") ? c['msg'] : JSON.stringify(c);
                alert(i18nReplace(i18n['FAILED'], {'info': msg}));
                grecaptcha['reset']();
            }
        }, () => {
            alert(i18nReplace(i18n['FAILED'], {'info': i18n['NETERR']}));
            grecaptcha['reset']();
        })
    })
})
