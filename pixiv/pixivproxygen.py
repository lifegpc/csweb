import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    f = abspath('.')
    sys.path.append(f)
    chdir(f + '/../')
    sys.path.append(abspath('.'))
    m = True
else:
    m = False
import web
from settings import settings
from mycache import setCacheControl
from langlink import genLangLink
from tep import getTemplate, embScr
from lang import (
    dictToJSON,
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator,
    mapToDict,
)


class PixivProxyGen:
    def GET(self):
        te = getTemplate("pixiv/pixivgen.html")
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('pixiv/pixivgen', lan)
        i18n2 = {}
        mapToDict(i18n, i18n2, ['ND'])
        trans = getTranslator(manage=i18n)
        web.header('Content-Language', lan)
        if web.input().get('hl') is None:
            web.header('Vary', 'Accept-Language')
        s = settings()
        s.ReadSettings()
        if s.webpageCacheTime is not None:
            setCacheControl(s.webpageCacheTime)
        return te(lan, trans, i18n, embScr, genLangLink, dictToJSON(i18n2))


if m:
    application = web.application((".*", "PixivProxyGen"), globals()).wsgifunc()  # noqa: E501
