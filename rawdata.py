import web
from typing import Dict, List
from io import BytesIO
from cgi import FieldStorage
ParseQsResult = Dict[str, List[str]]


def getRawData():
    e = web.ctx.env.copy()
    if e.get("CONTENT_TYPE", "").lower().startswith("multipart/"):
        a = web.ctx.get("_fieldstorage")
        if not a:
            fp = e["wsgi.input"]
            a = FieldStorage(fp=fp, environ=e, keep_blank_values=1)
            web.ctx._fieldstorage = a
    else:
        d = web.data()
        if isinstance(d, str):
            d = d.encode("utf-8")
        fp = BytesIO(d)
        a = FieldStorage(fp=fp, environ=e, keep_blank_values=1)
    return a


def getInputStrDict(default: ParseQsResult = None) -> ParseQsResult:
    """从POST DATA中获取得到与parse_qs结果一样的字典，将会自动忽略文件类型"""
    f = getRawData()
    r = {} if not isinstance(default, dict) else default.copy()
    if f.list:
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
