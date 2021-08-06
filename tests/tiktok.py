import sys
from os.path import abspath, exists
if abspath('tests/') not in sys.path:
    sys.path.append(abspath('tests/'))
from req import Req
from os import remove
from utils import set_settings


SEC1 = 'test1234'
SEC2 = 'esdd1234'
DB = 'tiktokdebug.db'
USERNAME = 'yui_ogura_offcial'
VID = '6945812541574499585'
set_settings('tiktokRSSSecrets', SEC1)
set_settings('tiktokDatabaseLocation', DB)
set_settings('RSSProxySerects', SEC2)
if exists(DB):
    remove(DB)
r = Req(SEC1)
print("Get User's RSS:")
re = r.getWithSign('/tiktokRSS', {"u": [USERNAME], 't': ['rss']})
if re.status_code >= 400:
    print(re.text)
    raise ValueError(f"{re.status_code} {re.reason}")
print("Get video's link with VID:")
re = r.getWithSign('/tiktokRSS', {"vid": [VID], 't': ['url']},
                   allow_redirects=False)
if re.status_code != 302:
    print(re.text)
    raise ValueError(f"{re.status_code} {re.reason}")
print(f"Get proxy link: {re.headers['location']}")
print("Get video's link with VID and username:")
re = r.getWithSign('/tiktokRSS', {"vid": [VID], 'u': [USERNAME], 't': ['url']},
                   allow_redirects=False)
if re.status_code != 302:
    print(re.text)
    raise ValueError(f"{re.status_code} {re.reason}")
print(f"Get proxy link: {re.headers['location']}")
