import sys
from os.path import abspath
from sqlite3 import connect
from typing import List, Union, Any, Tuple
from time import time_ns
from pickle import loads, dumps
from base64 import b64decode, b64encode
sys.path.append(abspath("../"))
from settings import settings  # noqa: E402


VERSION_TABLE = '''CREATE TABLE version (
id TEXT,
v1 INT,
v2 INT,
v3 INT,
v4 INT,
PRIMARY KEY (id)
);'''
TOKENS_TABLE = '''CREATE TABLE pixiv_tokens (
refresh_token TEXT,
access_token TEXT,
last_update_time INT,
expire INT,
PRIMARY KEY (refresh_token)
);'''
CACHE_TABLE = '''CREATE TABLE pixiv_cache (
id TEXT,
content TEXT,
time INT,
PRIMARY KEY(id)
)'''


class PixivDb:
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
        if 'pixiv_tokens' not in self._exist_tables:
            self._db.execute(TOKENS_TABLE)
        if 'pixiv_cache' not in self._exist_tables:
            self._db.execute(CACHE_TABLE)
        self._db.commit()

    def __init__(self):
        s = settings()
        s.ReadSettings()
        self._db = connect(s.pixivDatabaseLocation)
        if not self.__check_version():
            self.__create_table()

    def __read_version(self) -> List[int]:
        cur = self._db.execute("SELECT * FROM version WHERE id='pixiv';")
        for i in cur:
            return [k for k in i if isinstance(k, int)]

    def __write_version(self):
        if self.__read_version() is None:
            self._db.execute(
                'INSERT INTO version VALUES (?, ?, ?, ?, ?);',
                tuple(['pixiv'] + self.__version))
        else:
            self._db.execute(
                "UPDATE version SET v1=?, v2=?, v3=?, v4=? WHERE id='pixiv';",
                tuple(self.__version))
        self._db.commit()

    def get_cache(self, id: str, cacheTime: int = 5,
                  checkOnly: bool = False) -> Union[Tuple[Any, int], bool]:
        if not checkOnly and cacheTime <= 0:
            return None
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        cur = self._db.execute(
            "SELECT content, time FROM pixiv_cache WHERE id=?;", (id,))
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

    def get_token(self, refresh_token: str,
                  checkOnly: bool = False) -> Union[str, bool]:
        if refresh_token is None or not isinstance(refresh_token, str):
            raise ValueError('refresh_token MUST be string.')
        cur = self._db.execute("SELECT access_token, last_update_time, expire FROM pixiv_tokens WHERE refresh_token=?;", (refresh_token,))  # noqa: E501
        for i in cur:
            if checkOnly:
                return True
            now = time_ns()
            if now < i[1] + round((i[2] - 10) * 1E9):
                return i[0]
            return None
        if checkOnly:
            return False
        return None

    def save_cache(self, id: str, content) -> int:
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        c = b64encode(dumps(content)).decode()
        t = time_ns()
        if self.get_cache(id, checkOnly=True):
            self._db.execute(
                'UPDATE pixiv_cache SET content=?, time=? WHERE id=?;',
                (c, t, id))
        else:
            self._db.execute(
                'INSERT INTO pixiv_cache VALUES (?, ?, ?);', (id, c, t))
        self._db.commit()
        return t

    def save_token(self, refresh_token: str, access_token: str,
                   expire: int) -> bool:
        if refresh_token is None or not isinstance(refresh_token, str):
            raise ValueError('refresh_token MUST be string.')
        if access_token is None or not isinstance(access_token, str):
            raise ValueError('access_token MUST be string.')
        if expire is None or not isinstance(expire, int):
            raise ValueError('expire MUST be a integer.')
        t = time_ns()
        if self.get_token(refresh_token, True):
            self._db.execute("UPDATE pixiv_tokens SET access_token=?, last_update_time=?, expire=? WHERE refresh_token=?;", (access_token, t, refresh_token, expire))  # noqa: E501
        else:
            self._db.execute("INSERT INTO pixiv_tokens VALUES (?, ?, ?, ?);", (refresh_token, access_token, t, expire))  # noqa: E501
        self._db.commit()
        return True
