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
from traceback import format_exc
from requests import get
from settings import settings
from constants import jsonsep
from json import dumps, load as loadJson
from hashl import sha256
from re import search
from drawBagel import drawBagel


class ClearUrl:
    def GET(self):
        try:
            web.header("Content-Type", "application/json; charset=utf-8")
            s = settings()
            s.ReadSettings()
            bagel = web.input().get("bagel")
            bagel = False if bagel is None else True
            nod = web.input().get("noda")
            nod = False if nod is None else True
            ol = 0
            if not nod:
                r = get(s.clearUrlOrigin)
                r = r.json()
                ol = len(r['providers'])
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
            vt = []
            for i in li:
                if ind is not None and i not in ind:
                    continue
                elif ind is not None:
                    vt.append(i)
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
                            while ke in r['providers']:
                                z += 1
                                ke = f"{te}_{z}"
                            r['providers'][ke] = j['providers'][m]
            t = dumps(r, separators=jsonsep)
            if h:
                return sha256(t)
            elif bagel:
                lt = str(len(r["providers"].keys()))
                adm = []
                if int(lt) == ol:
                    adm.append('no any custom rules')
                if int(lt) != ol and ind is not None:
                    adm.append('types: ' + '; '.join(vt))
                if not nod:
                    adm.append(f'include {ol} offical rules')
                at = ', '.join(adm)
                at = '' if at == '' else f" ({at})"
                rt = f'custom rules{at}'
                svg = drawBagel(lt, rt, leftColor='#555', rightColor='#007ec6',
                                spacing=3)
                web.header('Content-Type', 'image/svg+xml')
                web.header('Cache-Control', 'public, max-age=300')
                return svg
            else:
                return t
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


if m:
    application = web.application((".*", "ClearUrl"), globals()).wsgifunc()
