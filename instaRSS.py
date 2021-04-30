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
from instaAPI import InstaAPI, NeedVerifyError
from instaDatabase import InstaDatabase
from traceback import format_exc
from urllib.parse import urlencode


class InstaRSS:
    def GET(self):
        web.header("Content-Type", "application/json; charset=UTF-8")
        try:
            s = settings()
            s.ReadSettings()
            db = InstaDatabase()
            i = InstaAPI(db, s.instagramUsername, s.instagramPassword)
            user = web.input().get("user")
            if user is not None:
                idd = f"user/{user}/init"
                r = db.get_cache(idd)
                c = None
                if r is None:
                    r = i.get_user_info(user)
                    db.save_cache(idd, r)
                else:
                    c = r[1]
                    r = r[0]
                from json import dumps
                from constants import jsonsep
                return dumps(r, ensure_ascii=False, separators=jsonsep)
        except NeedVerifyError as e:
            z = [('gourl', web.ctx.path), ('sign', e.sign)]
            web.HTTPError('302 Found')
            web.header("Location", "/instaVerify?" + urlencode(z))
            return ''
        except:
            web.HTTPError('500 Internal Server Error')
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    return format_exc()
            except:
                pass
            return ''


if m:
    application = web.application((".*", "InstaRSS"), globals()).wsgifunc()
