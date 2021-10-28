from requests import Session
from settings import settings
from pixivdb import PixivDb
from functools import wraps
from typing import Dict


AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"


def token_needed(f):
    @wraps(f)
    def o(*args, **kwargs):
        if isinstance(args[0], PixivAPI):
            t: PixivAPI = args[0]
            if not hasattr(t, "_access_token"):
                t.get_token()
            return f(*args, **kwargs)
    return o


class PixivAPI:
    def __init__(self, se: settings, db: PixivDb):
        self._ses = Session()
        self._ses.headers.update({"User-Agent": "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)", "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"})  # noqa: E501
        self._s = se
        self._db = db

    def get_token(self, force: bool = False):
        if self._s.pixivRefreshToken is None:
            raise ValueError('refresh_token is needed.')
        if not force:
            c = self._db.get_token(self._s.pixivRefreshToken)
            if c is not None:
                self._access_token: str = c
        re = self._ses.post(AUTH_TOKEN_URL, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "include_policy": "true",
            "refresh_token": self._s.pixivRefreshToken,
        })
        if re.status_code >= 400:
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        da = re.json()
        self._access_token: str = da['access_token']
        self._db.save_token(self._s.pixivRefreshToken, self._access_token, da.get("expires_in", 0))  # noqa: E501

    def get_headers(self) -> Dict[str, str]:
        d = {}
        if hasattr(self, "_access_token") and isinstance(self._access_token, str):  # noqa: E501
            d['Authorization'] = 'Bearer ' + self._access_token
        return d

    @token_needed
    def getIllusts(self, userId: int, lang: str = None, retry: bool = True):
        h = self.get_headers()
        d = {'user_id': userId}
        if lang is not None:
            d['lang'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v1/user/illusts', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getIllusts(userId, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        return d

    @token_needed
    def getUserDetails(self, userId: int, retry: bool = True):
        h = self.get_headers()
        re = self._ses.get('https://app-api.pixiv.net/v1/user/detail', params={'user_id': userId}, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getUserDetails(userId, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        return d

    @token_needed
    def getBookmarks(self, userId: int, restrict: bool = True,
                     lang: str = None, retry: bool = True):
        h = self.get_headers()
        d = {"user_id": userId}
        d['restrict'] = 'public' if restrict else 'private'
        if lang is not None:
            d['lang'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v1/user/bookmarks/illust', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getBookmarks(userId, restrict, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        return d
