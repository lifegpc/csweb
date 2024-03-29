from sqlite3 import connect
from settings import settings
from typing import List, Any, Union, Tuple
from pickle import dumps, loads
from base64 import b64encode, b64decode
from time import time_ns
from hashl import sha512


VERSION_TABLE = '''CREATE TABLE version (
id TEXT,
v1 INT,
v2 INT,
v3 INT,
v4 INT,
PRIMARY KEY (id)
);'''
COOKIES_TABLE = '''CREATE TABLE insta_cookies (
username TEXT,
cookies TEXT,
PRIMARY KEY(username)
)'''
CACHE_TABLE = '''CREATE TABLE insta_cache (
id TEXT,
content TEXT,
time INT,
PRIMARY KEY(id)
)'''
VERIFY_TABLE = '''CREATE TABLE insta_verify (
sign TEXT,
id TEXT,
code TEXT,
username TEXT,
time INT,
PRIMARY KEY(sign)
)'''
MAX_VERIFY_TIME = 600


class InstaDatabase:
    __version = [1, 0, 0, 0]

    def __check_version(self):
        cur = self._db.execute('SELECT * FROM main.sqlite_master;')
        self._exist_tables = {}
        for i in cur:
            if i[0] == 'table':
                self._exist_tables[i[1]] = i
        if 'version' not in self._exist_tables:
            return False
        v = self.__read_version()
        if v is None:
            return False
        elif v < self.__version:
            self.__write_version()
        return True

    def __create_table(self):
        if 'version' not in self._exist_tables:
            self._db.execute(VERSION_TABLE)
        self.__write_version()
        if 'insta_cookies' not in self._exist_tables:
            self._db.execute(COOKIES_TABLE)
        if 'insta_cache' not in self._exist_tables:
            self._db.execute(CACHE_TABLE)
        if 'insta_verify' not in self._exist_tables:
            self._db.execute(VERIFY_TABLE)
        self._db.commit()

    def __get_verify(self, sign: str, checkOnly=False) -> Union[bool, Tuple[
            str, str, str, int]]:
        if sign is None or not isinstance(sign, str):
            raise ValueError('sign MUST be string.')
        cur = self._db.execute(
            'SELECT id, code, username, time FROM insta_verify WHERE sign=?;',
            (sign, ))
        for i in cur:
            if checkOnly:
                return True
            return i[0], i[1], i[2], int(i[3])
        if checkOnly:
            return False
        return None

    def __init__(self):
        s = settings()
        s.ReadSettings()
        self._db = connect(s.instagramDatabaseLocation)
        if not self.__check_version():
            self.__create_table()

    def __read_version(self) -> List[int]:
        cur = self._db.execute("SELECT * FROM version WHERE id='insta';")
        for i in cur:
            return [k for k in i if isinstance(k, int)]

    def __write_version(self):
        if self.__read_version() is None:
            self._db.execute(
                'INSERT INTO version VALUES (?, ?, ?, ?, ?);',
                tuple(['insta'] + self.__version))
        else:
            self._db.execute(
                "UPDATE version SET v1=?, v2=?, v3=?, v4=? WHERE id='insta';",
                tuple(self.__version))
        self._db.commit()

    def get_cache(self, id: str, cacheTime: int = 15,
                  checkOnly: bool = False) -> Union[Tuple[Any, int], bool]:
        if not checkOnly and cacheTime <= 0:
            return None
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        cur = self._db.execute(
            "SELECT content, time FROM insta_cache WHERE id=?;", (id,))
        for i in cur:
            if checkOnly:
                return True
            now = time_ns()
            ct = round(cacheTime * 6E10)
            t = int(i[1])
            if now < ct + t:
                return loads(b64decode(i[0].encode())), t
            else:
                return None
        if checkOnly:
            return False
        return None

    def get_cookies(self, username: str, checkOnly: bool = False):
        if username is None or not isinstance(username, str):
            raise ValueError("username MUST be string.")
        cur = self._db.execute(
            "SELECT cookies FROM insta_cookies WHERE username=?;", (username,))
        for i in cur:
            if checkOnly:
                return True
            return loads(b64decode(i[0].encode()))
        if checkOnly:
            return False
        return None

    def get_verify(self, sign: str) -> Tuple[str, str, str, int]:
        v = self.__get_verify(sign)
        if v is None:
            return None
        self.remove_verify(sign)
        t = v[3]
        n = time_ns()
        if n < t + round(MAX_VERIFY_TIME * 1E9):
            return v
        else:
            return None

    def remove_cache(self, id: str):
        if self.get_cache(id, checkOnly=True):
            self._db.execute('DELETE FROM insta_cache WHERE id=?;', (id,))
            self._db.commit()

    def remove_cookies(self, username: str):
        if self.get_cookies(username, True):
            self._db.execute(
                'DELETE FROM insta_cookies WHERE username=?;', (username,))
            self._db.commit()

    def remove_verify(self, sign: str):
        if self.__get_verify(sign, True):
            self._db.execute('DELETE FROM insta_verify WHERE sign=?;', (sign,))
        self._db.commit()

    def save_cache(self, id: str, content) -> int:
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        c = b64encode(dumps(content)).decode()
        t = time_ns()
        if self.get_cache(id, checkOnly=True):
            self._db.execute(
                'UPDATE insta_cache SET content=?, time=? WHERE id=?;',
                (c, t, id))
        else:
            self._db.execute(
                'INSERT INTO insta_cache VALUES (?, ?, ?);', (id, c, t))
        self._db.commit()
        return t

    def save_cookies(self, username: str, cookies):
        t = b64encode(dumps(cookies)).decode()
        if username is None or not isinstance(username, str):
            raise ValueError("username MUST be string.")
        if self.get_cookies(username, True):
            self._db.execute(
                'UPDATE insta_cookies SET cookies=? WHERE username=?;',
                (t, username))
        else:
            self._db.execute(
                'INSERT INTO insta_cookies VALUES (?, ?);', (username, t))
        self._db.commit()

    def save_verify(self, id: str, code: str, username: str) -> str:
        if id is None or not isinstance(id, str):
            raise ValueError("id MUST be string.")
        if code is None or not isinstance(code, str):
            raise ValueError("code MUST be string.")
        if username is None or not isinstance(username, str):
            raise ValueError("username MUST be string.")
        t = time_ns()
        sign = sha512(f"{t},{id},{code},{username}")
        if self.__get_verify(sign, True):
            self._db.execute(
                'UPDATE insta_verify SET id=?, code=?, time=?, username=? WHERE sign=?;',  # noqa: E501
                (id, code, t, username, sign))
        else:
            self._db.execute(
                'INSERT INTO insta_verify VALUES (?, ?, ?, ?, ?);',
                (sign, id, code, username, t))
        self._db.commit()
        return sign
