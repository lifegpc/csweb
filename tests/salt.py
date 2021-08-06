from requests import Session


ses = Session()
ses.trust_env = False
r = ses.get('http://127.0.0.1:2600/salt')
if r.status_code >= 400:
    raise ValueError(f'Get {r.status_code} {r.reason}')
