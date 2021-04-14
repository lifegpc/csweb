import web
from cgi import FieldStorage
from typing import Dict, List
ParseQsResult = Dict[str, List[str]]


def getRawData():
    e = web.ctx.env.copy()
    return FieldStorage(fp=e["wsgi.input"], environ=e, keep_blank_values=1)


def getInputStrDict(default: ParseQsResult = None) -> ParseQsResult:
    """从POST DATA中获取得到与parse_qs结果一样的字典，将会自动忽略文件类型"""
    f = getRawData()
    r = {} if not isinstance(default, dict) else default.copy()
    for k in f.keys():
        t = f.getlist(k)
        if k in r:
            z = r[k]
        else:
            z = []
            r[k] = z
        for v in t:
            if isinstance(v, str):
                z.append(v)
    return r
