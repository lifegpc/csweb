from RSSGenerator import RSSItem
from typing import List
from dateutil import parser
from html import escape
from pixivrssp import genUrl


def escapeQuote(s: str) -> str:
    return s.replace('"', '\\"')


def genImage(i: dict, ser: str):
    url = None
    if 'original_image_url' in i:
        url = i['original_image_url']
    if 'image_urls' in i:
        url = i['image_urls']['original']
    if url is None:
        return ''
    url = genUrl(url, ser)
    return f"<img src=\"{escapeQuote(url)}\" referrerpolicy=\"no-referrer\">"


def genRSSItems(li: list, s, typ, include_tags: bool) -> List[RSSItem]:
    rl = []
    for i in li:
        t = RSSItem(typ)
        t.title = i['title']
        t.link = f"https://www.pixiv.net/artworks/{i['id']}"
        t.comments = t.link
        t.guid = t.link
        des = ''
        if i['page_count'] > 1:
            for p in i['meta_pages']:
                des += genImage(p, s.RSSProxySerects)
        else:
            des += genImage(i['meta_single_page'], s.RSSProxySerects)
        if include_tags:
            tags = []
            if 'tags' in i:
                for t in i['tags']:
                    tags.append(f"#{t['name']}")
            des += '<br/>' + escape(' '.join(tags))
        des += '<br/>' + i['caption']
        t.description = des
        try:
            t.pubDate = parser.parse(i['create_date']).timestamp()
        except Exception:
            pass
        try:
            t.author = i['user']['name']
        except Exception:
            pass
        rl.append(t)
    return rl
