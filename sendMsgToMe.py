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
from captcha2 import checkCaptcha2
from json import dumps
from constants import jsonsep as sep
from tep import getTemplate as getT, embScr
from telegram import sendMessage
from lang import (
    getLangFromAcceptLanguage as getlang,
    getdict,
    mapToDict,
    dictToJSON,
    getTranslator
)
from mycache import setCacheControl
from requests import post


class sendMsgToMe:
    def GET(self):
        te = getT("sendMsgToMe.html")
        se = settings()
        se.ReadSettings()
        sitekey = se.captcha2sitekey
        if te is None or sitekey is None:
            web.HTTPError('500 Internal Server Error')
            return 'Error'
        lan = getlang()
        i18n = getdict('basic', lan)
        i18n2 = getdict('sendMsgToMe', lan)
        i18n3 = {}
        mapToDict(i18n2, i18n3, ['OK', 'FAILED', 'NEEDCON', 'NEEDN'])
        mapToDict(i18n, i18n3, ['NETERR', 'RECAP2'])
        i18n3 = dictToJSON(i18n3)
        trans = getTranslator(basic=i18n, sendMsgToMe=i18n2)
        web.header('Content-Language', lan)
        if web.input().get('hl') is None:
            web.header('Vary', 'Accept-Language')
        if se.webpageCacheTime is not None:
            setCacheControl(se.webpageCacheTime)
        return te(sitekey, lan, i18n, i18n2, i18n3, embScr, trans)

    def POST(self):
        se = settings()
        se.ReadSettings()
        lan = getlang()
        web.header('Content-Language', lan)
        web.header('Content-Type', 'application/json; charset=UTF-8')
        i18n = getdict('sendMsgToMe', lan)
        inp = web.input()
        content = inp.get("content")
        if content is None or len(content) == 0:
            inf = {'code': -3, 'msg': i18n['NEEDCON']}
            return dumps(inf, ensure_ascii=False, separators=sep)
        name = inp.get("name")
        if name is None or len(name) == 0:
            inf = {'code': -4, 'msg': i18n['NEEDN']}
            return dumps(inf, ensure_ascii=False, separators=sep)
        checked, info = checkCaptcha2()
        inf = {}
        inf['code'] = 0 if checked else -1
        if se.debug:
            inf['debugInfo'] = info
        if not checked:
            inf['msg'] = info['msg']
        if checked:
            try:
                ip = web.ctx['ip']
                if ip is None:
                    ip = ''
            except:
                ip = ''
            ilan = web.input().get("lan")
            if ilan is None:
                ilan = 'Unknown'
            addt = f' ({ilan})' if ip == '' else f' ({ip}, {ilan})'
            if se.sendMsgToMeUseEveryPush:
                if se.everyPushServer is None:
                    inf['code'] = -2
                    if se.debug:
                        inf['debugInfo2'] = {'code': -1,
                                             'msg': 'No EveryPush Server.'}
                elif se.everyPushToken is None:
                    inf['code'] = -2
                    if se.debug:
                        inf['debugInfo2'] = {'code': -2,
                                             'msg': 'No EveryPush Token.'}
                else:
                    server = se.everyPushServer
                    token = se.everyPushToken
                    re = post(f"{server}/message/push",
                              {"pushToken": token, "title": f"{name}{addt}",
                               "text": content})
                    info['code'] = 0 if re.ok else -4
                    if not re.ok:
                        try:
                            info['msg'] = re.json()['message']
                            if se.debug:
                                info['debugInfo2'] = re.json()
                        except Exception:
                            info['msg'] = "Failed to get message."
            elif se.telegramchatid is None:
                inf['code'] = -2
                if se.debug:
                    inf['debugInfo2'] = {'code': -1, 'msg': 'No Chat Id.'}
            else:
                text = f"{name}{addt}: {content}"
                sended, info = sendMessage(se.telegramchatid, text)
                inf['code'] = 0 if sended else -4
                if not sended:
                    inf['msg'] = info['msg']
                if se.debug:
                    inf['debugInfo2'] = info
        return dumps(inf, ensure_ascii=False, separators=sep)


if m:
    application = web.application((".*", "sendMsgToMe"), globals()).wsgifunc()
