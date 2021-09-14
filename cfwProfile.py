import sys
from os.path import dirname, abspath
if abspath(dirname(__file__)) not in sys.path:
    from os import chdir
    chdir(dirname(__file__))
    sys.path.append(abspath("."))
    m = True
else:
    m = False
import web
from yaml import load, CSafeLoader, CSafeDumper, dump
from settings import settings
from traceback import format_exc
from requests import get
from sign import verifySign
from typing import List
from json import dumps


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
    remove_rule_providers: bool = False
    force_enable_udp: bool = False

    def __init__(self, default_proxy: str = None,
                 remove_rule_providers: bool = False,
                 force_enable_udp: bool = False):
        self.default_proxy = default_proxy
        self.remove_rule_providers = remove_rule_providers
        self.force_enable_udp = force_enable_udp


def checkNameInList(li: list, name: str):
    if name is None or name == '':
        return False
    for i in li:
        if 'name' in i and i['name'] == name:
            return True
    return False


def generateNameList(li: list) -> List[str]:
    r = []
    for i in li:
        if 'name' in i:
            r.append(i['name'])
    return r


def removeRuleProviders(target, headers: dict):
    if 'rule-providers' not in target:
        return
    if 'rules' not in target:
        del target['rule-providers']
        return
    r = []
    for i in target['rules']:
        i: str = i.strip()
        if i.lower().startswith("rule-set"):
            li = i.split(',')
            if len(li) != 3:
                raise ValueError(f"Unknown RULE-SET rules: {i}")
            name = li[1]
            if name not in target["rule-providers"]:
                continue
            rp = target['rule-providers'][name]
            if 'url' not in rp:
                raise ValueError(f"Unknown Rule Proviers: {dumps(rp)}")
            re = get(rp["url"], headers=headers)
            if re.status_code >= 400:
                raise ValueError(f"Network Error When Downloading Providers: {re.status_code}\n{rp['url']}")  # noqa: E501
            rules = readFile(re.text)
            if isinstance(rules, str):
                raise ValueError(f"Can not parse proviers:\n{rules}")
            if 'payload' not in rules:
                raise ValueError(f"Unknown proviers:\n{dumps(rules)}")
            if rp["behavior"] == "classical":
                for j in rules["payload"]:
                    jl = j.split(",")
                    if jl[0].lower() == "ip-cidr" and len(jl) == 3:
                        r.append(f"{jl[0]},{jl[1]},{li[2]},{jl[2]}")
                    else:
                        r.append(f"{j},{li[2]}")
            elif rp["behavior"] == "ipcidr":
                for j in rules["payload"]:
                    jl = j.split(",")
                    r.append(f"IP-CIDR,{j},{li[2]}")
            else:
                raise ValueError(f"Unknown behavior: {dumps(rp)}")
        else:
            r.append(i)
    del target['rule-providers']
    target['rules'] = r
    return


def addProfileToTarget(source, target, settings: CfwFileSettings):
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
                    elif i == "$(all_origin_proxy)":
                        if 'proxies' in target:
                            r += generateNameList(target["proxies"])
                    elif i == "$(all_new_proxy)":
                        if 'proxies' in source:
                            r += generateNameList(source["proxies"])
                    else:
                        r.append(i)
                d['proxies'] = r
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
    if 'proxies' in source and 'proxies' in target:
        target['proxies'] = source['proxies'] + target['proxies']
    elif 'proxies' in source:
        target['proxies'] = source['proxies']
    if settings.force_enable_udp:
        for i in target['proxies']:
            i['udp'] = True
    if 'proxy-groups' in source and 'proxy-groups' in target:
        target['proxy-groups'] = source['proxy-groups'] + target['proxy-groups']  # noqa: E501
    elif 'proxy-groups' in source:
        target['proxy-groups'] = source['proxy-groups']
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
            headers = {"User-Agent": "ClashforWindows/0.13.8"}
            if 'HTTP_USER_AGENT' in web.ctx.env:
                ua: str = web.ctx.env['HTTP_USER_AGENT']
                if ua.lower().startswith("clash"):
                    headers.update({'User-Agent': ua})
            r = get(origin, headers=headers)
            if r.status_code >= 400:
                web.HTTPError('400 Bad Request')
                return f'status = {r.status_code}\n{r.text}'
            ori = readFile(r.text)
            if isinstance(ori, str):
                web.HTTPError('200 Not Supported Type')
                return ori
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
            remove_rule_providers = web.input().get("rrp")
            if remove_rule_providers is None:
                remove_rule_providers = web.input().get("remove_rule_providers")  # noqa: E501
            if remove_rule_providers is not None:
                d['remove_rule_providers'] = True
            force_enable_udp = web.input().get("feu")
            if force_enable_udp is None:
                force_enable_udp = web.input().get("force_enable_udp")
            if force_enable_udp is not None:
                d['force_enable_udp'] = True
            cfws = CfwFileSettings(**d)
            if cfws.remove_rule_providers:
                removeRuleProviders(ori, headers)
                removeRuleProviders(prod, headers)
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


if m:
    application = web.application((".*", "CfwProfile"), globals()).wsgifunc()
