from drawSvg import Drawing, Rectangle, Mask, Group, Text, Raw
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
from fontForgeF import fontForgeSupported
if fontForgeSupported:
    from fontForgeF import generateFontCSS, ASCII_SUPPORT


class Style(Raw):
    TAG_NAME = 'style'


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
              rightColor: str = '#08C', spacing: int = 10,
              height: int = 20, fontName: str = None) -> str:
    spacing = max(spacing, 3)
    height = max(20, height)
    fontSize = max(round(height * 0.5), max(round(height * 0.75), fontSize))
    s = settings()
    s.ReadSettings()
    if fontName is None:
        fontName = s.defaultSvgFont
        fontFamily = 'sans-serif'
    else:
        fontFamily = fontName
    t1w = textwidth(text, fontSize, fontName)
    t2w = textwidth(text2, fontSize, fontName)
    zw = 4 * spacing + t1w + t2w
    d = Drawing(zw, height)
    if fontForgeSupported and 'sans-serif' != fontFamily:
        css = generateFontCSS(fontName, text + text2, genFlags=ASCII_SUPPORT)
        if css is not None:
            d.append(Style(css))
    m = Mask(id="m")
    d.append(m)
    rx = round(height * 0.15)
    m.append(Rectangle(0, 0, zw, height, fill='#FFF', rx=rx, ry=rx))
    g1 = Group(mask="url(#m)")
    g1.append(Rectangle(0, 0, 2 * spacing + t1w, height, fill=leftColor))
    g1.append(Rectangle(2 * spacing + t1w, 0, zw, height, fill=rightColor))
    d.append(g1)
    g2 = Group(aria_hidden="true", fill=textColor, text_anchor='start',
               font_family=fontFamily)
    g2.append(Text(text, fontSize, spacing, height - fontSize, textLength=t1w))
    g2.append(Text(text2, fontSize, 3 * spacing + t1w, height - fontSize,
                   textLength=t2w))
    d.append(g2)
    return d.asSvg().replace('\n', '')


class DrawBagel:
    def GET(self):
        try:
            text = web.input().get("t")
            if text is None:
                text = web.input().get("text")
            text2 = web.input().get("t2")
            if text2 is None:
                text = web.input().get("text2")
            spacing: str = web.input().get("spacing")
            fontSize: str = web.input().get("fs")
            if fontSize is None:
                fontSize = web.input().get("fontSize")
            height: str = web.input().get("h")
            if height is None:
                height = web.input().get("height")
            textColor: str = web.input().get("tc")
            if textColor is None:
                textColor = web.input().get("textColor")
            leftColor: str = web.input().get("lc")
            if leftColor is None:
                leftColor = web.input().get("leftColor")
            rightColor: str = web.input().get("rc")
            if rightColor is None:
                rightColor = web.input().get("rightColor")
            fontName: str = web.input().get("fn")
            if fontName is None:
                fontName = web.input().get("fontName")
            if text is None or text2 is None:
                return 'Must have t and t2 parameters.'
            args = {}
            if spacing is not None and spacing.isnumeric():
                args["spacing"] = int(spacing)
            if fontSize is not None and fontSize.isnumeric():
                args["fontSize"] = int(fontSize)
            if height is not None and height.isnumeric():
                args["height"] = int(height)
            if textColor is not None and textColor != '':
                args["textColor"] = textColor
            if leftColor is not None and leftColor != '':
                args["leftColor"] = leftColor
            if rightColor is not None and rightColor != '':
                args["rightColor"] = rightColor
            if fontName is not None and fontName != '':
                args['fontName'] = fontName
            svg = drawBagel(text, text2, **args)
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
