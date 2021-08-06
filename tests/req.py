from requests import Session, Response
from sign import genSign
from rawdata import ParseQsResult
from urllib.parse import urlencode, urlparse, urlunparse, ParseResult


def dealAPIResponse(r: Response, allowNonZeroCode: bool = False):
    if r.status_code >= 400:
        raise ValueError(f'Get {r.status_code} {r.reason}')
    re = r.json()
    if not allowNonZeroCode:
        if re['code'] != 0:
            raise ValueError(f"API return code {re['code']}: {re['msg']}")
        return re['result']
    return re


class Req:
    _host = 'http://127.0.0.1:2600'
    _sercet = None

    def __init__(self, sercet: str = None):
        self._ses = Session()
        self._ses.trust_env = False
        if sercet is not None:
            self._sercet = sercet

    def get(self, path: str, **k):
        return self.request("get", path, **k)

    def getWithSign(self, path: str, p: ParseQsResult, **k):
        return self.requestWithSign("get", path, p, **k)

    def post(self, path: str, **k):
        return self.request("post", path, **k)

    def postWithSign(self, path: str, p: ParseQsResult, **k):
        return self.requestWithSign("post", path, p, **k)

    def request(self, method: str, path: str, **k):
        return self._ses.request(method, f"{self._host}{path}", **k)

    def requestWithSign(self, method: str, path: str, p: ParseQsResult, **k):
        if self._sercet is None:
            return self.request(method, path, **k)
        h = genSign(self._sercet, p)
        p['sign'] = [h]
        if method.upper() == 'GET':
            r = urlparse(path)
            path = urlunparse(ParseResult(r[0], r[1], r[2], r[3],
                                          urlencode(p, doseq=True), r[5]))
            return self.request('get', path, **k)
        return self.request(method, path, data=p, **k)
