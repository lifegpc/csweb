import sys
import web
from os import chdir
from os.path import dirname, abspath
app_path = dirname(__file__)
if app_path:
    chdir(app_path)
sys.path.append(abspath("."))
from sendMsgToMe import sendMsgToMe  # noqa: F401, E402

urls = (
    '/sendMsgToMe', 'sendMsgToMe',
    '(/.*)', 'hello',
)


class hello:
    def GET(self, t):
        return "Hello World!"


application = web.application(urls, globals()).wsgifunc()
