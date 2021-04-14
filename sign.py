from hashl import sha512
from urllib.parse import quote_plus as q
from rawdata import getInputStrDict
SHA512_TYPE = 1


def verifySign(sercet: str, t: int = SHA512_TYPE):
    qd = getInputStrDict()
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
