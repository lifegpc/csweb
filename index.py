import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
    m = True
else:
    m = False
import web


class hello:
    def GET(self, t):
        return "Hello World!"


if m:
    application = web.application(('(/.*)', 'hello'), globals()).wsgifunc()
