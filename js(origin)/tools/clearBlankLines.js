const { copyToClipboard } = require("../clipboard");

window.addEventListener('load', () => {
    let cp = document.getElementById('cp');
    /**@type {HTMLTextAreaElement}*/
    let inp = document.getElementById('inp');
    /**@type {HTMLTextAreaElement}*/
    let out = document.getElementById('o');
    /**@type {HTMLInputElement}*/
    let gen = document.getElementById('gen');
    cp.addEventListener('click', () => {
        copyToClipboard(out, out.value);
    })
    gen.addEventListener('click', () => {
        let inpt = inp.value;
        if (!inpt.length) return;
        let re = inpt.split('\n');
        /**@type {Array<string>}*/
        let r = [];
        re.forEach((i) => {
            if (i.length) {
                r.push(i);
            }
        })
        out.value = r.join('\n');
    })
});
