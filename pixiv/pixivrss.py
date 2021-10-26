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
if m:
    sys.path.append('../')
from settings import settings
from traceback import format_exc
from pixivapi import PixivAPI
from pixivdb import PixivDb
from sign import verifySign
from mycache import sendCacheInfo
from json import dumps
from constants import jsonsep
from urllib.parse import urlencode


def parseBool(inp: str, default: bool) -> bool:
    if inp is None:
        return default
    lo = inp.lower()
    if lo == 'true':
        return True
    elif lo == 'false':
        return False
    try:
        i = int(lo)
        return bool(i)
    except Exception:
        pass
    return bool(inp)


class PixivRSS:
    def GET(self):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            s = settings()
            s.ReadSettings()
            if s.pixivRSSSecrets and not verifySign(s.pixivRSSSecrets):
                web.HTTPError('401 Unauthorized')
                return ''
            db = PixivDb()
            p = PixivAPI(s, db)
            user = web.input().get("u")
            if user is None or user == '':
                user = web.input().get("user")
            typ = web.input().get("t")
            if typ is None or typ not in ['rss', 'json', 'atom']:
                typ = web.input().get("type")
            if typ is None or typ not in ['rss', 'json', 'atom']:
                typ = 'rss'
            include_tags = False if web.input().get("include_tags") is None else True  # noqa: E501
            user_info = False if web.input().get("user_info") is None else True
            bookmarks = False if web.input().get("bookmarks") is None else True
            restrict = True if web.input().get("private") is None else False
            add_author_in_title = True if bookmarks else False
            add_author_in_title = parseBool(web.input().get("add_author_in_title"), add_author_in_title)  # noqa: E501
            if user is None:
                web.HTTPError('400 Bad Request')
                return 'User is needed.'
            if user is not None:
                uld = f'/user/detail/{user}'
                ld = f'/user/illusts/{user}'
                u = db.get_cache(uld, s.pixivCacheTime)
                new_cache = False
                if u is None:
                    u = p.getUserDetails(user)
                    if u is None:
                        raise Exception('Can not get user info.')
                    c = db.save_cache(uld, u)
                    new_cache = True
                else:
                    c = u[1]
                    u = u[0]
                if user_info:
                    if typ == 'json':
                        sendCacheInfo(60 * s.pixivCacheTime, c)
                        web.header("Content-Type",
                                   "application/json; charset=UTF-8")
                        return dumps(u, ensure_ascii=False, separators=jsonsep)
                    web.HTTPError('400 Bad Request')
                    return 'Type is not supported'
                if bookmarks:
                    d = {"restrict": restrict}
                    ld3 = f'/user/bookmarks/illusts/{user}?' + urlencode(d)
                    bk = db.get_cache(ld3, s.pixivCacheTime)
                    if bk is None:
                        bk = p.getBookmarks(user, restrict)
                        if bk is None:
                            raise Exception('Can not get bookmarks.')
                        c = db.save_cache(ld3, bk)
                        new_cache = True
                    else:
                        c = bk[1]
                        bk = bk[0]
                    ill = bk
                else:
                    ill = db.get_cache(ld, s.pixivCacheTime)
                    if ill is None:
                        ill = p.getIllusts(user)
                        if ill is None:
                            raise Exception("Can not get illusts")
                        c = db.save_cache(ld, ill)
                        new_cache = True
                    else:
                        c = ill[1]
                        ill = ill[0]
                sendCacheInfo(60 * s.pixivCacheTime, c)
                if typ == 'json':
                    web.header("Content-Type",
                               "application/json; charset=UTF-8")
                    return dumps(ill, ensure_ascii=False, separators=jsonsep)
                elif typ == 'rss':
                    if s.pixivCacheRSS:
                        d = {"include_tags": include_tags}
                        ld2 = f'/user/illusts/{user}/rss?' + urlencode(d)
                    r = None
                    if s.pixivCacheRSS and not new_cache:
                        r = db.get_cache(ld2, s.pixivCacheTime)
                        if r is not None:
                            r = r[0]
                    if r is None:
                        from RSSGenerator import RSSGen, RSS2_TYPE
                        from pixivHTMLGen import genRSSItems
                        from pixivrssp import genUrl
                        g = RSSGen(RSS2_TYPE)
                        ill = ill['illusts']
                        if not bookmarks:
                            g.meta.title = f"Pixiv {u['user']['name']}(@{u['user']['account']})'s illusts"  # noqa: E501
                        else:
                            g.meta.title = f"Pixiv {u['user']['name']}(@{u['user']['account']})'s bookmarks"  # noqa: E501
                            if not restrict:
                                g.meta.title += ' (private)'
                        g.meta.link = f"https://www.pixiv.net/users/{user}"
                        g.meta.description = u['user']['comment']
                        if g.meta.description is None:
                            g.meta.description = "This user don't have a comment."  # noqa: E501
                        img_url = u['profile']['background_image_url']
                        if img_url is not None:
                            g.meta.image = genUrl(img_url, s.RSSProxySerects)
                        g.meta.lastBuildDate = c / 1E9
                        g.meta.ttl = s.pixivCacheTime
                        g.list = genRSSItems(ill, s, RSS2_TYPE, include_tags,
                                             add_author_in_title)
                        r = g.generate()
                        if s.pixivCacheRSS:
                            db.save_cache(ld2, r)
                    web.header("Content-Type",
                               "application/xml; charset=UTF-8")
                    return r
        except:
            web.HTTPError('500 Internal Server Error')
            web.header("Content-Type", "text/plain; charset=UTF-8")
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    return format_exc()
            except:
                pass
            return ''


if m:
    application = web.application((".*", "PixivRSS"), globals()).wsgifunc()
