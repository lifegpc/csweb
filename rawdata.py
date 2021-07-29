import web
from cgi import FieldStorage
from typing import Dict, List
from tempfile import TemporaryFile
ParseQsResult = Dict[str, List[str]]


class FuckFieldStorage(FieldStorage):
    """
    Subclass cgi.FieldStorage, as read_binary expects fp to return
    bytes. If the headers do not contain a content-disposition with a
    filename, cgi.FieldStorage's make_file will create a TemporaryFile
    with `w+` flags. The write to that temporary file will fail, due
    to incorrect encoding in Python 3.
    """

    def make_file(self, binary=None):
        """
        For backwards compatibility with Python 2, make_file accepted
        a binary flag. This was unused, and removed in Python 3.
        """
        return TemporaryFile("wb+")


def getRawData():
    e = web.ctx.env.copy()
    return FuckFieldStorage(fp=e["wsgi.input"], environ=e, keep_blank_values=1)


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
