const { i18nReplace } = require('./i18n');

let i18n = window['i18n'];

/**
 * @param {File} file output_log.txt
 */
async function read_output_log(file) {
    let logText = await file.text();
    let gamePathMch = logText.match(/\w:\/.+(GenshinImpact_Data|YuanShen_Data)/);
    if (gamePathMch === null) {
        throw new Error(i18n['NO_GAME_DIR']);
    }
    return gamePathMch[0] + '/webCaches/Cache/Cache_Data/data_2';
}

/**
 * @param {File} file
 */
async function read_wish_url(file) {
    let cacheText = await file.text();
    const urlMch = cacheText.match(/https.+?game_biz=hk4e_\w+/g)
    if (urlMch) {
        return urlMch[urlMch.length - 1]
    } else {
        throw new Error(i18n['NO_WISH_URL']);
    }
}

window.addEventListener('load', () => {
    let analysis = document.getElementById('ana1');
    let analysis2 = document.getElementById('ana2');
    /**@type {HTMLInputElement}*/
    let file = document.getElementById('file');
    let label = document.getElementById('output');
    /**@type {HTMLInputElement}*/
    let output = document.getElementById('output2');
    analysis.addEventListener('click', () => {
        if (!file.files.length) {
            alert(i18n['NO_FILE_FOUND']);
            return;
        }
        let log_file = file.files[0];
        read_output_log(log_file).then((gamePath) => {
            label.innerText = i18nReplace(i18n['OUTPUT'], { 'FILE': gamePath });
        })
            .catch(e => {
                console.warn(e);
                /**@type {Error} */
                let err = e;
                alert(err.message);
            })
    })
    analysis2.addEventListener('click', () => {
        if (!file.files.length) {
            alert(i18n['NO_FILE_FOUND']);
            return;
        }
        let log_file = file.files[0];
        read_wish_url(log_file).then((url) => {
            output.value = url;
        }).catch(e => {
            console.warn(e);
            /**@type {Error} */
            let err = e;
            alert(err.message);
        })
    })
})
