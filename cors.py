import web
from typing import List


def allowCors(origin: str = '*', methods: List[str] = None,
              headers: List[str] = None, maxAge: int = 86400):
    web.header('Access-Control-Allow-Origin', origin)
    if methods is None:
        methods = ['POST', 'GET', 'OPTIONS']
    web.header('Access-Control-Allow-Methods', ', '.join(methods))
    if headers is not None:
        web.header('Access-Control-Allow-Headers', ', '.join(headers))
    web.header('Access-Control-Max-Age', str(maxAge))
