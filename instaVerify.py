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


class InstaVerify:
    def GET(self):
        from tep import getTemplate, embScr
        t = getTemplate("instaVerify.html")
        return t(embScr)

    def POST(self):
        from constants import jsonsep
        from json import dumps
        from settings import settings
        from traceback import format_exc
        from instaDatabase import InstaDatabase
        from instaAPI import InstaAPI, VerifyComplete
        web.header("Content-Type", "application/json; charset=UTF-8")
        try:
            sign = web.input().get("sign")
            if sign is None or not isinstance(sign, str) or len(sign) == 0:
                d = {"code": -1, "msg": "sign is needed."}
                return dumps(d, ensure_ascii=False, separators=jsonsep)
            code = web.input().get("code")
            if code is None or not isinstance(code, str) or len(code) == 0:
                d = {"code": -2, "msg": "code is needed."}
                return dumps(d, ensure_ascii=False, separators=jsonsep)
            db = InstaDatabase()
            InstaAPI(db, None, None, code, sign)
            d = {"code": -3, "msg": "Unknown Error."}
        except VerifyComplete:
            d = {"code": 0, "msg": "Verify Complete."}
        except:
            web.HTTPError('500 Internal Server Error')
            d = {"code": -500, "msg": "Internal Server Error"}
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    d["detail"] = format_exc()
            except:
                pass
        return dumps(d, ensure_ascii=False, separators=jsonsep)


if m:
    application = web.application((".*", "InstaVerify"), globals()).wsgifunc()
