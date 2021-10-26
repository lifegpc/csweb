from sign import genSign
from urllib.parse import urlencode
import web


def genUrl(origin: str, serects: str) -> str:
    url = f'{web.ctx.homedomain}/RSSProxy?'
    p = {'t': [origin], 'r': ['https://www.pixiv.net/']}
    p['sign'] = genSign(serects, p)
    url += urlencode(p, doseq=True)
    return url
