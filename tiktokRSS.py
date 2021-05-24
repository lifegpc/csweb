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
from traceback import format_exc
from tiktokAPI import TiktokAPI
from constants import jsonsep
from json import dumps
from tiktokDatabase import TiktokDatabase
from mycache import sendCacheInfo
from sign import verifySign
from urllib.parse import urlencode


VIDEO_CACHE_TIME = 360


class TiktokRSS:
    def GET(self):
        try:
            s = settings()
            s.ReadSettings()
            if s.tiktokRSSSecrets and not verifySign(s.tiktokRSSSecrets):
                web.HTTPError('401 Unauthorized')
                return ''
            t = TiktokAPI()
            user = web.input().get("u")
            if user is None or user == '':
                user = web.input().get("user")
            typ = web.input().get("t")
            if typ is None or typ not in ['rss', 'json', 'atom', 'url']:
                typ = web.input().get("type")
            if typ is None or typ not in ['rss', 'json', 'atom', 'url']:
                typ = 'rss'
            videoid = web.input().get("vid")
            if videoid is None or videoid == '':
                videoid = web.input().get("videoid")
            contain_id = web.input().get("cid")
            if contain_id is None:
                contain_id = web.input().get("contain_id")
            contain_id = contain_id is not None
            db = TiktokDatabase()
            cacheTime = 15
            if videoid is not None:
                ld = f'/video/{videoid}'
                vdata = db.get_cache(ld, VIDEO_CACHE_TIME)
                if vdata is None:
                    vdata = t.get_video(videoid, user)
                    if vdata is None or vdata['statusCode'] != 0:
                        raise Exception("Can not parse video info.")
                    c = db.save_cache(ld, vdata)
                else:
                    c = vdata[1]
                    vdata = vdata[0]
                sendCacheInfo(VIDEO_CACHE_TIME * 60, c)
                if typ == 'json':
                    web.header("Content-Type",
                               "application/json; charset=UTF-8")
                    return dumps(vdata, ensure_ascii=False,
                                 separators=jsonsep)
                elif typ == 'url':
                    vurl = None
                    i = vdata['itemInfo']['itemStruct']
                    for k in ['downloadAddr', 'playAddr']:
                        if k in i['video']:
                            if i['video'][k] is not None:
                                vurl = i['video'][k]
                                break
                    if vurl is None:
                        raise ValueError('Can not find play url.')
                    if s.RSSProxySerects is None:
                        raise ValueError(
                            'RSSProxySerects is needed in settings.')
                    from tiktokRSSP import genUrl
                    vurl = genUrl(vurl, s.RSSProxySerects, vdata,
                                  "https://www.tiktok.com/")
                    web.HTTPError('302 FOUND')
                    web.header('Location', vurl)
                    return ''
                raise Exception('Other Type is not supported.')
            elif user is not None:
                ld = f'/user/{user}'
                udata = db.get_cache(ld, cacheTime)
                new_cache = False
                if udata is None:
                    udata = t.get_user(user)
                    if udata is None or udata['statusCode'] != 0:
                        raise Exception("Can not parse user info.")
                    c = db.save_cache(ld, udata)
                    new_cache = True
                else:
                    c = udata[1]
                    udata = udata[0]
                sendCacheInfo(cacheTime * 60, c)
                if typ == 'json':
                    web.header("Content-Type",
                               "application/json; charset=UTF-8")
                    return dumps(udata, ensure_ascii=False, separators=jsonsep)
                elif typ == 'rss':
                    r = None
                    if s.tiktokCacheRSS and not new_cache:
                        d = {"contain_id": str(contain_id)}
                        ldd2 = f"user/{user}/rss?" + urlencode(d)
                        r = db.get_cache(ldd2, cacheTime)
                        if r is not None:
                            r = r[0]
                    if r is None:
                        from RSSGenerator import RSSGen, RSS2_TYPE
                        from tiktokHTMLGen import genItemList
                        g = RSSGen(RSS2_TYPE)
                        u = udata['userInfo']['user']
                        ti = f"Tiktok {u['nickname']}(@{u['uniqueId']}"
                        ti += f", {u['id']})" if contain_id else ')'
                        g.meta.title = ti
                        g.meta.link = f"https://www.tiktok.com/@{user}"
                        g.meta.description = u['signature']
                        g.meta.image = u['avatarLarger']
                        g.meta.lastBuildDate = c / 1E9
                        g.meta.ttl = cacheTime
                        g.list = genItemList(user, udata, udata['items'],
                                             RSS2_TYPE)
                        r = g.generate()
                        if s.tiktokCacheRSS:
                            db.save_cache(ldd2, r)
                    web.header("Content-Type",
                               "application/xml; charset=UTF-8")
                    return r
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
    application = web.application((".*", "TiktokRSS"), globals()).wsgifunc()
