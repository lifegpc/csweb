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


def genUgoira(i: dict, ser: str):
    import xml.etree.ElementTree as ET
    from json import dumps
    from constants import jsonsep
    u = ET.Element('ugoira')
    u.set('poster', genUrl(i['meta_single_page']['original_image_url'], ser))
    u.set('src', genUrl(i['ugoira_data']['originalSrc'], ser))
    u.set('frames', dumps(i['ugoira_data']['frames'], ensure_ascii=False,
                          separators=jsonsep))
    return ET.tostring(u, encoding='UTF8', method='html').decode()


def genRSSItems(li: list, s, typ, include_tags: bool,
                add_author_in_title: bool,
                enable_ugoira: bool) -> List[RSSItem]:
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
        if i['type'] == 'ugoira' and enable_ugoira:
            if 'ugoira_data' in i:
                des += genUgoira(i, s.RSSProxySerects)
            else:
                des += genImage(i['meta_single_page'], s.RSSProxySerects)
        else:
            if i['page_count'] > 1:
                for p in i['meta_pages']:
                    des += genImage(p, s.RSSProxySerects)
            else:
                des += genImage(i['meta_single_page'], s.RSSProxySerects)
        if include_tags:
            tags = []
            if 'illust_ai_type' in i:
                if i['illust_ai_type'] == 2:
                    tags.append("#AI")
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
