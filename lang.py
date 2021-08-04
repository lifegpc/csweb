import polib
from os.path import exists
from typing import Dict, List
import web
from constants import jsonsep
from json import dumps
LanDict = Dict[str, str]
lanList = ['en', 'ja', 'zh_CN', 'zh_TW']
StrList = List[str]


def getdict(sn: str, lan: str) -> LanDict:
    """获取翻译词典
    sn 资源名称
    lan 语言代码"""
    if lan == "en":
        fn = f"Language/{sn}.pot"
    else:
        fn = f"Language/{sn}.{lan}.po"
    if not exists(fn) and lan.startswith('zh'):
        if lan == 'zh_TW':
            fn = f'Language/{sn}.zh_CN.po'
        else:
            fn = f'Language/{sn}.zh_TW.po'
    if not exists(fn):
        fn = f'Language/{sn}.pot'
        if not exists(fn):
            return -1
    po = polib.pofile(fn, encoding='utf8')
    r = {}
    for i in po.translated_entries():
        r[i.msgctxt] = i.msgstr
    for i in po.untranslated_entries():
        r[i.msgctxt] = i.msgid
    return r


def getLangFromAcceptLanguage(lan: str = None) -> str:
    hl = web.input().get('hl')
    if lan is None:
        hl = web.input().get('hl')
        if hl is not None:
            lan = hl
        else:
            lan = web.ctx.env.get("HTTP_ACCEPT_LANGUAGE")
    if lan is None:
        return 'en'
    ql = lan.split(',')
    lanList2 = {}
    for lan in lanList:
        la = lan[:2]
        if la not in lanList2:
            lanList2[la] = lan
    for q in ql:
        q = q.split(';')[0]
        q = q.replace('-', '_')
        if q in lanList:
            return q
        if q in ['zh_Hant', 'zh_HK']:
            return 'zh_TW'
        if q[:2] in lanList2:
            return lanList2[q[:2]]
    return 'en'


def mapToDict(source: LanDict, target: LanDict, keyList: StrList):
    for key in keyList:
        if key in source and key not in target:
            target[key] = source[key]


def dictToJSON(source: LanDict) -> str:
    return dumps(source, ensure_ascii=False, separators=jsonsep)


def getTranslator(**d: Dict[str, LanDict]) -> str:
    basic = d.get('basic')
    if basic is None:
        lan = getLangFromAcceptLanguage()
        basic = getdict('basic', lan)
    t = basic['TRANSBY'] + " "
    namedict: Dict[str, StrList] = {}
    for key in d:
        ld: LanDict = d[key]
        names = ld['TRANSLATOR'].split(',')
        for name in names:
            name = name.strip()
            if name not in namedict:
                namedict[name] = [key]
            elif key not in namedict[name]:
                namedict[name].append(key)
    for name in namedict:
        t += name + "("
        for key in namedict[name]:
            t += key + ", "
        t = t.rstrip(", ")
        t += "), "
    t = t.rstrip(", ")
    return t
