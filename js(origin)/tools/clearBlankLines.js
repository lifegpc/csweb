window.addEventListener('load', () => {
    var ClipboardJS = window["ClipboardJS"];
    var clipboard = new ClipboardJS('#cp');
    clipboard["on"]('success', function (e) {
        e["clearSelection"]();
    });
    clipboard["on"]('error', function (e) {
        console.error('Action:', e["action"]);
        console.error('Trigger:', e["trigger"]);
    });
    /**@type {HTMLTextAreaElement}*/
    let inp = document.getElementById('inp');
    /**@type {HTMLTextAreaElement}*/
    let out = document.getElementById('o');
    /**@type {HTMLInputElement}*/
    let gen = document.getElementById('gen');
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
