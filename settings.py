from os.path import exists
from json import load as loadjson
from typing import Dict


class settings:
    def ReadSettings(self):
        if exists('settings.json'):
            try:
                with open('settings.json', 'r', encoding='utf8') as f:
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
            if isinstance(v, [int, float]):
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
