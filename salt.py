import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
    m = True
else:
    m = False
import web
from tep import getTemplate, embScr, addWikiLinkToText
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator,
    mapToDict,
    dictToJSON
)
from ie import isIE
from mycache import setCacheControl
from settings import settings
from langlink import genLangLink


class Salt:
    def GET(self):
        te = getTemplate("salt.html")
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('salt', lan)
        trans = getTranslator(salt=i18n)
        i18n2 = {}
        mapToDict(i18n, i18n2, ["UKNHASH"])
        i18n2 = dictToJSON(i18n2)
        s = settings()
        s.ReadSettings()
        web.header('Content-Language', lan)
        vary = 'User-Agent'
        if web.input().get('hl') is None:
            vary += ',Accept-Language'
        web.header('Vary', vary)
        if s.webpageCacheTime is not None:
            setCacheControl(s.webpageCacheTime)
        return te(lan, trans, i18n, embScr, addWikiLinkToText, i18n2, isIE,
                  genLangLink)


if m:
    application = web.application((".*", "Salt"), globals()).wsgifunc()
