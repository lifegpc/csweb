import sys
from os.path import abspath
if abspath('tests/') not in sys.path:
    sys.path.append(abspath('tests/'))
from req import Req, dealAPIResponse
from utils import set_settings, DebugList, debug
from json import dumps
from os import remove
from os.path import exists


def getT():
    from time import time
    return str(round(time()))


dl = DebugList('proxy.txt')
SEC = 'test1234'
DB = 'proxydebug.db'
set_settings('proxyAPISecrets', SEC)
set_settings('proxyDatabaseLocation', DB)
if exists(DB):
    remove(DB)
r = Req(SEC)
print('GET /proxy/list')
re = r.getWithSign('/proxy/list', {"a": ["list"], "t": [getT()]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('GET /proxy/add')
re = r.getWithSign('/proxy/add', {"a": ["add"], "t": [getT()], "id": ["test1"],
                                  "headers": ["test=1;a=2"],
                                  "cookies": ["tes=1;a=3"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/add')
re = r.postWithSign('/proxy/add', {"a": ["add"], "t": [getT()],
                                   "id": ["test2"],
                                   "headers": ['{"test":"2","a":"4"}'],
                                   "cookies": ['{"te":"3","a":"1"}']})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('GET /proxy/exists')
re = r.getWithSign('/proxy/exists', {"a": ["exists"], "t": [getT()],
                                     "id": ["test1"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/exists')
re = r.postWithSign('/proxy/exists', {"a": ["exists"], "t": [getT()],
                                      "id": ["test2"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/exists')
re = r.postWithSign('/proxy/exists', {"a": ["exists"], "t": [getT()],
                                      "id": ["test3"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('GET /proxy/get')
re = r.getWithSign('/proxy/get', {"a": ["get"], "t": [getT()],
                                  "id": ["test1"]})
re = dealAPIResponse(re)
debug(f"Get {re['id']}", dl=dl)
debug(f"cookies = {re['cookies']}", dl=dl)
debug(f"headers = {re['headers']}", dl=dl)
print('POST /proxy/get')
re = r.postWithSign('/proxy/get', {"a": ["get"], "t": [getT()],
                                   "id": ["test2"]})
re = dealAPIResponse(re)
debug(f"Get {re['id']}", dl=dl)
debug(f"cookies = {re['cookies']}", dl=dl)
debug(f"headers = {re['headers']}", dl=dl)
print('GET /proxy/delete')
re = r.getWithSign('/proxy/delete', {"a": ["delete"], "t": [getT()],
                                     "id": ["test2"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/delete')
re = r.postWithSign('/proxy/delete', {"a": ["delete"], "t": [getT()],
                                      "id": ["test2"]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/list')
re = r.getWithSign('/proxy/list', {"a": ["list"], "t": [getT()]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
print('POST /proxy/deleteAll')
re = r.postWithSign('/proxy/deleteAll', {"a": ["deleteAll"], "t": [getT()]})
re = dealAPIResponse(re)
debug(f"Get {dumps(re)}", dl=dl)
