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
        if t != '/':
            web.HTTPError('301 Moved Permanently')
            web.header('Location', 'https://www.google.com/teapot')
            return '你是傻逼吗？祝你🐴早死早超生！'
        return "Hello World!"


if m:
    application = web.application(('(/.*)', 'hello'), globals()).wsgifunc()
