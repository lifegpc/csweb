function OnloadRecaptcha() {
    var grecaptcha = window['grecaptcha'];
    var render = grecaptcha['render'];
    render("captcha2", {
        "sitekey": document.getElementById("captcha2").getAttribute("sitekey")
    })
}
window['OnloadRecaptcha'] = OnloadRecaptcha;
