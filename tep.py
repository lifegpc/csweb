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


def addWikiLinkToText(s: str, key: str, itemName: str, itemId: str,
                      display: str, tabIndex: int = 0):
    '''添加维基链接
    s 原始字符串：如<salt>:
    key 要替换的键：salt
    itemName 维基百科内容标题
    itemId 在wikidata上的值，Qxxxx
    display 显示名称'''
    return s.replace(f'<{key}>', f'<a class="wplink" item="{itemName}" qid="{itemId}" tabindex="{tabIndex}">{display}</a>')  # noqa: E501
