import web
from settings import settings
from captcha2 import checkCaptcha2
from json import dumps
from constants import jsonsep as sep
from tep import getTemplate as getT
from telegram import sendMessage


class sendMsgToMe:
    def GET(self):
        te = getT("sendMsgToMe.html")
        se = settings()
        se.ReadSettings()
        sitekey = se.captcha2sitekey
        if te is None or sitekey is None:
            return 'Error'
        return te(sitekey)

    def POST(self):
        se = settings()
        se.ReadSettings()
        content = web.input().get("content")
        if content is None or len(content) == 0:
            inf = {'code': -3, 'msg': 'No content.'}
            return dumps(inf, ensure_ascii=False, separators=sep)
        checked, info = checkCaptcha2()
        inf = {}
        inf['code'] = 0 if checked else -1
        if se.debug:
            inf['debugInfo'] = info
        if checked:
            if se.telegramchatid is None:
                inf['code'] = -2
                inf['debugInfo2'] = {'code': -1, 'msg': 'No Chat Id.'}
            else:
                sended, info = sendMessage(se.telegramchatid, content)
                inf['code'] = 0 if sended else -4
                if se.debug:
                    inf['debugInfo2'] = info
        return dumps(inf, ensure_ascii=False, separators=sep)
