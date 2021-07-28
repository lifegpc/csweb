from typing import Dict


def loadsWithHeaderSep(s: str) -> Dict[str, str]:
    try:
        d = {}
        sl = s.split(';')
        for i in sl:
            i = i.strip()
            ss = i.split('=', 1)
            d[ss[0]] = ss[1]
        return d
    except:
        return None
