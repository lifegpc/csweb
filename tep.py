from web.template import Template


def getTemplate(name: str) -> Template:
    with open(f"html/{name}", "r", encoding='utf8') as f:
        t = f.read()
        return Template(t)
    return None
