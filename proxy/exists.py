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
from json import dumps
from traceback import format_exc
from time import time
from db import ProxyDb
sys.path.append(abspath("../"))
from settings import settings  # noqa: E402
from constants import jsonsep  # noqa: E402
from sign import verifySign  # noqa: E402


class ProxyExists:
    def __init__(self):
        self._method = None

    def GET(self):
        self._method = 'GET'
        return self.POST()

    def POST(self):
        if self._method is None:
            self._method = 'POST'
        web.header("Content-Type", "application/json; charset=utf-8")
        try:
            callback = None
            if self._method == 'GET':
                callback = web.input().get("callback")
                if callback is not None and callback != '':
                    web.header("Content-Type",
                               "application/javascript; charset=utf-8")
                else:
                    callback = None
            cors = web.input().get("cors")
            if cors is not None:
                web.header('Access-Control-Allow-Origin', '*')
            s = settings()
            s.ReadSettings()
            sg = s.proxyAPISecrets
            if sg is None:
                d = dumps({"code": -500, "msg":
                           "proxyAPISecrets must be set in settings."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            if not verifySign(sg):
                d = dumps({"code": -401, "msg": "Unauthorized"},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            t = web.input().get("t")
            if t is None:
                d = dumps({"code": -1, "msg": "current time(t) is needed."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            try:
                t = int(t)
            except:
                d = dumps({"code": -2, "msg":
                           "current time(t) must be a integer."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            nt = round(time())
            if nt > (t + 300) or t < (t - 300):
                d = dumps({"code": -3, "msg":
                           "Emm. Seems the current time is not right."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            idd = web.input().get("id")
            if idd is None:
                d = dumps({"code": -4, "msg": "id is needed."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            act = web.input().get("a")
            if act is None or act == '':
                act = web.input().get("action")
            if act is None or act == '':
                d = dumps({"code": -5, "msg":
                           "action type (a/action) is needed."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            if act != 'exists':
                d = dumps({"code": -6, "msg":
                           "action type (a/action) must be 'exists'."},
                          ensure_ascii=False, separators=jsonsep)
                return d if callback is None else f'{callback}({d})'
            db = ProxyDb()
            r = db.get_proxy(idd, True)
            d = dumps({"code": 0, "result": r}, ensure_ascii=False,
                      separators=jsonsep)
            return d if callback is None else f'{callback}({d})'
        except:
            t = ''
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    t = format_exc()
            except:
                pass
            return dumps({"code": -500, "msg": t}, ensure_ascii=False,
                         separators=jsonsep)

    def OPTIONS(self):
        from cors import allowCors
        allowCors()
        return ''


if m:
    application = web.application((".*", "ProxyExists"), globals()).wsgifunc()
