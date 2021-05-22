from settings import settings
from requests import Session
from constants import TELEGRAM_PARSE_MODE


def sendMessage(chatId: int, message: str, botkey: str = None,
                parseMode: str = None, disableWebPagePreview: bool = None) -> (
                    bool, dict):
    if botkey is None:
        se = settings()
        se.ReadSettings()
    key = se.telegrambotkey if botkey is None else botkey
    if key is None:
        return False, {'code': -1, 'msg': 'No Telegram Bot Key.'}
    r = Session()
    d = {"chat_id": chatId, "text": message}
    if parseMode in TELEGRAM_PARSE_MODE:
        d['parse_mode'] = parseMode
    if disableWebPagePreview:
        d['disable_web_page_preview'] = True
    re = r.post(f"https://api.telegram.org/bot{key}/sendMessage", d)
    re = re.json()
    if 'ok' in re and re['ok']:
        return True, {'code': 0, 'result': re}
    else:
        return True, {'code': -2, 'msg': 'send failed', 'info': re}
