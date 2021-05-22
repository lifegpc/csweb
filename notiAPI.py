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
        APP_NAME = 'filterbox.field.APP_NAME'
        PACKAGE_NAME = 'filterbox.field.PACKAGE_NAME'
        TITLE = 'android.title'
        TEXT = 'android.text'
        WHEN = 'filterbox.field.WHEN'
        if APP_NAME in j:
            if PACKAGE_NAME in j:
                pn = j[PACKAGE_NAME]
                mes.addtotext(f"<b>{escape(j[APP_NAME])} ({escape(pn)})</b>")
            else:
                mes.addtotext(f"<b>{escape(j[APP_NAME])}</b>")
        mes.addtotext(f"<b>{escape(j[TITLE])}</b>")
        mes.addtotext(escape(j[TEXT]))
        mes.addtotext(strftime(ISO8601_FORMAT, gmtime(j[WHEN] / 1000)))
        while len(mes):
            sendMessage(s.notiAPITelegraBotChatId, mes.tostr(),
                        s.notiAPITelegramBotAPIKey, 'HTML', True)
        return ''


if m:
    application = web.application((".*", "NotiAPI"), globals()).wsgifunc()
