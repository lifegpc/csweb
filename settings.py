from os.path import exists
from json import load as loadjson
from typing import Dict, List


class settings:
    def ReadSettings(self):
        if exists('settings.json'):
            try:
                with open('settings.json', 'r', encoding='utf8') as f:
                    self.__data = loadjson(f)
            except:
                self.__data = None
        elif exists('../settings.json'):
            try:
                with open('../settings.json', 'r', encoding='utf8') as f:
                    self.__data = loadjson(f)
            except:
                self.__data = None
        else:
            self.__data = None

    @property
    def captcha2sercetkey(self) -> str:
        if self.__data is None:
            return None
        key = 'captcha2sercetkey'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def captcha2sitekey(self) -> str:
        if self.__data is None:
            return None
        key = 'captcha2sitekey'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def debug(self) -> bool:
        if self.__data is None:
            return False
        key = 'debug'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def telegrambotkey(self) -> str:
        if self.__data is None:
            return None
        key = 'telegrambotkey'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def telegramchatid(self) -> int:
        if self.__data is None:
            return None
        key = 'telegramchatid'
        if key in self.__data and self.__data[key]:
            return self.__data[key]
        return None

    @property
    def clearUrlOrigin(self) -> str:
        defalut = 'https://rules2.clearurls.xyz/data.minify.json'
        if self.__data is None:
            return defalut
        key = 'clearUrlOrigin'
        if key in self.__data and self.__data[key]:
            return self.__data[key]
        return defalut

    @property
    def clearUrlCustomList(self) -> Dict[str, str]:
        if self.__data is None:
            return None
        key = 'clearUrlCustomList'
        if key in self.__data and self.__data[key] is not None:
            if isinstance(self.__data[key], list):
                if len(self.__data[key]) > 0:
                    r = {}
                    k = 1
                    for i in self.__data[key]:
                        if isinstance(i, str) and i != '' and exists(i):
                            r[str(k)] = i
                            k += 1
                    if k > 1:
                        return r
            elif isinstance(self.__data[key], dict):
                r = {}
                m = self.__data[key]
                kl = m.keys()
                z = 0
                for i in kl:
                    if isinstance(m[i], str) and m[i] != '' and exists(m[i]):
                        r[i] = m[i]
                        z += 1
                if z >= 1:
                    return r
            elif isinstance(self.__data[key], str) and self.__data[key] != '':
                if exists(self.__data[key]):
                    return {"1": self.__data[key]}
        return None

    @property
    def defaultSvgFont(self) -> str:
        default = 'Microsoft Sans Serif'
        if self.__data is None:
            return None
        key = 'defaultSvgFont'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def everyPushServer(self) -> str:
        if self.__data is None:
            return None
        key = 'everyPushServer'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def everyPushToken(self) -> str:
        if self.__data is None:
            return None
        key = 'everyPushToken'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def fontLocationMap(self) -> Dict[str, str]:
        if self.__data is None:
            return None
        key = 'fontLocationMap'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def cfwProfileSecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'cfwProfileSecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def webpageCacheTime(self) -> int:
        if self.__data is None:
            return None
        key = 'webpageCacheTime'
        if key in self.__data and self.__data[key] and self.__data[key] > 0:
            return self.__data[key]
        return None

    @property
    def instagramRSSSecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'instagramRSSSecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def instagramCacheTime(self) -> int:
        '缓存时间（分），0为禁用'
        default = 15
        if self.__data is None:
            return default
        key = 'instagramCacheTime'
        if key in self.__data and self.__data[key] is not None:
            v = self.__data[key]
            if isinstance(v, (int, float)):
                v = round(v)
                if v >= 0:
                    return v
            elif isinstance(v, str):
                if v.isnumeric():
                    return int(v)
        return default

    @property
    def instagramDatabaseLocation(self) -> str:
        default = 'data.db'
        if self.__data is None:
            return default
        key = 'instagramDatabaseLocation'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def instagramUsername(self) -> str:
        if self.__data is None:
            return None
        key = 'instagramUsername'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def instagramPassword(self) -> str:
        if self.__data is None:
            return None
        key = 'instagramPassword'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def isntagramCacheRSS(self) -> bool:
        if self.__data is None:
            return False
        key = 'isntagramCacheRSS'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def RSSProxySerects(self) -> str:
        if self.__data is None:
            return None
        key = 'RSSProxySerects'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def notiAPITelegramBotAPIKey(self) -> str:
        if self.__data is None:
            return None
        key = 'notiAPITelegramBotAPIKey'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return self.telegrambotkey

    @property
    def notiAPITelegraBotChatId(self) -> int:
        if self.__data is None:
            return None
        key = 'notiAPITelegraBotChatId'
        if key in self.__data and self.__data[key]:
            return self.__data[key]
        return self.telegramchatid

    @property
    def notiAPISecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'notiAPISecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def tiktokDatabaseLocation(self) -> str:
        default = 'data.db'
        if self.__data is None:
            return default
        key = 'tiktokDatabaseLocation'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def tiktokRSSSecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'tiktokRSSSecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def tiktokCacheRSS(self) -> bool:
        if self.__data is None:
            return False
        key = 'tiktokCacheRSS'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def proxyDatabaseLocation(self) -> str:
        default = 'data.db'
        if self.__data is None:
            return default
        key = 'proxyDatabaseLocation'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def proxyAPISecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'proxyAPISecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def proxyEntry(self) -> str:
        default = '/proxy/proxy'
        if self.__data is None:
            return default
        key = 'proxyEntry'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def pixivRefreshToken(self) -> str:
        if self.__data is None:
            return None
        key = 'pixivRefreshToken'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def pixivCacheTime(self) -> int:
        default = 5
        if self.__data is None:
            return default
        key = 'pixivCacheTime'
        if key in self.__data and self.__data[key] is not None:
            v = self.__data[key]
            if isinstance(v, (int, float)):
                v = round(v)
                if v >= 0:
                    return v
            elif isinstance(v, str):
                if v.isnumeric():
                    return int(v)
        return default

    @property
    def pixivDatabaseLocation(self) -> str:
        default = 'data.db'
        if self.__data is None:
            return default
        key = 'pixivDatabaseLocation'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return default

    @property
    def pixivRSSSecrets(self) -> str:
        if self.__data is None:
            return None
        key = 'pixivRSSSecrets'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def pixivCacheRSS(self) -> bool:
        if self.__data is None:
            return False
        key = 'pixivCacheRSS'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def pixivWebCookiesFileLocation(self) -> str:
        if self.__data is None:
            return None
        key = 'pixivWebCookiesFileLocation'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def pixivEnableUgoira(self) -> bool:
        if self.__data is None:
            return False
        key = 'pixivEnableUgoira'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def pixivProxy(self) -> bool:
        if self.__data is None:
            return None
        key = 'pixivProxy'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def pixivSinglePageCacheTime(self) -> int:
        default = 360
        if self.__data is None:
            return default
        key = 'pixivSinglePageCacheTime'
        if key in self.__data and self.__data[key] is not None:
            v = self.__data[key]
            if isinstance(v, (int, float)):
                v = round(v)
                if v >= 0:
                    return v
            elif isinstance(v, str):
                if v.isnumeric():
                    return int(v)
        return default

    @property
    def onlyOfficeEndpoint(self) -> str:
        if self.__data is None:
            return None
        key = 'onlyOfficeEndpoint'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def onlyOfficeAllowOrigins(self) -> List[str]:
        if self.__data is None:
            return []
        key = 'onlyOfficeAllowOrigins'
        if key in self.__data:
            v = self.__data[key]
            if isinstance(v, str) and v != '':
                return [v]
            elif isinstance(v, list):
                t = []
                for i in v:
                    if isinstance(i, str) and i != '':
                        t.append(i)
                return t
        return []

    @property
    def onlyOfficeToken(self) -> str:
        if self.__data is None:
            return None
        key = 'onlyOfficeToken'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None

    @property
    def sendMsgToMeUseEveryPush(self) -> bool:
        if self.__data is None:
            return False
        key = 'sendMsgToMeUseEveryPush'
        if key in self.__data and self.__data[key]:
            return True
        return False

    @property
    def geoDatabase(self) -> str:
        if self.__data is None:
            return None
        key = 'geoDatabase'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None
