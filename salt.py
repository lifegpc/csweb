import web
from tep import getTemplate, embScr, addWikiLinkToText
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator,
    mapToDict,
    dictToJSON
)


class Salt:
    def GET(self):
        te = getTemplate("salt.html")
        if te is None:
            web.HTTPError('500')
            return 'Error'
        lan = getlang()
        i18n = getdict('salt', lan)
        trans = getTranslator(salt=i18n)
        i18n2 = {}
        mapToDict(i18n, i18n2, ["UKNHASH"])
        i18n2 = dictToJSON(i18n2)
        return te(lan, trans, i18n, embScr, addWikiLinkToText, i18n2)
