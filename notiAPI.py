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
from settings import settings
from json import loads
from telegram import sendMessage
from html import escape
from textc import textc
from constants import ISO8601_FORMAT
from time import strftime, gmtime
from sign import verifySign


class NotiAPI:
    def POST(self):
        s = settings()
        s.ReadSettings()
        if s.notiAPISecrets is not None:
            if not verifySign(s.notiAPISecrets, True):
                web.HTTPError('401 Unauthorized')
                return ''
        ignore_ongoing = web.input().get("io", True)
        data = web.data()
        if isinstance(data, bytes):
            d = data.decode('UTF-8')
        elif isinstance(data, str):
            d = data
        else:
            web.HTTPError('500 Internal Server Error')
            return ''
        j = loads(d)
        mes = textc()
        if ignore_ongoing and 'ongoing' in j and j['ongoing']:
            return ''
        if 'app_name' in j:
            if 'package_name' in j:
                pn = j['package_name']
                mes.addtotext(f"<b>{escape(j['app_name'])} ({escape(pn)})</b>")
            else:
                mes.addtotext(f"<b>{escape(j['app_name'])}</b>")
        if 'title' in j:
            mes.addtotext(f"<b>{escape(j['title'])}</b>")
        if 'text' in j:
            mes.addtotext(escape(j['text']))
        mes.addtotext(strftime(ISO8601_FORMAT, gmtime(j['when'] / 1000)))
        while len(mes):
            sendMessage(s.notiAPITelegraBotChatId, mes.tostr(),
                        s.notiAPITelegramBotAPIKey, 'HTML', True)
        return ''


if m:
    application = web.application((".*", "NotiAPI"), globals()).wsgifunc()
