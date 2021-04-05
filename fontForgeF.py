try:
    from fontforge import font, open as openfont
    from hashl import sha256, md5
    from os.path import exists
    from os import mkdir
    from settings import settings
    from html import escape
    ASCII_SUPPORT = 1
    TTF_TYPE = 1
    WOFF_TYPE = 2
    WOFF2_TYPE = 4
    EOT_TYPE = 8
    ALL_TYPE = 15
    INCLUDE_STYLE_TAG = 1
    ADD_CSS_SELECTOR = 2

    def getFontLocation(fontName: str):
        s = settings()
        s.ReadSettings()
        if s.fontLocationMap is None:
            return None
        if fontName in s.fontLocationMap:
            return s.fontLocationMap[fontName]

    def generateFont(fontName: str, text: str, saveType: int = WOFF_TYPE,
                     flags: int = 0) -> str:
        try:
            fontLocation = getFontLocation(fontName)
            if fontLocation is None:
                return None
            if saveType <= 0:
                return None
            if flags & ASCII_SUPPORT:
                charList = [chr(i) for i in range(32, 127)]
            else:
                charList = []
            for i in text:
                if i not in charList:
                    charList.append(i)
            fn = f"fonts/{md5(fontName)}_{sha256(''.join(charList))}"
            cont = False
            if saveType & TTF_TYPE and not exists(f"{fn}.ttf"):
                cont = True
            if saveType & WOFF_TYPE and not exists(f"{fn}.woff"):
                cont = True
            if saveType & WOFF2_TYPE and not exists(f"{fn}.woff2"):
                cont = True
            if saveType & EOT_TYPE and not exists(f"{fn}.eot"):
                cont = True
            if not cont:
                return fn
            print(fontLocation)
            ft: font = openfont(fontLocation)
            print(ft.encoding)
            nf = font()
            nf.encoding = 'UnicodeBMP'
            for char in charList:
                char = ord(char)
                ft.selection.select(("more", None), char)
                nf.selection.select(("more", None), char)
            ft.copy()
            nf.paste()
            if not exists('fonts/'):
                mkdir('fonts/')
            if saveType & TTF_TYPE:
                nf.generate(f"{fn}.ttf", flags="opentype")
            if saveType & WOFF_TYPE:
                nf.generate(f"{fn}.woff")
            if saveType & WOFF2_TYPE:
                nf.generate(f"{fn}.woff2")
            if saveType & EOT_TYPE:
                nf.generate(f"{fn}.eot")
            return fn
        except Exception as e:
            s = settings()
            s.ReadSettings()
            if s.debug:
                raise e
            return None

    def generateFontCSS(fontName: str, text: str, familyName: str = None,
                        supportType: int = WOFF_TYPE, genFlags: int = 0,
                        flags: int = 0, **args):
        if familyName is None or familyName == '':
            familyName = fontName
        fn = generateFont(fontName, text, supportType, genFlags)
        if fn is None:
            return None
        fn = '/' + fn
        b = '@font-face {\nfont-family: "' + familyName + \
            '";\n src: local("' + fontName + '")'
        if supportType & WOFF2_TYPE:
            b += ',\nurl("' + fn + '.woff2") format("woff2")'
        if supportType & WOFF_TYPE:
            b += ',\nurl("' + fn + '.woff") format("woff")'
        if supportType & TTF_TYPE:
            b += ',\nurl("' + fn + '.ttf") format("truetype")'
        if supportType & EOT_TYPE:
            b += ',\nurl("' + fn + '.eof") format("embedded-opentype")'
        b += ';\n}'
        if flags & ADD_CSS_SELECTOR and 'css_selector' in args:
            if args['css_selector'] is not None and args['css_selector'] != '':
                css_selector: str = args['css_selector']
                b += '\n' + css_selector + ' {family-name: "' + familyName + \
                     '";}'
        if flags & INCLUDE_STYLE_TAG:
            b = f"<style>{escape(b)}</style>"
        return b.replace('\n', '')

    fontForgeSupported = True
except:
    fontForgeSupported = False
