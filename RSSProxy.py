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
from requests import Session, Response


def parseBool(inp: str, default: bool) -> bool:
    if inp is None:
        return default
    lo = inp.lower()
    if lo == 'true':
        return True
    elif lo == 'false':
        return False
    try:
        i = int(lo)
        return bool(i)
    except Exception:
        pass
    return bool(inp)


class RSSProxy:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}  # noqa: E501
        e = web.ctx.env.copy()
        for k in ['User-Agent', 'Range', 'Accept', 'If-Modified-Since']:
            km = "HTTP_" + k.upper().replace('-', '_')
            if km in e:
                headers[k] = e[km]
        ref = web.input().get("r")
        if ref is not None:
            headers['referer'] = ref
        ses = Session()
        ses.headers.update(headers)
        cookie = web.input().get("c")
        if cookie is not None:
            from json import loads
            ses.cookies.update(loads(cookie))
        header = web.input().get("h")
        if header is not None:
            from json import loads
            ses.headers.update(loads(header))
        allow_redirects = parseBool(web.input().get("ar"), True)
        return_redirect_as_json = parseBool(web.input().get("rraj"), False)
        re = ses.get(t, stream=True, allow_redirects=allow_redirects)
        if re.status_code != 200:
            if re.status_code in [301, 302, 307] and return_redirect_as_json:
                web.HTTPError(f"200 OK")
                from json import dumps
                from constants import jsonsep
                return dumps({"code": re.status_code, "location": re.headers.get("Location")}, ensure_ascii=False, separators=jsonsep)  # noqa: E501
            else:
                web.HTTPError(f"{re.status_code} {re.reason}")
        h = re.headers
        for i in ['cache-control', 'content-length', 'content-type', 'date',
                  'last-modified', 'content-range', 'age', 'expires',
                  'keep-alive', 'location', 'server']:
            if i == 'content-length':
                if 'content-encoding' in h and h['content-encoding'] != 'identity':  # noqa: E501
                    continue
            if i in h:
                web.header(i, h[i])
        return self.send(re)

    def send(self, r: Response):
        for i in r.iter_content(1024):
            if i:
                yield i

    def OPTIONS(self):
        from cors import allowCors
        allowCors(methods=['GET', 'OPTIONS'], headers=['If-Modified-Since'])
        return ''


if m:
    application = web.application((".*", "RSSProxy"), globals()).wsgifunc()
