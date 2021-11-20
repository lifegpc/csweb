const _cmark_gfm = require('../_cmark_gfm')
let m_loaded = false;
let cmark_gfm_loaded = false;
function main() {
    let d = document.getElementById('ver');
    d.innerText = _cmark_gfm.version();
}
_cmark_gfm['onRuntimeInitialized'] = () => {
    cmark_gfm_loaded = true;
    if (m_loaded) main();
}
window.addEventListener('load', () => {
    m_loaded = true;
    if (cmark_gfm_loaded) main();
})
