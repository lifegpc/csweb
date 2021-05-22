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


def genUrl(origin: str, serects: str, f: callable, f2: callable,
           hd: str) -> str:
    url = f'{hd}/RSSProxy?'
    p = {'t': [origin]}
    h = f(serects, p)  # genSign
    url += f2([('t', origin), ('sign', h)])  # urlencode
    return url


def dealWithSingleEdge(d: dict, **kwargs) -> str:
    proxy = bool(kwargs.get("proxy"))
    if proxy:
        from sign import genSign
        from settings import settings
        from urllib.parse import urlencode
        import web
        s = settings()
        s.ReadSettings()
        if s.RSSProxySerects is None:
            raise ValueError('RSSProxySerects is needed in settings.')
        ser = s.RSSProxySerects
        hd = web.ctx.homedomain
    if 'node' in d:
        n = d['node']
        if n is not None:
            tn = n['__typename']
            if tn == 'GraphVideo':
                dp = None
                if 'display_url' in n:
                    dp = n['display_url']
                    if proxy:
                        dp = genUrl(dp, ser, genSign, urlencode, hd)
                alt = None
                if 'accessibility_caption' in n:
                    alt = n['accessibility_caption']
                p = f' poster="{escapeQuote(dp)}"' if dp is not None else ''
                p2 = f' alt="{escapeQuote(alt)}"' if alt is not None else ''
                vurl = n["video_url"]
                if proxy:
                    vurl = genUrl(vurl, ser, genSign, urlencode, hd)
                return f'<video src="{escapeQuote(vurl)}"{p}{p2}>'
            elif tn == 'GraphImage':
                alt = None
                if 'accessibility_caption' in n:
                    alt = n['accessibility_caption']
                p = f' alt="{escapeQuote(alt)}"' if alt is not None else ''
                durl = n["display_url"]
                if proxy:
                    durl = genUrl(durl, ser, genSign, urlencode, hd)
                return f'<img src="{escapeQuote(durl)}" width="{n["dimensions"]["width"]}" height="{n["dimensions"]["height"]}"{p} referrerpolicy="no-referrer">'  # noqa: E501
            else:
                raise ValueError('Unknown Type.')
    return ''


def dealWithNode(d: dict, typ: int, **kwargs) -> RSSItem:
    if 'node' in d:
        n = d['node']
        if n is not None:
            tn = n['__typename']
            t = desc = getText(n)
            if t == '':
                if 'title' in n and n['title'] is not None:
                    t = desc = escape(n['title'])
            if tn == 'GraphImage' or tn == "GraphVideo":
                desc += dealWithSingleEdge(d, **kwargs)
            elif tn == "GraphSidecar":
                if 'edge_sidecar_to_children' in n:
                    c = n['edge_sidecar_to_children']
                    if c is not None and 'edges':
                        ce = c['edges']
                        if ce is not None and isinstance(ce, list):
                            for i in ce:
                                desc += dealWithSingleEdge(i, **kwargs)
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


def genItemList(d: dict, typ: int, **kwargs) -> List[RSSItem]:
    rl = []
    for i in ['edge_owner_to_timeline_media', 'edge_felix_video_timeline',
              'edge_user_to_photos_of_you']:
        if i in d:
            tl = d[i]
            if tl is not None and 'edges' in tl:
                edges = tl['edges']
                if edges is not None and isinstance(edges, list):
                    for k in edges:
                        r = dealWithNode(k, typ, **kwargs)
                        if r is not None:
                            rl.append(r)
    return rl
