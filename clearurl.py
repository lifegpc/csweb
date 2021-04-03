import web
from traceback import format_exc
from requests import get
from settings import settings
from constants import jsonsep
from json import dumps, load as loadJson
from hashl import sha256
from re import search


class ClearUrl:
    def GET(self):
        try:
            web.header("Content-Type", "application/json; charset=utf-8")
            s = settings()
            s.ReadSettings()
            nod = web.input().get("noda")
            nod = False if nod is None else True
            if not nod:
                r = get(s.clearUrlOrigin)
                r = r.json()
            else:
                r = {"providers": {}}
            li = s.clearUrlCustomList
            h = web.input().get("hash")
            h = False if h is None else True
            if li is None:
                t = dumps(r, separators=jsonsep)
                return sha256(t) if h else t
            ind: str = web.input().get("t")
            ind = ind.split(',') if ind is not None and ind != '' else None
            for i in li:
                if ind is not None and i not in ind:
                    continue
                with open(li[i], 'r', encoding='utf8') as f:
                    j = loadJson(f)
                    if 'providers' in j:
                        for m in j['providers']:
                            ke = m
                            te = ke
                            z = 0
                            re = search(r'^(.+)_(\d+)$', m)
                            if re is not None:
                                re = re.groups()
                                te = re[0]
                                z = int(re[1])
                            while ke in r['providers']:
                                z += 1
                                ke = f"{te}_{z}"
                            r['providers'][ke] = j['providers'][m]
            t = dumps(r, separators=jsonsep)
            return sha256(t) if h else t
        except:
            web.HTTPError('500 Internal Server Error')
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    return format_exc()
            except:
                pass
            return ''
