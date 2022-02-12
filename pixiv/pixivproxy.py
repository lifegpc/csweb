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
from urllib.parse import unquote_plus, urlencode
from typing import List
from hashl import sha512
from pixivdb import PixivDb
from pixivapi import PixivAPI
from json import dumps
from constants import jsonsep
from mycache import sendCacheInfo
from pixivrssp import genUrl


def verifySign(sercet: str, query: List[str]):
    sign = None
    q = ''
    for i in query:
        if i.startswith('sign='):
            sign = i[5:]
        else:
            if q == '':
                q = i
            else:
                q += '/' + i
    if sign is None:
        return False
    return sha512(sercet + q) == sign


def parseBool(inp: str, default: bool) -> bool:
    if inp is None or inp == '':
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


def getUrl(d: dict, s: str = 'original'):
    if s == 'original':
        if 'meta_single_page' in d:
            m = d['meta_single_page']
            if 'original_image_url' in m:
                return m['original_image_url']
        elif 'original_image_url' in d:
            return d['original_image_url']
    if 'image_urls' in d:
        if s in d['image_urls']:
            return d['image_urls'][s]


class PixivProxy:
    def GET(self, *k):
        try:
            web.header('Access-Control-Allow-Origin', '*')
            s = settings()
            s.ReadSettings()
            if len(k) == 0:
                web.HTTPError('400 Bad Request')
                return '400 Bad Request'
            args = k[0].split('/')
            if s.pixivRSSSecrets and not verifySign(s.pixivRSSSecrets, args):
                web.HTTPError('401 Unauthorized')
                return '401 Unauthorized'
            m = {}
            for i in args:
                d = unquote_plus(i).split('=', 1)
                if len(d) == 1:
                    continue
                m[d[0]] = d[1]
            id = m.get('id', '')
            typ = m.get('t', '')
            if typ == '':
                m.get('type', '')
            if typ == '':
                typ = 'url'
            if id == '':
                web.HTTPError('400 Bad Request')
                return '400 Bad Request: id is needed.'
            db = PixivDb()
            p = PixivAPI(s, db)
            lang = m.get('lang', None)
            lld = {}
            if lang is not None:
                lld['lang'] = lld
            ld = f"/illust/{id}?{urlencode(lld)}"
            d = db.get_cache(ld, s.pixivSinglePageCacheTime)
            if d is None:
                d = p.getIllustDetails(id, lang)
                lt = db.save_cache(ld, d)
            else:
                lt = d[1]
                d = d[0]
            sendCacheInfo(60 * s.pixivSinglePageCacheTime, lt)
            if typ == 'json':
                web.header("Content-Type", "application/json; charset=utf-8")
                return dumps(d, ensure_ascii=False, separators=jsonsep)
            page = m.get('p', '')
            if page == '':
                page = m.get('page', '1')
            page = min(max(int(page), 1), d['page_count'])
            add_fn = m.get('f', '')
            if add_fn == '':
                add_fn = m.get('add_fn', '')
            add_fn = parseBool(add_fn, True)
            if typ == 'url':
                if d['page_count'] == 1:
                    url = getUrl(d, m.get('size', 'original'))
                else:
                    url = getUrl(d['meta_pages'][page - 1], m.get('size', 'original'))  # noqa: E501
                if url is None:
                    web.HTTPError('404 Not Found')
                    return '404 Failed to extract url.'
                web.found(genUrl(url, s.RSSProxySerects, add_fn))
                return True
        except Exception:
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

    def POST(self, *k):
        self.GET(*k)

    def OPTIONS(self):
        from cors import allowCors
        allowCors()
        return ''


if m:
    application = web.application(("(.*)", "PixivProxy"), globals()).wsgifunc()
