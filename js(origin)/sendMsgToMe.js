window.addEventListener('load', () => {
    document.getElementById('submit').addEventListener('click', () => {
        var grecaptcha = window['grecaptcha'];
        var res = grecaptcha['getResponse']();
        if (res == "") return;
        /**@type {HTMLTextAreaElement} */
        var content = document.getElementById('content');
        if (content.value == "") return;
        post("/sendMsgToMe", {"g-recaptcha-response": res, "content": content.value}, (c) => {
            var c = JSON.parse(c);
            console.log(c);
        }, () => {
            console.error('F');
        })
    })
})
