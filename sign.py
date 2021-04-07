from hashl import sha512
import web
from urllib.parse import quote_plus as q
SHA512_TYPE = 1


def verifySign(sercet: str, t: int = SHA512_TYPE):
    sign = web.input().get("sign")
    if sign is None or sign == '':
        return False
    para = ''
    d = web.input()
    keys = d.keys()
    keys = sorted(keys)
    for k in keys:
        if k != 'sign' and d[k] is not None:
            v = f"{q(k)}={q(d[k])}"
            para = v if para == '' else f"{para}&{v}"
    para = sercet + para
    if t & SHA512_TYPE:
        h = sha512(para)
    else:
        h = sha512(para)
    return True if h == sign else False
