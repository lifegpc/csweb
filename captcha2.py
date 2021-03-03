import web
from requests import Session
from settings import settings
from lang import getLangFromAcceptLanguage as getlang, getdict, LanDict


def checkCaptcha2(i18n: LanDict = None) -> (bool, dict):
    """判断验证是否通过"""
    if i18n is None:
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
        return False, {'code': -2, 'msg': 'No sercet key to verify reCAPTCHA.\n' + i18n['SITEERR']}  # noqa: E501
    data = {'secret': sercet, 'response': rekey}
    url = "https://www.recaptcha.net/recaptcha/api/siteverify"
    re = r.post(url, data=data)
    re = re.json()
    if re['success']:
        return True, {'code': 0, 'result': re}
    else:
        return False, {'code': -3, 'msg': i18n['RECAP2VE'], 'info': re}
