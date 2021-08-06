from hashl import sha512
from urllib.parse import quote_plus as q, parse_qs
from rawdata import getInputStrDict, ParseQsResult
SHA512_TYPE = 1


def genSign(sercet: str, qd: ParseQsResult, t: int = SHA512_TYPE):
    para = ''
    keys = qd.keys()
    keys = sorted(keys)
    for k in keys:
        if k != 'sign' and qd[k] is not None:
            qd[k].sort()
            for qv in qd[k]:
                v = f"{q(k)}={q(qv)}"
                para = v if para == '' else f"{para}&{v}"
    para = sercet + para
    if t & SHA512_TYPE:
        h = sha512(para)
    else:
        h = sha512(para)
    return h


def verifySign(sercet: str, onlyQuery: bool = False, t: int = SHA512_TYPE):
    if onlyQuery:
        import web
        e = web.ctx.env.copy()
        qs = e['QUERY_STRING']
    qd = parse_qs(qs) if onlyQuery else getInputStrDict()
    sign = qd["sign"][0] if "sign" in qd else None
    if sign is None or sign == '':
        return False
    h = genSign(sercet, qd, t)
    return True if h == sign else False
