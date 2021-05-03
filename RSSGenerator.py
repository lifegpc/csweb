# RSS2.0 Specification: https://cyber.harvard.edu/rss/rss.html
# Atom Specification: https://tools.ietf.org/html/rfc4287
from urllib.parse import urlparse, urlunparse, ParseResult
from constants import GMT_FORMAT, ISO8601_FORMAT
from time import strftime, gmtime
from typing import Union
from functools import wraps
import xml.etree.ElementTree as ET


RSS2_TYPE = 1
ATOM_TYPE = 2
ET._original_serialize_xml = ET._serialize_xml


def serialize_xml_with_CDATA(write, elem, qnames, namespaces,
                             short_empty_elements, **kwargs):
    if elem.tag == 'CDATA':
        write("<![CDATA[{}]]>".format(elem.text))
        return
    return ET._original_serialize_xml(write, elem, qnames, namespaces,
                                      short_empty_elements, **kwargs)


ET._serialize_xml = ET._serialize['xml'] = serialize_xml_with_CDATA


def CDATA(text):
    element = ET.Element("CDATA")
    element.text = text
    return element


class RSSTypeError(Exception):
    def __init__(self, typ: int = None):
        if typ is None or typ < RSS2_TYPE or typ > ATOM_TYPE:
            Exception.__init__(self, "Type Error: Unknown Type.")
        else:
            d = {1: 'RSS2', 2: 'ATOM'}
            Exception.__init__(self, f'Type Error: Type must be {d[typ]}.')


class RSSAttrRequired(Exception):
    def __init__(self, text: str):
        Exception.__init__(self, f'"{text}" is needed.')


def rss2Required(func):
    @wraps(func)
    def o(*args, **kwargs):
        if args[0]._type != RSS2_TYPE:
            raise RSSTypeError(RSS2_TYPE)
        return func(*args, **kwargs)
    return o


class RSSBasic:
    def __init__(self, typ):
        self._data = {}
        self.category = []
        if typ >= RSS2_TYPE and typ <= ATOM_TYPE:
            self._type = typ
        else:
            raise RSSTypeError()

    def _getTime(self, key: str) -> Union[int, float]:
        if key in self._data:
            v = self._data[key]
            if v is not None and isinstance(v, (int, float)):
                return v
        return None

    def _setTime(self, key: str, v):
        if isinstance(v, (int, float)):
            self._data[key] = v
        elif isinstance(v, str):
            if v.isnumeric():
                self._data[key] = int(v)

    def _toGMT(self, t: int):
        if t is None:
            return None
        return strftime(GMT_FORMAT, gmtime(t))

    def _toISO(self, t: int):
        if t is None:
            return None
        return strftime(ISO8601_FORMAT, gmtime(t))

    @property
    def title(self):
        if 'title' in self._data:
            v = self._data['title']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @title.setter
    def title(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['title'] = v
        else:
            try:
                self._data['title'] = str(v)
            except:
                pass

    @property
    def link(self):
        if 'link' in self._data:
            v = self._data['link']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @link.setter
    def link(self, v):
        if isinstance(v, str):
            s = v
        else:
            try:
                s = str(v)
            except:
                return
        p = urlparse(s)
        n = ParseResult(p.scheme if p.scheme != '' else 'http', p.netloc,
                        p.path, p.params, p.query, p.fragment)
        self._data['link'] = urlunparse(n)

    @property
    @rss2Required
    def description(self):
        if 'description' in self._data:
            v = self._data['description']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @description.setter
    @rss2Required
    def description(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['description'] = v
        else:
            try:
                self._data['description'] = str(v)
            except:
                pass

    @property
    def pubDate(self):
        return self._getTime('pubDate')

    @property
    def pubDateAsGMT(self):
        return self._toGMT(self.pubDate)

    @property
    def pubDateAsISO(self):
        return self._toISO(self.pubDate)

    @pubDate.setter
    def pubDate(self, v):
        self._setTime('pubDate', v)


class RSSItem(RSSBasic):
    def __init__(self, typ):
        RSSBasic.__init__(self, typ)

    @property
    def author(self):
        if 'author' in self._data:
            v = self._data['author']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @author.setter
    def author(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['author'] = v
        else:
            try:
                self._data['author'] = str(v)
            except:
                pass

    @property
    def comments(self):
        if 'comments' in self._data:
            v = self._data['comments']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @comments.setter
    def comments(self, v):
        if isinstance(v, str):
            s = v
        else:
            try:
                s = str(v)
            except:
                return
        p = urlparse(s)
        n = ParseResult(p.scheme if p.scheme != '' else 'http', p.netloc,
                        p.path, p.params, p.query, p.fragment)
        self._data['comments'] = urlunparse(n)

    @property
    def guid(self):
        if 'guid' in self._data:
            v = self._data['guid']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @guid.setter
    def guid(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['guid'] = v
        else:
            try:
                self._data['guid'] = str(v)
            except:
                pass

    def generate(self):
        if self._type == RSS2_TYPE:
            return self.genRSS2()

    def genRSS2(self):
        r = ET.Element("item")
        t = self.title
        has_title = t is not None
        if has_title:
            e = ET.Element("title")
            e.append(CDATA(t))
            r.append(e)
        t = self.description
        has_desc = t is not None
        if has_desc:
            e = ET.Element("description")
            e.append(CDATA(t))
            r.append(e)
        if not has_title and not has_desc:
            raise RSSAttrRequired("title or description")
        t = self.comments
        if t is not None:
            e = ET.Element("comments")
            e.text = t
            r.append(e)
        t = self.guid
        if t is not None:
            e = ET.Element("guid")
            e.text = t
            r.append(e)
        t = self.link
        if t is not None:
            e = ET.Element("link")
            e.text = t
            r.append(e)
        t = self.pubDateAsGMT
        if t is not None:
            e = ET.Element("pubDate")
            e.text = t
            r.append(e)
        return r


class RSSMetadata(RSSBasic):
    def __init__(self, typ):
        RSSBasic.__init__(self, typ)

    @property
    @rss2Required
    def language(self):
        if 'language' in self._data:
            v = self._data['language']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @language.setter
    @rss2Required
    def language(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['language'] = v
        else:
            try:
                self._data['language'] = str(v)
            except:
                pass

    @property
    def copyright(self):
        if 'copyright' in self._data:
            v = self._data['copyright']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @copyright.setter
    def copyright(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['copyright'] = v
        else:
            try:
                self._data['copyright'] = str(v)
            except:
                pass

    @property
    def managingEditor(self):
        if 'managingEditor' in self._data:
            v = self._data['managingEditor']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @managingEditor.setter
    def managingEditor(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['managingEditor'] = v
        else:
            try:
                self._data['managingEditor'] = str(v)
            except:
                pass

    @property
    def webMaster(self):
        if 'webMaster' in self._data:
            v = self._data['webMaster']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @webMaster.setter
    def webMaster(self, v):
        if isinstance(v, str):
            if v != '':
                self._data['webMaster'] = v
        else:
            try:
                self._data['webMaster'] = str(v)
            except:
                pass

    @property
    def lastBuildDate(self):
        return self._getTime('lastBuildDate')

    @property
    def lastBuildDateAsGMT(self):
        return self._toGMT(self.lastBuildDate)

    @property
    def lastBuildDateAsISO(self):
        return self._toISO(self.lastBuildDate)

    @lastBuildDate.setter
    def lastBuildDate(self, v):
        self._setTime('lastBuildDate', v)

    @property
    @rss2Required
    def generator(self):
        return 'csweb (https://github.com/lifegpc/csweb)'

    @property
    @rss2Required
    def docs(self):
        return 'https://cyber.harvard.edu/rss/rss.html'

    @property
    def ttl(self):
        if 'ttl' in self._data:
            v = self._data['ttl']
            if v is not None:
                if isinstance(v, int) and v > 0:
                    return v
                elif isinstance(v, float) and round(v) > 0:
                    return round(v)
                elif isinstance(v, str) and v.isnumeric():
                    i = int(v)
                    if i > 0:
                        return i
        return None

    @ttl.setter
    def ttl(self, v):
        if isinstance(v, int):
            if v > 0:
                self._data['ttl'] = v
        elif isinstance(v, float):
            if round(v) > 0:
                self._data['ttl'] = v
        elif isinstance(v, str) and v.isnumeric():
            i = int(v)
            if i > 0:
                self._data['ttl'] = i

    @property
    def image(self):
        if 'image' in self._data:
            v = self._data['image']
            if v is not None and isinstance(v, str) and v != '':
                return v
        return None

    @image.setter
    def image(self, v):
        if isinstance(v, str):
            s = v
        else:
            try:
                s = str(v)
            except:
                return
        p = urlparse(s)
        n = ParseResult(p.scheme if p.scheme != '' else 'http', p.netloc,
                        p.path, p.params, p.query, p.fragment)
        self._data['image'] = urlunparse(n)

    def generate(self, r: ET.Element):
        if self._type == RSS2_TYPE:
            self.genRSS2(r)

    def genRSS2(self, r: ET.Element):
        t = self.title
        if t is None:
            raise RSSAttrRequired("title")
        e = ET.Element("title")
        e.append(CDATA(t))
        r.append(e)
        t = self.link
        if t is None:
            raise RSSAttrRequired("link")
        e = ET.Element("link")
        e.text = t
        r.append(e)
        t = self.description
        if t is None:
            raise RSSAttrRequired("description")
        e = ET.Element("description")
        e.append(CDATA(t))
        r.append(e)
        t = self.copyright
        if t is not None:
            e = ET.Element("copyright")
            e.text = t
            r.append(e)
        t = self.docs
        if t is not None:
            e = ET.Element("docs")
            e.text = t
            r.append(e)
        t = self.generator
        if t is not None:
            e = ET.Element("generator")
            e.text = t
            r.append(e)
        t = self.image
        if t is not None:
            e = ET.Element("image")
            e.text = t
            r.append(e)
        t = self.language
        if t is not None:
            e = ET.Element("language")
            e.text = t
            r.append(e)
        t = self.lastBuildDateAsGMT
        if t is not None:
            e = ET.Element("lastBuildDate")
            e.text = t
            r.append(e)
        t = self.managingEditor
        if t is not None:
            e = ET.Element("managingEditor")
            e.text = t
            r.append(e)
        t = self.pubDateAsGMT
        if t is not None:
            e = ET.Element("pubDate")
            e.text = t
            r.append(e)
        t = self.ttl
        if t is not None:
            e = ET.Element("ttl")
            e.text = str(t)
            r.append(e)
        t = self.webMaster
        if t is not None:
            e = ET.Element("webMaster")
            e.text = str(t)
            r.append(e)


class RSSGen:
    def __init__(self, typ: int):
        self.meta = RSSMetadata(typ)
        self._typ = typ
        self.list = []

    def generate(self):
        if self._typ == RSS2_TYPE:
            return self.genRSS2()

    def genRSS2(self):
        r = ET.Element("rss")
        r.attrib['version'] = '2.0'
        c = ET.Element("channel")
        r.append(c)
        self.meta.genRSS2(c)
        for i in self.list:
            if isinstance(i, RSSItem):
                c.append(i.genRSS2())
        return ET.tostring(r, encoding='UTF8').decode()
