from drawSvg import Drawing, Rectangle, Mask, Group, Text
from cairo import (  # pylint: disable=no-name-in-module
    SVGSurface,
    Context,
    FONT_SLANT_NORMAL,
    FONT_WEIGHT_BOLD
)
from tempfile import _get_candidate_names, gettempdir
from os import remove
from os.path import abspath
from settings import settings
import web
from traceback import format_exc


def textwidth(text: str, fontSize: int, font: str):
    fn = abspath(gettempdir() + "/" + next(_get_candidate_names()))
    width = len(text) * fontSize
    with SVGSurface(fn, 1280, 720) as surface:
        cr = Context(surface)
        cr.select_font_face(font, FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD)
        cr.set_font_size(fontSize)
        width = cr.text_extents(text)[2]
    remove(fn)
    return round(width, 1)


def drawBagel(text: str, text2: str, fontSize: int = 13,
              textColor: str = '#FFF', leftColor: str = '#555',
              rightColor: str = '#08C') -> str:
    s = settings()
    s.ReadSettings()
    t1w = textwidth(text, fontSize, s.defaultSvgFont)
    t2w = textwidth(text2, fontSize, s.defaultSvgFont)
    zw = 40 + t1w + t2w
    d = Drawing(zw, 20)
    m = Mask(id="m")
    d.append(m)
    m.append(Rectangle(0, 0, zw, 20, fill=textColor, rx="3", ry="3"))
    g1 = Group(mask="url(#m)")
    g1.append(Rectangle(0, 0, 20 + t1w, 20, fill=leftColor))
    g1.append(Rectangle(20 + t1w, 0, zw, 20, fill=rightColor))
    d.append(g1)
    g2 = Group(aria_hidden=True, fill=textColor, text_anchor='start',
               font_family='sans-serif')
    g2.append(Text(text, 13, 10, 7, textLength=t1w))
    g2.append(Text(text2, 13, 30 + t1w, 7, textLength=t2w))
    d.append(g2)
    return d.asSvg()


class DrawBagel:
    def GET(self):
        try:
            text = web.input().get("t")
            text2 = web.input().get("t2")
            if text is None or text2 is None:
                return 'Must have t and t2 parameters.'
            svg = drawBagel(text, text2)
            web.header('Content-Type', 'image/svg+xml')
            web.header('Cache-Control', 'public, max-age=600')
            return svg
        except:
            web.HTTPError('500 Internal Server Error')
            try:
                s = settings()
                s.ReadSettings()
                if s.debug:
                    return format_exc()
            except:
                pass
            return ''
