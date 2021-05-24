from requests import Session
from requests.exceptions import RequestException
from re import search, IGNORECASE
from json import loads
from functools import wraps


def prepared_needed(f):
    @wraps(f)
    def o(*args, **kwargs):
        if isinstance(args[0], TiktokAPI):
            t: TiktokAPI = args[0]
            if not t._prepared:
                t.prepare()
            return f(*args, **kwargs)
    return o


class TiktokAPI:
    def __init__(self):
        self._ses = Session()
        self._ses.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",  # noqa: E 501
                                  "Connection": "keep-alive",
                                  "Accept": "*/*",
                                  "Accept-Language": "zh-CN,zh;q=0.8"})
        self._prepared = False

    @prepared_needed
    def get_video(self, id: str, username: str = None):
        '获取视频'
        try:
            if username is not None:
                url = f"https://www.tiktok.com/@{username}/video/{id}"
            else:
                url = f'https://t.tiktok.com/i18n/share/video/{id}/'
            r = self._ses.get(url)
            if r.status_code != 200:
                return None
            rs = search(r'<script[^>]+\bid=["\']__NEXT_DATA__[^>]+>\s*({.+?})\s*</script',  # noqa: E501
                        r.text, IGNORECASE)
            if rs is None:
                return None
            s = next(g for g in rs.groups() if g is not None)
            d = loads(s)['props']['pageProps']
            d['headers'] = dict(self._ses.headers)
            d['cookies'] = dict(self._ses.cookies)
            return d
        except RequestException:
            return None

    @prepared_needed
    def get_user(self, username: str):
        try:
            r = self._ses.get(f"https://www.tiktok.com/@{username}")
            if r.status_code != 200:
                return None
            rs = search(r'<script[^>]+\bid=["\']__NEXT_DATA__[^>]+>\s*({.+?})\s*</script',  # noqa: E501
                        r.text, IGNORECASE)
            if rs is None:
                return None
            s = next(g for g in rs.groups() if g is not None)
            d = loads(s)['props']['pageProps']
            d['headers'] = dict(self._ses.headers)
            d['cookies'] = dict(self._ses.cookies)
            return d
        except RequestException:
            return None

    def prepare(self):
        self._ses.get("https://www.tiktok.com/")  # 获取必要的cookies
        self._prepared = True
