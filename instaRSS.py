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
from settings import settings


class InstaRSS:
    def GET(self):
        web.header("Content-Type", "application/json; charset=UTF-8")
        try:
            s = settings()
            s.ReadSettings()
        except:
            pass


if m:
    application = web.application((".*", "InstaRSS"), globals()).wsgifunc()
