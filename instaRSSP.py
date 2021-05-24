from sign import genSign
from urllib.parse import urlencode
import web


def genUrl(origin: str, serects: str) -> str:
    url = f'{web.ctx.homedomain}/RSSProxy?'
    p = {'t': [origin]}
    h = genSign(serects, p)
    url += urlencode([('t', origin), ('sign', h)])
    return url
