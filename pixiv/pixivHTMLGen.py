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


def genRSSItems(li: list, s, typ, include_tags: bool,
                add_author_in_title: bool) -> List[RSSItem]:
    rl = []
    for i in li:
        if not i['visible']:
            continue
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
                for tt in i['tags']:
                    tags.append(f"#{tt['name']}")
                    if tt['translated_name'] is not None:
                        tags.append(f"#{tt['translated_name']}")
            des += '<br/>' + escape(' '.join(tags))
        des += '<br/>' + i['caption']
        t.description = des
        try:
            t.pubDate = parser.parse(i['create_date']).timestamp()
        except Exception:
            pass
        try:
            t.author = i['user']['name']
            if add_author_in_title:
                t.title = t.title + f" (@{t.author})"
        except Exception:
            pass
        rl.append(t)
    return rl
