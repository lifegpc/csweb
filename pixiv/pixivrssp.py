from sign import genSign
from urllib.parse import urlencode, urlparse
import web


def genUrl(origin: str, serects: str, add_fn: bool = False) -> str:
    fn = ''
    if add_fn:
        p = urlparse(origin).path
        if p != '':
            fn = '/' + p.split('/')[-1]
    url = f'{web.ctx.homedomain}/RSSProxy{fn}?'
    p = {'t': [origin], 'r': ['https://www.pixiv.net/']}
    p['sign'] = genSign(serects, p)
    url += urlencode(p, doseq=True)
    return url
