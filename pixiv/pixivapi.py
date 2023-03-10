from requests import Session
from enum import Enum, unique
from settings import settings
from pixivdb import PixivDb
from functools import wraps
from typing import Dict
from http.cookiejar import MozillaCookieJar
from os.path import exists
from hashl import md5
from textc import timeToStr
from time import time


AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
CLIENT_ID = "KzEZED7aC0vird8jWyHM38mXjNTY"
CLIENT_SECRET = "W9JZoJe00qPvJsiyCGT3CCtC6ZUtdpKpzMbNlUGP"
APP_VERSION = "7.16.6"


def token_needed(f):
    @wraps(f)
    def o(*args, **kwargs):
        if isinstance(args[0], PixivAPI):
            t: PixivAPI = args[0]
            if not hasattr(t, "_access_token"):
                t.get_token()
            return f(*args, **kwargs)
    return o


@unique
class PixivFollowRestrict(Enum):
    ALL = 0
    PRIVATE = 1
    PUBLIC = 2

    def __str__(self):
        if self._value_ == 0:
            return 'all'
        elif self._value_ == 1:
            return 'private'
        elif self._value_ == 2:
            return 'public'


class PixivAPI:
    def __init__(self, se: settings, db: PixivDb):
        self._ses = Session()
        self._ses.headers.update({"User-Agent": "PixivIOSApp/7.16.6 (iOS 16.3; iPad13,18)", "App-Version": APP_VERSION, "App-OS": "ios", "App-OS-Version": "1.16.3"})  # noqa: E501
        self._wses = Session()
        self._wses.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})  # noqa: E501
        self._wses.cookies = MozillaCookieJar()
        if se.pixivProxy:
            self._ses.proxies['all'] = se.pixivProxy
            self._wses.proxies['all'] = se.pixivProxy
        self._s = se
        self._db = db
        self.get_cookies()

    def __del__(self):
        self.save_cookies()

    def get_cookies(self, force: bool = False):
        if self._s.pixivWebCookiesFileLocation is None:
            if force:
                raise ValueError('pixivWebCookiesFileLocation is needed.')
            return False
        else:
            if exists(self._s.pixivWebCookiesFileLocation):
                c: MozillaCookieJar = self._wses.cookies
                c.load(self._s.pixivWebCookiesFileLocation)
                return True
            else:
                return False

    def save_cookies(self):
        if self._s.pixivWebCookiesFileLocation:
            c: MozillaCookieJar = self._wses.cookies
            c.save(self._s.pixivWebCookiesFileLocation)

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
        }, headers=self.get_headers(True))
        if re.status_code >= 400:
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        da = re.json()
        self._access_token: str = da['access_token']
        self._db.save_token(self._s.pixivRefreshToken, self._access_token, da.get("expires_in", 0))  # noqa: E501

    def get_headers(self, skip_access_token: bool = False) -> Dict[str, str]:
        d = {}
        now = timeToStr(time())
        d['X-Client-Time'] = now
        d['X-Client-Hash'] = md5(f'{now}28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c')  # noqa: E501
        if not skip_access_token and hasattr(self, "_access_token") and isinstance(self._access_token, str):  # noqa: E501
            d['Authorization'] = 'Bearer ' + self._access_token
        return d

    @token_needed
    def getIllusts(self, userId: int, lang: str = None, retry: bool = True):
        h = self.get_headers()
        d = {'user_id': userId}
        if lang is not None:
            h['Accept-Language'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v1/user/illusts', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getIllusts(userId, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        for i in d['illusts']:
            if i['type'] == 'ugoira':
                i['ugoira_data'] = self.getUgoira(i['id'])
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
            h['Accept-Language'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v1/user/bookmarks/illust', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getBookmarks(userId, restrict, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        for i in d['illusts']:
            if i['type'] == 'ugoira':
                i['ugoira_data'] = self.getUgoira(i['id'])
        return d

    @token_needed
    def getFollow(self, restrict: PixivFollowRestrict = PixivFollowRestrict.PUBLIC, lang: str = None, retry: bool = True):  # noqa: E501
        h = self.get_headers()
        d = {'restrict': str(restrict)}
        if lang is not None:
            h['Accept-Language'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v2/illust/follow', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getFollow(restrict, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        for i in d['illusts']:
            if i['type'] == 'ugoira':
                i['ugoira_data'] = self.getUgoira(i['id'])
        return d

    def getUgoira(self, id: int, retry: bool = True):
        re = self._wses.get(f'https://www.pixiv.net/ajax/illust/{id}/ugoira_meta')  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_cookies(True)
                return self.getUgoira(id, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        self.save_cookies()
        return d['body']

    def getIllustDetails(self, id: int, lang: str = None, retry: bool = True):
        h = self.get_headers()
        d = {'illust_id': id}
        if lang is not None:
            h['Accept-Language'] = lang
        re = self._ses.get('https://app-api.pixiv.net/v1/illust/detail', params=d, headers=h)  # noqa: E501
        if re.status_code >= 400:
            if retry:
                self.get_token(True)
                return self.getIllustDetails(id, lang, False)
            raise ValueError(f"HTTP ERROR {re.status_code}\n{re.text}")
        d = re.json()
        return d['illust']
