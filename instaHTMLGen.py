from RSSGenerator import RSSItem
from typing import List
from html import escape, unescape


def escapeQuote(s: str) -> str:
    return s.replace('"', '\\"')


def getText(d: dict) -> str:
    if 'edge_media_to_caption' in d:
        c = d['edge_media_to_caption']
        if c is not None and 'edges' in c:
            edges = c['edges']
            if edges is not None and isinstance(edges, list):
                r = ''
                for i in edges:
                    if 'node' in i:
                        n = i['node']
                        if n is not None:
                            if 'text' in n:
                                r += n['text']
                            else:
                                raise ValueError("Unknown node.")
                r = escape(r)
                r = r.replace('\r\n', '\n')
                return r.replace('\n', '<br>')
    return ''


def dealWithSingleEdge(d: dict) -> str:
    if 'node' in d:
        n = d['node']
        if n is not None:
            tn = n['__typename']
            if tn == 'GraphVideo':
                dp = None
                if 'display_url' in n:
                    dp = n['display_url']
                alt = None
                if 'accessibility_caption' in n:
                    alt = n['accessibility_caption']
                p = f' poster="{escapeQuote(dp)}"' if dp is not None else ''
                p2 = f' alt="{escapeQuote(alt)}"' if alt is not None else ''
                return f'<video src="{escapeQuote(n["video_url"])}"{p}{p2}>'
            elif tn == 'GraphImage':
                alt = None
                if 'accessibility_caption' in n:
                    alt = n['accessibility_caption']
                p = f' alt="{escapeQuote(alt)}"' if alt is not None else ''
                return f'<img src="{escapeQuote(n["display_url"])}" width="{n["dimensions"]["width"]}" height="{n["dimensions"]["height"]}"{p}>'  # noqa: E501
            else:
                raise ValueError('Unknown Type.')
    return ''


def dealWithNode(d: dict, typ: int) -> RSSItem:
    if 'node' in d:
        n = d['node']
        if n is not None:
            tn = n['__typename']
            t = desc = getText(n)
            if t == '':
                if 'title' in n and n['title'] is not None:
                    t = desc = escape(n['title'])
            if tn == 'GraphImage' or tn == "GraphVideo":
                desc += dealWithSingleEdge(d)
            elif tn == "GraphSidecar":
                if 'edge_sidecar_to_children' in n:
                    c = n['edge_sidecar_to_children']
                    if c is not None and 'edges':
                        ce = c['edges']
                        if ce is not None and isinstance(ce, list):
                            for i in ce:
                                desc += dealWithSingleEdge(i)
            else:
                raise ValueError("Unkown Type.")
            r = RSSItem(typ)
            if 'product_type' in n and n['product_type'] == 'igtv':
                url = f"https://www.instagram.com/tv/{n['shortcode']}/"
            else:
                url = f"https://www.instagram.com/p/{n['shortcode']}/"
            r.link = url
            r.comments = url
            r.guid = url
            r.description = desc
            ti = unescape(t.split('<br>')[0])
            if len(ti) > 50:
                r.title = ti[:47] + '...'
            else:
                r.title = ti
            r.pubDate = n['taken_at_timestamp']
            return r


def genItemList(d: dict, typ: int) -> List[RSSItem]:
    rl = []
    for i in ['edge_owner_to_timeline_media', 'edge_felix_video_timeline',
              'edge_user_to_photos_of_you']:
        if i in d:
            tl = d[i]
            if tl is not None and 'edges' in tl:
                edges = tl['edges']
                if edges is not None and isinstance(edges, list):
                    for k in edges:
                        r = dealWithNode(k, typ)
                        if r is not None:
                            rl.append(r)
    return rl
