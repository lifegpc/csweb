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
from urllib.parse import urlparse, urlencode
sys.path.append(abspath("../"))
from settings import settings  # noqa: E402
from constants import jsonsep  # noqa: E402
from sign import verifySign, genSign  # noqa: E402


class ProxyGen:
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
            target = web.input().get("target")
            if target is None or target == '':
                return dumps({"code": -5, "msg":
                              "target url (targte) is needed."},
                             ensure_ascii=False, separators=jsonsep)
            act = web.input().get("a")
            if act is None or act == '':
                act = web.input().get("action")
            if act is None or act == '':
                return dumps({"code": -7, "msg":
                              "action type (a/action) is needed."},
                             ensure_ascii=False, separators=jsonsep)
            if act != 'gen':
                return dumps({"code": -8, "msg":
                              "action type (a/action) must be 'gen'."},
                             ensure_ascii=False, separators=jsonsep)
            exp = web.input().get("e")
            if exp is None or exp == '':
                exp = web.input().get("expired")
            if exp is not None and exp != '':
                try:
                    exp = int(exp)
                except:
                    return dumps({"code": -9, "msg":
                                  "expired time (e/expired) must be a integer."
                                  }, ensure_ascii=False, separators=jsonsep)
            else:
                exp = None
            db = ProxyDb()
            r = db.get_proxy(idd, True)
            if not r:
                return dumps({"code": -6, "msg":
                              "Can not find this id in database."},
                             ensure_ascii=False, separators=jsonsep)
            ent = s.proxyEntry
            entr = urlparse(ent)
            if entr.netloc == '' and entr.path.startswith('/'):
                ent = f'{web.ctx.homedomain}{ent}'
            se = {"t": [target], "id": [idd]}
            if exp is not None:
                se["e"] = [str(exp)]
            t = genSign(s.proxyAPISecrets, se)
            se.update({"sign": [t]})
            for i in se:
                se[i] = se[i][0]
            url = f'{ent}?{urlencode(se)}'
            return dumps({"code": 0, "result": url}, ensure_ascii=False,
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
    application = web.application((".*", "ProxyGen"), globals()).wsgifunc()
