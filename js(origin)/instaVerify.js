const { post } = require('./xhr');
window.addEventListener('load', () => {
    /**@type {HTMLInputElement}*/
    let s = document.getElementById('s');
    /**@type {HTMLInputElement}*/
    let verify = document.getElementById('verify');
    let url = new URL(window.location.href);
    let sign = url.searchParams.get("nc")
    let gourl = url.searchParams.get("gourl");
    if (sign == null) window.location.href = '/';
    if (gourl == null) gourl = '/';
    s.addEventListener('click', () => {
        if (verify.validationMessage != '') {
            alert(verify.validationMessage);
            return;
        }
        let code = verify.value;
        post("/instaVerify", {"sign": sign, "code": code}, (s) => {
            let r = JSON.parse(s);
            if (r['code'] == 0) {
                window.location.href = gourl;
            } else {
                console.warn(r);
                alert(r["code"] + " " + r["msg"]);
            }
        })
    })
})
