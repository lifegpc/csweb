import sys
from os.path import abspath
from sqlite3 import connect
from typing import List, Union, Tuple
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
PROXY_TABLE = '''CREATE TABLE proxy (
id TEXT,
cookies TEXT,
headers TEXT,
PRIMARY KEY (id)
);'''


class ProxyDb:
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
        if 'proxy' not in self._exist_tables:
            self._db.execute(PROXY_TABLE)
        self._db.commit()

    def __init__(self):
        s = settings()
        s.ReadSettings()
        self._db = connect(s.proxyDatabaseLocation)
        if not self.__check_version():
            self.__create_table()

    def __read_version(self) -> List[int]:
        cur = self._db.execute("SELECT * FROM version WHERE id='proxy';")
        for i in cur:
            return [k for k in i if isinstance(k, int)]

    def __write_version(self):
        if self.__read_version() is None:
            self._db.execute(
                'INSERT INTO version VALUES (?, ?, ?, ?, ?);',
                tuple(['proxy'] + self.__version))
        else:
            self._db.execute(
                "UPDATE version SET v1=?, v2=?, v3=?, v4=? WHERE id='proxy';",
                tuple(self.__version))
        self._db.commit()

    def add_proxy(self, id: str, cookies: str = '', headers: str = ''):
        '''Add new proxy to database. If already exists, override old value.'''
        if id is None or cookies is None or headers is None:
            return False
        if self.get_proxy(id, True):
            try:
                self._db.execute(
                    'UPDATE proxy SET cookies=?, headers=? WHERE id=?;',
                    (cookies, headers, id))
            except:
                return False
        else:
            try:
                self._db.execute('INSERT INTO proxy VALUES (?, ?, ?);',
                                 (id, cookies, headers))
            except:
                return False
        self._db.commit()
        return True

    def delete_proxy(self, id: str) -> bool:
        if not self.get_proxy(id, True):
            return False
        try:
            self._db.execute('DELETE FROM proxy WHERE id=?;', (id,))
        except:
            return False
        self._db.commit()
        return True

    def get_proxy(self, id: str, only_check: bool = False) -> Union[
            bool, Tuple[str, str]]:
        '''Get proxy by id'''
        if id is None:
            return False if only_check else None
        cur = self._db.execute('SELECT * FROM proxy WHERE id=?;', (id,))
        for i in cur:
            return True if only_check else (i[1], i[2])
        return False if only_check else None

    def get_proxy_list(self) -> List[str]:
        '''Get all available id in database'''
        r = []
        cur = self._db.execute('SELECT id FROM proxy;')
        for i in cur:
            r.append(i[0])
        return r
