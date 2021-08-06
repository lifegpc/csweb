import sys
from os.path import abspath
if abspath('tests/') not in sys.path:
    sys.path.append(abspath('tests/'))
from utils import DebugList, debug
from hashl import sha512, sha256, md5


dl = DebugList('hashl.txt')
debug(sha512('test'), dl=dl)
debug(sha256('test'), dl=dl)
debug(md5('test'), dl=dl)
