from typing import List, Tuple
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, ParseResult


def genLangLink(default: str, langs: List[str] = None, pages:
                List[Tuple[str, str]] = None):
    try:
        if default is None:
            return ''
        e = ET.Element('link', {'rel': 'alternate', 'hreflang': 'x-default',
                                'href': default})
        b: bytes = ET.tostring(e, encoding='UTF-8')
        if langs is not None:
            for lan in langs:
                tlan = lan.replace('_', '-')
                tlan2 = lan.replace('-', '_')
                r = urlparse(default)
                pl = parse_qs(r.query)
                pl['hl'] = tlan2
                r = ParseResult(r.scheme, r.netloc, r.path, r.params,
                                urlencode(pl, doseq=True), r.fragment)
                href = urlunparse(r)
                e = ET.Element('link', {'rel': 'alternate', 'hreflang': tlan,
                                        'href': href})
                b += ET.tostring(e, encoding='UTF-8')
        if pages is not None:
            for i in pages:
                tlan = i[0].replace('_', '-')
                e = ET.Element('link', {'rel': 'alternate', 'hreflang': tlan,
                                        'href': i[1]})
                b += ET.tostring(e, encoding='UTF-8')
        return b.decode('UTF-8')
    except:
        from traceback import format_exc
        from settings import settings
        try:
            s = settings()
            s.ReadSettings()
            if s.debug:
                return f'<!--{format_exc()}-->'
            return ''
        except:
            return ''
