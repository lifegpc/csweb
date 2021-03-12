/// <reference path="xhr.js"/>
window.addEventListener('load', () => {
    /**@type {HTMLCollectionOf<HTMLLinkElement>} */
    var list = document.getElementsByClassName('wplink');
    /**@type {Array<HTMLLinkElement>} */
    var li = [];
    for (var i = 0; i < list.length; i++) li.push(list[i]);
    li.forEach((ele) => {
        var item = ele.getAttribute('item');
        var qid = ele.getAttribute('qid');
        if (item == null || qid == null) return;
        var matched = item.match(/([A-Za-z]{2}):/)
        var lan = matched != null ? matched[1] : 'en';
        if (matched != null) item = item.substr(3, item.length - 3);
        ele.href = 'https://' + lan + ".wikipedia.org/wiki/" + item;
        /**@type {string}*/
        var winlan = window['lan'];
        try {
            get("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&origin=*", { "ids": qid }, (c) => {
                var con = JSON.parse(c);
                if (con['success']) {
                    if (con['entities'][qid]['type'] == 'item') {
                        var sitelinks = con['entities'][qid]['sitelinks'];
                        if (sitelinks) {
                            var t = winlan.substr(0, 2)
                            var name = ''
                            if (sitelinks[t + "wiki"]) name = sitelinks[t + "wiki"]['title']
                            else if (sitelinks["enwiki"]) {
                                t = 'en';
                                name = sitelinks["enwiki"]['title'];
                            }
                            else {
                                var keyli = Object.getOwnPropertyNames(sitelinks);
                                if (keyli.length && sitelinks[keyli[0]]) {
                                    t = keyli[0].substr(0, 2);
                                    name = sitelinks[keyli[0]]['title'];
                                }
                            }
                            if (t.length && name.length) {
                                ele.href = 'https://' + t + ".wikipedia.org/wiki/" + name;
                            }
                        }
                    }
                }
            })
        } catch (e) {
            console.warn(e);
        }
    })
})
