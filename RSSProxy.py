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
from settings import settings
from sign import verifySign
import requests


class RSSProxy:
    def GET(self):
        s = settings()
        s.ReadSettings()
        if s.RSSProxySerects is None:
            web.HTTPError('500 Internal Server Error')
            return 'RSSProxySerects is needed in settings.'
        if not verifySign(s.RSSProxySerects):
            web.HTTPError('401 Unauthorized')
            return ''
        t = web.input().get("t")
        if t is None:
            web.HTTPError('400 Bad Request')
            return ''
        headers = {}
        e = web.ctx.env.copy()
        for k in ['User-Agent', 'Range', 'Accept', 'If-Modified-Since',
                  'Keep-Alive']:
            km = "HTTP_" + k.upper().replace('-', '_')
            if km in e:
                headers[k] = e[km]
        re = requests.get(t, headers=headers)
        if re.status_code != 200:
            web.HTTPError(f"{re.status_code} {re.reason}")
        h = re.headers
        for i in ['cache-control', 'content-length', 'content-type', 'date',
                  'last-modified', 'content-range', 'age', 'expires',
                  'keep-alive', 'location', 'server']:
            if i in h:
                web.header(i, h[i])
        return re.content


if m:
    application = web.application((".*", "RSSProxy"), globals()).wsgifunc()
