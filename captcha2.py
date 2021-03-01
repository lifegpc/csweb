import web
from requests import Session
from settings import settings
from lang import getLangFromAcceptLanguage as getlang, getdict


def checkCaptcha2() -> (bool, dict):
    """判断验证是否通过"""
    lan = getlang()
    i18n = getdict('basic', lan)
    rekey = web.input().get("g-recaptcha-response")
    if rekey is None:
        return False, {'code': -1, 'msg': i18n['RECAP2']}
    r = Session()
    se = settings()
    se.ReadSettings()
    sercet = se.captcha2sercetkey
    if sercet is None:
        return False, {'code': -2, 'msg': 'No sercet key.'}
    data = {'secret': sercet, 'response': rekey}
    url = "https://www.recaptcha.net/recaptcha/api/siteverify"
    re = r.post(url, data=data)
    re = re.json()
    if re['success']:
        return True, {'code': 0, 'result': re}
    else:
        return False, {'code': -3, 'msg': 'siteverify failed.', 'info': re}
