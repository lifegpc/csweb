import web
import sys
from os.path import dirname, abspath


def getAbspath():
    dn = dirname(__file__)
    if dn == "":
        dn = "../"
    else:
        dn += "/../"
    return abspath(dn)


if getAbspath() not in sys.path:
    from os import chdir
    chdir(getAbspath())
    sys.path.append(getAbspath())
    m = True
else:
    m = False


class index:
    def GET(self, t):
        return 'LOL'


if m:
    application = web.application(('(/.*)', 'index'), globals()).wsgifunc()
