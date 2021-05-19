from insta_api import InstaAPI as _InstaAPI
from insta_api.exceptions import (
    LoginAuthenticationError
)
from insta_api.endpoints import (
    challenge_replay,
    challenge_endpoint,
    login_endpoint
)
from insta_api.utils import login_required
from instaDatabase import InstaDatabase
from requests.exceptions import HTTPError
from constants import jsonsep
from json import dumps


shared_data = '/data/shared_data/'
FEED_QUERY_ID = '92e44d9fc579ba10a84fd6dde2018f7d'  # 硬编码在js中


class NeedVerifyError(Exception):
    def __init__(self, sign: str):
        Exception.__init__(self, "Need verify.")
        self.sign = sign


class VerifyComplete(Exception):
    def __init__(self):
        Exception.__init__(self, "Verify completed.")


class NeedInputCodeError(Exception):
    def __init__(self):
        Exception.__init__(self, "Need input challenge code.")


def encrypt_password_version_0(password):
    return f'#PWD_INSTAGRAM_BROWSER:0:0:{password}'


class InstaAPI(_InstaAPI):
    def __init__(self, instaDatabase: InstaDatabase, username: str,
                 password: str, challenge_code: str = None, sign: str = None,
                 **k):
        _InstaAPI.__init__(self, False)
        self.key_id = None
        self.public_key = None
        self._db = instaDatabase
        self.use_cookies = True
        self._try_username = username
        self._try_password = password
        if challenge_code is not None:
            if len(challenge_code) <= 0:
                raise NeedInputCodeError()
            if sign is None or len(sign) <= 0:
                raise ValueError("Sign is needed.")
            d = self._db.get_verify(sign)
            self._checkpoint_id = d[1]
            self._checkpoint_code = d[2]
            self._challenge_code = challenge_code
            self._try_username = username
        if self._load_cookies():
            if challenge_code is not None:
                self.__solve_challenge()
        else:
            self.login()

    def __solve_challenge(self):
        if self._challenge_code == 'REPLAY':
            self._make_request(challenge_replay.format(
                id=self._checkpoint_id, code=self._checkpoint_id), post=True)
            s = self._db.save_verify(
                self._checkpoint_id, self._checkpoint_code, self._try_username)
            raise NeedVerifyError(s)
        else:
            self._make_request(challenge_endpoint.format(
                id=self._checkpoint_id, code=self._checkpoint_code),
                data={'security_code': self._challenge_code})
            if self.is_loggedin:
                self._save_cookies()
                raise VerifyComplete()
            else:
                raise LoginAuthenticationError

    def _load_cookies(self) -> bool:
        c = self._db.get_cookies(self._try_username)
        if c is None:
            return False
        self.ses.cookies = c
        return True

    def _save_cookies(self,):
        self._db.save_cookies(self._try_username, self.ses.cookies)

    def fetch_crypto_data(self):
        resp = self._make_request(shared_data)
        data = resp.json()
        self.key_id = data['encryption']['key_id']
        self.public_key = data['encryption']['public_key']

    @login_required
    def get_user_tagged(self, id: str):
        QUERY = '31fe64d9463cbbe58319dced405c6206'  # 硬编码在js中
        json = {"id": id, "first": 12}
        p = dumps(json, ensure_ascii=False, separators=jsonsep)
        resp = self._make_request(
            "/graphql/query/", params={"variables": p, "query_hash": QUERY},
            msg="Get User Tagged")
        return resp.json()['data']['user']

    def login(self):
        username = self._try_username
        password = self._try_password
        self._get_init_csrftoken()
        self.fetch_crypto_data()
        login_data = {'username': username, 'enc_password':
                      encrypt_password_version_0(password)}
        try:
            self._make_request(login_endpoint, data=login_data,
                               msg="Login request sent")
        except HTTPError:
            if not self.last_resp:
                raise ValueError("No Response.")
            resp_data = self.last_resp.json()
            if resp_data['message'] == 'checkpoint_required':
                self._save_cookies()
                checkpoint_url = resp_data['checkpoint_url']
                checkpoint_id = checkpoint_url.split("/")[2]
                checkpoint_code = checkpoint_url.split("/")[3]
                self._make_request(checkpoint_url)
                self._make_request(challenge_endpoint.format(
                    id=checkpoint_id, code=checkpoint_code),
                    data={'choice': '1'})
                s = self._db.save_verify(checkpoint_id, checkpoint_code,
                                         username)
                raise NeedVerifyError(s)
        else:
            resp_data = self.last_resp.json()
            if resp_data['authenticated']:
                self.ses.headers.update(
                    {'x-csrftoken': self.last_resp.cookies['csrftoken']})
                assert 'sessionid' in self.ses.cookies.get_dict()
                self._save_cookies()
                self.username = username
            else:
                raise LoginAuthenticationError
