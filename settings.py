from os.path import exists
from json import load as loadjson


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
