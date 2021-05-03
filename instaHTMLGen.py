from RSSGenerator import RSSItem
from typing import List


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
            if tn == 'GraphImage' or tn == "GraphVideo":
                desc += dealWithSingleEdge(n)
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
            url = f"https://www.instagram.com/p/{n['shortcode']}/"
            r.link = url
            r.comments = url
            r.guid = url
            r.description = desc
            ti = t.split('<br>')[0]
            if len(ti) > 20:
                r.title = ti[:17] + '...'
            else:
                r.title = ti
            r.pubDate = n['taken_at_timestamp']
            return r


def genItemList(d: dict, typ: int) -> List[RSSItem]:
    rl = []
    if 'edge_owner_to_timeline_media' in d:
        tl = d['edge_owner_to_timeline_media']
        if tl is not None and 'edges' in tl:
            edges = tl['edges']
            if edges is not None and isinstance(edges, list):
                for i in edges:
                    r = dealWithNode(i, typ)
                    if r is not None:
                        rl.append(r)
    return rl
