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
from json import dumps
from constants import jsonsep
from sign import verifySign
from mycache import sendCacheInfo


class InstaRSS:
    def GET(self):
        try:
            s = settings()
            s.ReadSettings()
            if s.instagramRSSSecrets and not verifySign(s.instagramRSSSecrets):
                web.HTTPError('401 Unauthorized')
                return ''
            db = InstaDatabase()
            i = InstaAPI(db, s.instagramUsername, s.instagramPassword)
            user = web.input().get("u")
            if user is None or user == '':
                user = web.input().get("user")
            typ = web.input().get("t")
            if typ is None or typ not in ['rss', 'json', 'atom']:
                typ = web.input().get("type")
            if typ is None or typ not in ['rss', 'json', 'atom']:
                typ = 'rss'
            contain_id = web.input().get("cid")
            if contain_id is None:
                contain_id = web.input().get("contain_id")
            contain_id = contain_id is not None
            tagged = web.input().get("tagged")
            tagged = True if tagged is not None else False
            cacheTime = s.instagramCacheTime
            if user is not None:
                idd = f"user/{user}/init"
                r = db.get_cache(idd, cacheTime)
                new_cache = False
                if r is None:
                    i._get_init_csrftoken()
                    r = i.get_user_info(user)
                    c = db.save_cache(idd, r)
                    new_cache = True
                else:
                    c = r[1]
                    r = r[0]
                if tagged:
                    idd2 = f"user/{user}/tagged"
                    r2 = None
                    new_cache = False
                    r2 = db.get_cache(idd2, cacheTime)
                    if r2 is not None:
                        c = r2[1]
                        r2 = r2[0]
                    if r2 is None:
                        r2 = i.get_user_tagged(r['id'])
                        c = db.save_cache(idd2, r2)
                        new_cache = True
                    sendCacheInfo(cacheTime * 60, c)
                    if typ == "json":
                        web.header("Content-Type",
                                   "application/json; charset=UTF-8")
                        return dumps(r2, ensure_ascii=False,
                                     separators=jsonsep)
                    elif typ == "rss":
                        r3 = None
                        if s.isntagramCacheRSS and not new_cache:
                            d = {"contain_id": str(contain_id)}
                            idd3 = f"user/{user}/tagged/rss?" + urlencode(d)
                            r3 = db.get_cache(idd3, cacheTime)
                            if r3 is not None:
                                r3 = r3[0]
                        if r3 is None:
                            from RSSGenerator import RSSGen, RSS2_TYPE
                            from instaHTMLGen import genItemList
                            g = RSSGen(RSS2_TYPE)
                            if not contain_id:
                                ti = f"Instagram Tagged {r['full_name']}(@{r['username']})"  # noqa: E501
                            else:
                                ti = f"Instagram Tagged {r['full_name']}(@{r['username']}, {r['id']})"  # noqa: E501
                            g.meta.title = ti
                            url = f"https://www.instagram.com/{r['username']}/"
                            if 'external_url' in r:
                                te = r['external_url']
                                if te is not None and isinstance(te, str) and len(te):  # noqa: E501
                                    url = te
                            g.meta.link = url
                            g.meta.description = r['biography']
                            g.meta.image = r['profile_pic_url_hd']
                            g.meta.lastBuildDate = c / 1E9
                            g.meta.ttl = cacheTime
                            g.list = genItemList(r2, RSS2_TYPE)
                            r3 = g.generate()
                            if s.isntagramCacheRSS:
                                db.save_cache(idd3, r3)
                        web.header("Content-Type",
                                   "application/xml; charset=UTF-8")
                        return r3
                    return
                sendCacheInfo(cacheTime * 60, c)
                if typ == 'json':
                    web.header("Content-Type",
                               "application/json; charset=UTF-8")
                    return dumps(r, ensure_ascii=False, separators=jsonsep)
                elif typ == "rss":
                    r2 = None
                    if s.isntagramCacheRSS and not new_cache:
                        d = {"contain_id": str(contain_id)}
                        idd2 = f"user/{user}/rss?" + urlencode(d)
                        r2 = db.get_cache(idd2, cacheTime)
                        if r2 is not None:
                            r2 = r2[0]
                    if r2 is None:
                        from RSSGenerator import RSSGen, RSS2_TYPE
                        from instaHTMLGen import genItemList
                        g = RSSGen(RSS2_TYPE)
                        if not contain_id:
                            ti = f"Instagram {r['full_name']}(@{r['username']})"  # noqa: E501
                        else:
                            ti = f"Instagram {r['full_name']}(@{r['username']}, {r['id']})"  # noqa: E501
                        g.meta.title = ti
                        url = f"https://www.instagram.com/{r['username']}/"
                        if 'external_url' in r:
                            te = r['external_url']
                            if te is not None and isinstance(te, str) and len(te):  # noqa: E501
                                url = te
                        g.meta.link = url
                        g.meta.description = r['biography']
                        g.meta.image = r['profile_pic_url_hd']
                        g.meta.lastBuildDate = c / 1E9
                        g.meta.ttl = cacheTime
                        g.list = genItemList(r, RSS2_TYPE)
                        r2 = g.generate()
                        if s.isntagramCacheRSS:
                            db.save_cache(idd2, r2)
                    web.header("Content-Type",
                               "application/xml; charset=UTF-8")
                    return r2
        except NeedVerifyError as e:
            z = [('gourl', web.ctx.path), ('nc', e.sign)]
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
