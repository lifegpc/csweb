import sys
from os.path import abspath, dirname
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath('.'))
    m = True
else:
    m = False
import web
from tep import getTemplate, embScr
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator,
    mapToDict,
    dictToJSON
)
from mycache import setCacheControl
from settings import settings
from langlink import genLangLink


class GenshinExportWishUrl:
    def GET(self):
        te = getTemplate('genshinExportWishUrl.html')
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('genshinExportWishUrl', lan)
        trans = getTranslator(genshinExportWishUrl=i18n)
        i18n2 = {}
        mapToDict(i18n, i18n2, ['NO_FILE_FOUND',
                                'NO_GAME_DIR', 'OUTPUT', 'NO_WISH_URL'])
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
        return te(lan, trans, i18n, embScr, genLangLink, i18n2)


if m:
    application = web.application((".*", "GenshinExportWishUrl"), globals()).wsgifunc()  # noqa: E501
