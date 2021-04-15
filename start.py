import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
import web
from index import hello  # noqa: F401
from cfwProfile import CfwProfile  # noqa: F401
from clearurl import ClearUrl  # noqa: F401
from drawBagel import DrawBagel  # noqa: F401
from salt import Salt  # noqa: F401
from sendMsgToMe import sendMsgToMe  # noqa: F401


urls = (
    '^/cfwProfile', 'CfwProfile',
    '^/clearUrl', 'ClearUrl',
    '^/drawBagel', 'DrawBagel',
    '^/salt', 'Salt',
    '^/sendMsgToMe', 'sendMsgToMe',
    '(/.*)', 'hello',
)


class mywebapp(web.application):
    def run(self, host: str = "127.0.0.1", port: int = 2500, *middleware):
        "重写方法以支持指定host和port"
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (host, port))


if __name__ == "__main__":
    app = mywebapp(urls, globals())
    app.run()