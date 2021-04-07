import web
from yaml import load, CSafeLoader, CSafeDumper, dump
from settings import settings
from traceback import format_exc
from requests import get
from sign import verifySign


def readFile(data: str, isFileName: bool = False):
    if isFileName:
        a = '\\'
        data = f"cfw_profile/{data.replace('/', '').replace(a, '')}.yaml"
        with open(data, 'r', encoding='utf8') as f:
            return load(f, CSafeLoader)
    else:
        return load(data, CSafeLoader)


class CfwFileSettings:
    default_proxy: str = None

    def __init__(self, default_proxy: str = None):
        self.default_proxy = default_proxy


def checkNameInList(li: list, name: str):
    if name is None or name == '':
        return False
    for i in li:
        if 'name' in i and i['name'] == name:
            return True
    return False


def addProfileToTarget(source, target, settings: CfwFileSettings):
    if 'proxies' in source and 'proxies' in target:
        target['proxies'] = source['proxies'] + target['proxies']
    elif 'proxies' in source:
        target['proxies'] = source['proxies']
    if 'proxy-groups' in source:
        for d in source['proxy-groups']:
            if 'proxies' in d:
                r = []
                for i in d['proxies']:
                    if i.find("$(default_proxy)") > -1:
                        if settings.default_proxy and 'proxy-groups' in target\
                            and checkNameInList(target['proxy-groups'],
                                                settings.default_proxy):
                            i = i.replace("$(default_proxy)",
                                          settings.default_proxy)
                            r.append(i)
                    else:
                        r.append(i)
                d['proxies'] = r
    if 'proxy-groups' in source and 'proxy-groups' in target:
        target['proxy-groups'] = source['proxy-groups'] + target['proxy-groups']  # noqa: E501
    elif 'proxy-groups' in source:
        target['proxy-groups'] = source['proxy-groups']
    if 'rules' in source:
        r = []
        for i in source['rules']:
            if i.find("$(default_proxy)") > -1:
                if settings.default_proxy and 'proxy-groups' in target and\
                    checkNameInList(target['proxy-groups'],
                                    settings.default_proxy):
                    i = i.replace("$(default_proxy)", settings.default_proxy)
                    r.append(i)
            else:
                r.append(i)
        source['rules'] = r
    if 'rules' in target and 'rules' in source:
        target['rules'] = source['rules'] + target['rules']
    elif 'rules' in source:
        target['rules'] = source['rules']


class CfwProfile:
    def GET(self):
        try:
            s = settings()
            s.ReadSettings()
            if s.cfwProfileSecrets and not verifySign(s.cfwProfileSecrets):
                web.HTTPError('401 Unauthorized')
                return ''
            origin = web.input().get("o")
            if origin is None or origin == '':
                origin = web.input().get("origin")
            if origin is None or origin == '':
                web.HTTPError('400 Bad Request')
                return ''
            r = get(origin)
            if r.status_code >= 400:
                web.HTTPError('400 Bad Request')
                return f'status = {r.status_code}\n{r.text}'
            ori = readFile(r.text)
            pro = web.input().get("p")
            if pro is None or pro == '':
                pro = web.input().get("profile")
            if pro is None or pro == '':
                return r.text
            prod = readFile(pro, True)
            d = {}
            default_proxy = web.input().get("dp")
            if default_proxy is None or default_proxy == '':
                default_proxy = web.input().get("default_proxy")
            if default_proxy is not None and default_proxy != '':
                d['default_proxy'] = default_proxy
            cfws = CfwFileSettings(**d)
            addProfileToTarget(prod, ori, cfws)
            t = dump(ori, Dumper=CSafeDumper, allow_unicode=True)
            web.header('Content-Type', 'text/yaml; charset=utf-8')
            return t
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
