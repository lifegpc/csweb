import sys
from os.path import abspath
if abspath('tests/') not in sys.path:
    sys.path.append(abspath('tests/'))
from utils import DebugList, debug
from sign import genSign


dl = DebugList('sign.txt')
debug(genSign('thistest', {"test": ["test", "123"]}), dl=dl)
