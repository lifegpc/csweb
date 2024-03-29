from sqlite3 import connect
from settings import settings
from typing import List, Any, Union, Tuple
from pickle import dumps, loads
from base64 import b64encode, b64decode
from time import time_ns


VERSION_TABLE = '''CREATE TABLE version (
id TEXT,
v1 INT,
v2 INT,
v3 INT,
v4 INT,
PRIMARY KEY (id)
);'''
CACHE_TABLE = '''CREATE TABLE tiktok_cache (
id TEXT,
content TEXT,
time INT,
PRIMARY KEY(id)
)'''


class TiktokDatabase:
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
        if 'tiktok_cache' not in self._exist_tables:
            self._db.execute(CACHE_TABLE)
        self._db.commit()

    def __init__(self):
        s = settings()
        s.ReadSettings()
        self._db = connect(s.tiktokDatabaseLocation)
        if not self.__check_version():
            self.__create_table()

    def __read_version(self) -> List[int]:
        cur = self._db.execute("SELECT * FROM version WHERE id='tiktok';")
        for i in cur:
            return [k for k in i if isinstance(k, int)]

    def __write_version(self):
        if self.__read_version() is None:
            self._db.execute(
                'INSERT INTO version VALUES (?, ?, ?, ?, ?);',
                tuple(['tiktok'] + self.__version))
        else:
            self._db.execute(
                "UPDATE version SET v1=?, v2=?, v3=?, v4=? WHERE id='tiktok';",
                tuple(self.__version))
        self._db.commit()

    def get_cache(self, id: str, cacheTime: int = 15,
                  checkOnly: bool = False) -> Union[Tuple[Any, int], bool]:
        if not checkOnly and cacheTime <= 0:
            return None
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        cur = self._db.execute(
            "SELECT content, time FROM tiktok_cache WHERE id=?;", (id,))
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

    def remove_cache(self, id: str):
        if self.get_cache(id, checkOnly=True):
            self._db.execute('DELETE FROM tiktok_cache WHERE id=?;', (id,))
            self._db.commit()

    def save_cache(self, id: str, content) -> int:
        if id is None or not isinstance(id, str):
            raise ValueError('id MUST be string.')
        c = b64encode(dumps(content)).decode()
        t = time_ns()
        if self.get_cache(id, checkOnly=True):
            self._db.execute(
                'UPDATE tiktok_cache SET content=?, time=? WHERE id=?;',
                (c, t, id))
        else:
            self._db.execute(
                'INSERT INTO tiktok_cache VALUES (?, ?, ?);', (id, c, t))
        self._db.commit()
        return t
