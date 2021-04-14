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
    def telegramchatid(self) -> str:
        if self.__data is None:
            return None
        key = 'telegramchatid'
        if key in self.__data and self.__data[key] and self.__data[key] != '':
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
        if key in self.__data and self.__data[key] and self.__data[key] != '':
            return self.__data[key]
        return None
