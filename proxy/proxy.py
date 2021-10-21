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
from time import time
from db import ProxyDb
from json import loads
from requests import Session, Response
sys.path.append(abspath("../"))
from settings import settings  # noqa: E402
from sign import verifySign  # noqa: E402


class ProxyProxy:
    def GET(self):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            s = settings()
            s.ReadSettings()
            sg = s.proxyAPISecrets
            if sg is None:
                web.header('Content-Type', 'text/plain; charset=UTF-8')
                web.HTTPError('500 Internal Server Error')
                return "proxyAPISecrets must be set in settings."
            if not verifySign(sg):
                web.HTTPError('401 Unauthorized')
                return ''
            t = web.input().get('t')
            if t is None or t == '':
                t = web.input().get("target")
            if t is None or t == '':
                web.header('Content-Type', 'text/plain; charset=UTF-8')
                web.HTTPError('400 Bad Request')
                return 'target url (t/target) is needed.'
            idd = web.input().get("id")
            if idd == '':
                idd = None
            exp = web.input().get("e")
            if exp is None or exp == '':
                exp = web.input().get("expired")
            if exp is not None and exp != '':
                try:
                    exp = int(exp)
                except:
                    web.header('Content-Type', 'text/plain; charset=UTF-8')
                    web.HTTPError('400 Bad Request')
                    return 'Expired time should be a integer.'
                nt = round(time())
                if nt > exp:
                    web.header('Content-Type', 'text/plain; charset=UTF-8')
                    web.HTTPError('400 Bad Request')
                    return 'This reverse proxy link is expired.'
            if idd is not None:
                db = ProxyDb()
                r = db.get_proxy(idd)
                if r is None:
                    web.header('Content-Type', 'text/plain; charset=UTF-8')
                    web.HTTPError('400 Bad Request')
                    return 'Can not find this id in database.'
            else:
                r = ('{}', '{}')
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}  # noqa: E501
            if r[1] != '':
                try:
                    headers.update(loads(r[1]))
                except:
                    pass
            e = web.ctx.env.copy()
            for k in ['User-Agent', 'Range', 'Accept', 'If-Modified-Since']:
                km = "HTTP_" + k.upper().replace('-', '_')
                if km in e:
                    headers[k] = e[km]
            ref = web.input().get("r")
            if ref is not None:
                headers['referer'] = ref
            ses = Session()
            if r[0] != '':
                try:
                    ses.cookies.update(loads(r[0]))
                except:
                    pass
            ses.headers.update(headers)
            cookie = web.input().get("c")
            if cookie is not None:
                try:
                    ses.cookies.update(loads(cookie))
                except:
                    pass
            header = web.input().get("h")
            if header is not None:
                try:
                    ses.headers.update(loads(header))
                except:
                    pass
            re = ses.get(t, stream=True)
            if re.status_code != 200:
                web.HTTPError(f"{re.status_code} {re.reason}")
            h = re.headers
            for i in ['cache-control', 'content-length', 'content-type',
                      'date', 'last-modified', 'content-range', 'age',
                      'expires', 'keep-alive', 'location', 'server']:
                if i in h:
                    web.header(i, h[i])
            return self.send(re)
        except:
            web.header('Content-Type', 'text/plain; charset=UTF-8')
            web.HTTPError('500 Internal Server Error')
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    return format_exc()
            except:
                pass
            return ''

    def send(self, r: Response):
        for i in r.iter_content(1024):
            if i:
                yield i

    def OPTIONS(self):
        from cors import allowCors
        allowCors(methods=['GET', 'OPTIONS'], headers=['If-Modified-Since'])
        return ''


if m:
    application = web.application((".*", "ProxyProxy"), globals()).wsgifunc()
