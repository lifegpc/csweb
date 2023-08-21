function detect_darkmode() {
    return window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/**
 * @param {(e: MediaQueryListEvent) => void} e
 */
function addDarkModeListener(e) {
    return window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").addEventListener(
            "change",
            e,
        );
}

function basic_handle_darkmode() {
    if (detect_darkmode()) document.body.classList.add("dark-scheme");
    addDarkModeListener(e => {
        if (e.matches) document.body.classList.add("dark-scheme");
        else document.body.classList.remove("dark-scheme");
    })
}

module.exports = { detect_darkmode, addDarkModeListener, basic_handle_darkmode }
