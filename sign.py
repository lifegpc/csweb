from hashl import sha512
import web
from urllib.parse import quote_plus as q, parse_qs
from rawdata import getInputStrDict
SHA512_TYPE = 1


def verifySign(sercet: str, t: int = SHA512_TYPE):
    query: str = web.ctx.query
    if query is not None and len(query) > 0:
        query = query[1:]
    elif query is None:
        query = ''
    qd = parse_qs(query, keep_blank_values=True)
    if web.ctx.env["REQUEST_METHOD"].lower() == "post":
        qd = getInputStrDict(qd)
    sign = qd["sign"][0] if "sign" in qd else None
    if sign is None or sign == '':
        return False
    para = ''
    keys = qd.keys()
    keys = sorted(keys)
    for k in keys:
        if k != 'sign' and qd[k] is not None:
            for qv in qd[k]:
                v = f"{q(k)}={q(qv)}"
                para = v if para == '' else f"{para}&{v}"
    para = sercet + para
    if t & SHA512_TYPE:
        h = sha512(para)
    else:
        h = sha512(para)
    return True if h == sign else False
