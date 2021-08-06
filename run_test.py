import sys
from yaml import load as loadyaml, CSafeLoader
from typing import Dict, Any
from json import dumps
from os.path import exists
from traceback import print_exc


class main():
    VAILD_LEVELS = ['error', 'warning']

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

    def run(self) -> int:
        self.tests = loadyaml(open('tests.yaml', 'r', encoding='UTF-8'),
                              CSafeLoader)
        for test in self.tests:
            self.checkTest(test)
        err_num = 0
        warn_num = 0
        suc = 0
        fail = 0
        for test in self.tests:
            if self.run_test(test):
                suc += 1
            else:
                fail += 1
                if test['level'] == 'warning':
                    warn_num += 1
                else:
                    err_num += 1
        pt = f'Run {suc + fail} tests, {suc} successed, {fail} failed.'
        if fail != 0:
            pt += f' ({warn_num} Warnings, {err_num} Errors)'
        print(pt)
        return 0 if err_num == 0 else 1

    def run_test(self, test: Dict[str, Any]) -> bool:
        with open(f"tests/{test['test_file']}", 'r', encoding='UTF-8') as f:
            t = f.read()
        try:
            print(f"Run {test['name']} (tests/{test['test_file']})")
            exec(t, {}, {})
            return True
        except Exception:
            print_exc()
            return False


if __name__ == '__main__':
    try:
        m = main()
        sys.exit(m.run())
    except Exception:
        print_exc()
        sys.exit(1)
