import web
from settings import settings
from captcha2 import checkCaptcha2
from json import dumps
from constants import jsonsep as sep
from tep import getTemplate as getT, embScr
from telegram import sendMessage
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    mapToDict,
    dictToJSON
)


class sendMsgToMe:
    def GET(self):
        te = getT("sendMsgToMe.html")
        se = settings()
        se.ReadSettings()
        sitekey = se.captcha2sitekey
        if te is None or sitekey is None:
            return 'Error'
        lan = getlang()
        i18n = getdict('basic', lan)
        i18n2 = getdict('sendMsgToMe', lan)
        i18n3 = {}
        mapToDict(i18n2, i18n3, ['OK', 'FAILED'])
        mapToDict(i18n, i18n3, ['NETERR'])
        i18n3 = dictToJSON(i18n3)
        return te(sitekey, lan, i18n, i18n2, i18n3, embScr)

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
                if not sended:
                    inf['msg'] = info['msg']
                if se.debug:
                    inf['debugInfo2'] = info
        return dumps(inf, ensure_ascii=False, separators=sep)
