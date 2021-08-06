import sys
from yaml import load as loadyaml, CSafeLoader
from typing import Dict, Any, List
from json import dumps
from os.path import exists
from traceback import print_exc
from subprocess import Popen
from requests import Session
from time import sleep
from os import remove


class main():
    VAILD_LEVELS = ['error', 'warning']
    VALID_NEEDS = ['server', 'settings']

    def __init__(self):
        self._server = None
        self._ses = Session()
        self._ses.trust_env = False
        self._settings = []

    def backupSettings(self):
        if exists('settings.json'):
            with open('settings.json', 'r', encoding='UTF-8') as f:
                self._settings.append(f.read())
            remove('settings.json')

    def checkServer(self) -> bool:
        try:
            r = self._ses.get('http://127.0.0.1:2600/')
            return False if r.status_code >= 400 else True
        except Exception:
            return False

    def checkTest(self, test: Dict[str, Any]):
        if 'name' not in test or test['name'] is None or not isinstance(
                test['name'], str) or test['name'] == '':
            raise ValueError(f'Test must have a vaild name: {dumps(test)}')
        if 'level' not in test or test['level'] is None:
            test['level'] = 'error'
        if not isinstance(test['level'],
                          str) or test['level'] not in self.VAILD_LEVELS:
            raise ValueError(f"Test don't have a vaild level: {dumps(test)}" + '\n' + f"All vaild levels: {', '.join(self.VAILD_LEVELS)}")  # noqa: E501
        if 'test_file' not in test or test['test_file'] is None or not isinstance(test['test_file'], str) or test['test_file'] == '':  # noqa: E501
            raise ValueError(
                f'Test must have a vaild test_file: {dumps(test)}')
        if not exists(f"tests/{test['test_file']}"):
            raise ValueError(f"Can not find file: {dumps(test)}")
        self.get_needs(test)

    def get_needs(self, test: Dict[str, Any]) -> List[str]:
        if 'needs' not in test or test['needs'] is None:
            return None
        if isinstance(test['needs'], str):
            s = test['needs']
            if s in self.VALID_NEEDS:
                return [s]
        elif isinstance(test['needs'], list):
            ok = True
            for i in test['needs']:
                if i not in self.VALID_NEEDS:
                    ok = False
            if ok:
                return test['needs']
        raise ValueError(f"Test don't have a vaild needs: {dumps(test)}" + '\n' + f"All vaild needs: {', '.join(self.VALID_NEEDS)}")  # noqa: E501

    def kill_server(self):
        if self._server is None:
            return
        if self._server.poll() is None:
            print('Kill server')
            self._server.kill()

    def removeSettings(self):
        try:
            if exists('settings.json'):
                remove('settings.json')
        except:
            pass

    def restoreSettings(self):
        try:
            s = self._settings.pop()
            if s is not None:
                with open('settings.json', 'w', encoding='UTF-8') as f:
                    f.write(s)
            else:
                self.removeSettings()
        except Exception:
            self.removeSettings()

    def run(self) -> int:
        self.tests = loadyaml(open('tests.yaml', 'r', encoding='UTF-8'),
                              CSafeLoader)
        for test in self.tests:
            self.checkTest(test)
        err_num = 0
        warn_num = 0
        suc = 0
        fail = 0
        self.start_server()
        for test in self.tests:
            if self.run_test(test):
                suc += 1
            else:
                fail += 1
                if test['level'] == 'warning':
                    warn_num += 1
                else:
                    err_num += 1
        self.kill_server()
        pt = f'Run {suc + fail} tests, {suc} successed, {fail} failed.'
        if fail != 0:
            pt += f' ({warn_num} Warnings, {err_num} Errors)'
        print(pt)
        return 0 if err_num == 0 else 1

    def run_test(self, test: Dict[str, Any]) -> bool:
        store_settings = False
        with open(f"tests/{test['test_file']}", 'r', encoding='UTF-8') as f:
            t = f.read()
        try:
            print(f"Run {test['name']} (tests/{test['test_file']})")
            ns = self.get_needs(test)
            if ns:
                if 'server' in ns:
                    if not self.checkServer():
                        r = self.wait_server()
                        if r is False:
                            return False
                if 'settings' in ns:
                    self.backupSettings()
                    store_settings = True
            exec(t, {}, {})
            if store_settings:
                self.restoreSettings()
            return True
        except Exception:
            print_exc()
            if store_settings:
                self.restoreSettings()
            return False

    def start_server(self) -> bool:
        if self._server is not None:
            return False
        print('Try start server')
        self._server = Popen([sys.executable, 'start.py'])

    def wait_server(self):
        print('Wait server started')
        r = self._server.poll()
        if r is not None:
            print(f'Server process already exited with {r}')
            return False
        r = self.checkServer()
        while not r:
            sleep(1)
            r = self.checkServer()
        return True


if __name__ == '__main__':
    try:
        m = main()
        sys.exit(m.run())
    except Exception:
        print_exc()
        sys.exit(1)
