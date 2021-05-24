from sign import genSign
from urllib.parse import urlencode
import web
from json import dumps
from constants import jsonsep


def genUrl(origin: str, serects: str, d: dict = None, ref: str = None) -> str:
    url = f'{web.ctx.homedomain}/RSSProxy?'
    p = {'t': [origin]}
    li = [('t', origin)]
    if d is not None:
        if 'cookies' in d:
            t = dumps(d['cookies'], ensure_ascii=False, separators=jsonsep)
            p['c'] = [t]
            li.append(('c', t))
        if 'headers' in d:
            t = dumps(d['headers'], ensure_ascii=False, separators=jsonsep)
            p['h'] = [t]
            li.append(('h', t))
    if ref is not None:
        p['r'] = [ref]
        li.append(('r', ref))
    h = genSign(serects, p)
    li.sort(key=lambda t: t[0])
    li.append(('sign', h))
    url += urlencode(li)
    return url
