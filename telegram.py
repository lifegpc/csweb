from settings import settings
from requests import Session


def sendMessage(chatId: int, message: str) -> (bool, dict):
    se = settings()
    se.ReadSettings()
    key = se.telegrambotkey
    if key is None:
        return False, {'code': -1, 'msg': 'No Telegram Bot Key.'}
    r = Session()
    re = r.post(f"https://api.telegram.org/bot{key}/sendMessage", {
                "chat_id": chatId, "text": message})
    re = re.json()
    if 'ok' in re and re['ok']:
        return True, {'code': 0, 'result': re}
    else:
        return True, {'code': -2, 'msg': 'send failed', 'info': re}
