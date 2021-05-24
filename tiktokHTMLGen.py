from RSSGenerator import RSSItem
from typing import List
from html import escape
from tiktokRSSP import genUrl
from settings import settings


def escapeQuote(s: str) -> str:
    return s.replace('"', '\\"')


def genItemList(username: str, d: dict, li: list, typ: int) -> List[RSSItem]:
    s = settings()
    s.ReadSettings()
    ser = s.RSSProxySerects
    r = []
    for i in li:
        t = RSSItem(typ)
        url = f"https://www.tiktok.com/@{username}/video/{i['id']}"
        t.link = url
        t.author = i['author']['nickname']
        t.guid = url
        t.comments = url
        desc = escape(i['desc'])
        vurl = None
        for k in ['downloadAddr', 'playAddr']:
            if k in i['video']:
                if i['video'][k] is not None:
                    vurl = i['video'][k]
                    break
        cover = None
        for k in ['originCover', 'reflowCover']:
            if k in i['video']:
                cover = i['video'][k]
                break
        if vurl is not None:
            vurl = genUrl(vurl, ser, d, "https://www.tiktok.com/")
        if cover is not None:
            cover = genUrl(cover, ser)
        if vurl is not None:
            p = f' poster="{escapeQuote(cover)}"' if cover is not None else ''
            desc += f'<video src="{escapeQuote(vurl)}"{p} controls="controls">'
        t.description = desc
        r.append(t)
    return r
