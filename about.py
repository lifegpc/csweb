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
from tep import getTemplate, addWikiLinkToText, embScr
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator
)
from settings import settings
from mycache import setCacheControl
from langlink import genLangLink


class About:
    def GET(self):
        te = getTemplate("about.html")
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('about', lan)
        trans = getTranslator(about=i18n)
        web.header('Content-Language', lan)
        if web.input().get('hl') is None:
            web.header('Vary', 'Accept-Language')
        s = settings()
        s.ReadSettings()
        if s.webpageCacheTime is not None:
            setCacheControl(s.webpageCacheTime)
        return te(lan, trans, i18n, addWikiLinkToText, embScr, genLangLink)


if m:
    application = web.application((".*", "About"), globals()).wsgifunc()
