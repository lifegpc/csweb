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
from json import dumps, loads
from traceback import format_exc
from time import time
from db import ProxyDb
from load import loadsWithHeaderSep
sys.path.append(abspath("../"))
from settings import settings  # noqa: E402
from constants import jsonsep  # noqa: E402
from sign import verifySign  # noqa: E402


class ProxyAdd:
    def GET(self):
        return self.POST()

    def POST(self):
        web.header("Content-Type", "application/json; charset=utf-8")
        try:
            s = settings()
            s.ReadSettings()
            sg = s.proxyAPISecrets
            if sg is None:
                return dumps({"code": -500, "msg":
                              "proxyAPISecrets must be set in settings."},
                             ensure_ascii=False, separators=jsonsep)
            if not verifySign(sg):
                return dumps({"code": -401, "msg": "Unauthorized"},
                             ensure_ascii=False, separators=jsonsep)
            t = web.input().get("t")
            if t is None:
                return dumps({"code": -1, "msg":
                              "current time(t) is needed."},
                             ensure_ascii=False, separators=jsonsep)
            try:
                t = int(t)
            except:
                return dumps({"code": -2, "msg":
                              "current time(t) must be a integer."},
                             ensure_ascii=False, separators=jsonsep)
            nt = round(time())
            if nt > (t + 300) or t < (t - 300):
                return dumps({"code": -3, "msg":
                              "Emm. Seems the current time is not right."},
                             ensure_ascii=False, separators=jsonsep)
            idd = web.input().get("id")
            if idd is None:
                return dumps({"code": -4, "msg": "id is needed."},
                             ensure_ascii=False, separators=jsonsep)
            cookies = web.input().get('c')
            if cookies is None or cookies == '':
                cookies = web.input().get("cookies")
            headers = web.input().get('h')
            if headers is None or headers == '':
                headers = web.input().get("headers")
            if cookies is None:
                cookies = ''
            if headers is None:
                headers = ''
            if cookies == '' and headers == '':
                return dumps({"code": -5, "msg":
                              "cookies or headers is needed."},
                             ensure_ascii=False, separators=jsonsep)
            if cookies != '':
                try:
                    loads(cookies)
                except:
                    tem = loadsWithHeaderSep(cookies)
                    if tem is not None:
                        cookies = dumps(tem, ensure_ascii=False,
                                        separators=jsonsep)
                    else:
                        return dumps({"code": -6, "msg":
                                      "cookies is not a vaild JSON."},
                                     ensure_ascii=False, separators=jsonsep)
            if headers != '':
                try:
                    loads(headers)
                except:
                    tem = loadsWithHeaderSep(headers)
                    if tem is not None:
                        headers = dumps(tem, ensure_ascii=False,
                                        separators=jsonsep)
                    else:
                        return dumps({"code": -7, "msg":
                                      "headers is not a vaild JSON."},
                                     ensure_ascii=False, separators=jsonsep)
            db = ProxyDb()
            r = db.add_proxy(idd, cookies, headers)
            return dumps({"code": 0, "result": r}, ensure_ascii=False,
                         separators=jsonsep)
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


if m:
    application = web.application((".*", "ProxyAdd"), globals()).wsgifunc()
