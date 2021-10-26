import sys
from os.path import dirname, abspath
if True:
    from os import chdir
    chdir(abspath(dirname(__file__)))
    sys.path.append(abspath("."))
    sys.path.append(abspath('proxy'))
    sys.path.append(abspath('tools'))
    sys.path.append(abspath('pixiv'))
import web
from index import hello  # noqa: F401
from cfwProfile import CfwProfile  # noqa: F401
from clearurl import ClearUrl  # noqa: F401
from drawBagel import DrawBagel  # noqa: F401
from salt import Salt  # noqa: F401
from sendMsgToMe import sendMsgToMe  # noqa: F401
from instaRSS import InstaRSS  # noqa: F401
from instaVerify import InstaVerify  # noqa: F401
from notiAPI import NotiAPI  # noqa: F401
from RSSProxy import RSSProxy  # noqa: F401
from tiktokRSS import TiktokRSS  # noqa: F401
from proxy.add import ProxyAdd  # noqa: F401
from proxy.delete import ProxyDelete  # noqa: F401
from proxy.deleteAll import ProxyDeleteAll  # noqa: F401
from proxy.exists import ProxyExists  # noqa: F401
from proxy.gen import ProxyGen  # noqa: F401
from proxy.get import ProxyGet  # noqa: F401
from proxy.list import ProxyList  # noqa: F401
from proxy.proxy import ProxyProxy  # noqa: F401
from about import About  # noqa: F401
from tools.clearBlankLines import ClearBlankLines  # noqa: F401
from pixiv.pixivrss import PixivRSS  # noqa: F401


urls = (
    '^/cfwProfile$', 'CfwProfile',
    '^/clearUrl$', 'ClearUrl',
    '^/drawBagel$', 'DrawBagel',
    '^/instaRSS$', 'InstaRSS',
    '^/instaVerify$', 'InstaVerify',
    '^/RSSProxy', 'RSSProxy',
    '^/salt$', 'Salt',
    '^/sendMsgToMe$', 'sendMsgToMe',
    '^/tiktokRSS$', 'TiktokRSS',
    '^/notiAPI$', 'NotiAPI',
    '^/proxy/add$', 'ProxyAdd',
    '^/proxy/delete$', 'ProxyDelete',
    '^/proxy/deleteAll$', 'ProxyDeleteAll',
    '^/proxy/exists$', 'ProxyExists',
    '^/proxy/gen$', 'ProxyGen',
    '^/proxy/get$', 'ProxyGet',
    '^/proxy/list$', 'ProxyList',
    '^/proxy/proxy$', 'ProxyProxy',
    '^/about', 'About',
    '^/tools/clearBlankLines$', 'ClearBlankLines',
    '^/pixiv/rss$', 'PixivRSS',
    '(/.*)', 'hello',
)


class mywebapp(web.application):
    def run(self, host: str = "127.0.0.1", port: int = 2600, *middleware):
        "重写方法以支持指定host和port"
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (host, port))


if __name__ == "__main__":
    try:
        app = mywebapp(urls, globals())
        k = {}
        if len(sys.argv) >= 3:
            k['host'] = sys.argv[1]
            k['port'] = int(sys.argv[2])
        app.run(**k)
    except:
        from traceback import format_exc
        format_exc()
        sys.exit(1)
