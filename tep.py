from web.template import Template


def getTemplate(name: str) -> Template:
    with open(f"html/{name}", "r", encoding='utf8') as f:
        t = f.read()
        return Template(t)
    return None


def embScr(name: str) -> str:
    fn = f'js/{name}.js'
    try:
        with open(fn, 'r', encoding='utf8') as f:
            t = f.read()
        return f'<script>{t}</script>'.replace('\n', '')
    except:
        pass
    return f'<script src="{fn}"></script>'
