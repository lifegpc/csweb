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
from tep import getTemplate, embScr
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    getTranslator
)
from settings import settings
from mycache import setCacheControl


class ClearBlankLines:
    def GET(self):
        te = getTemplate("tools/clearBlankLines.html")
        if te is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('tools/clearBlankLines', lan)
        trans = getTranslator(clearBlankLines=i18n)
        web.header('Content-Language', lan)
        if web.input().get('hl') is None:
            web.header('Vary', 'Accept-Language')
        s = settings()
        s.ReadSettings()
        if s.webpageCacheTime is not None:
            setCacheControl(s.webpageCacheTime)
        return te(lan, i18n, trans, embScr)


if m:
    application = web.application((".*",
                                   "ClearBlankLines"), globals()).wsgifunc()
