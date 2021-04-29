from insta_api import (  # pylint: disable=no-name-in-module
    InstaAPI as _InstaAPI,
    LoginAuthenticationError,
    login_endpoint
)
from instaDatabase import InstaDatabase
from requests.exceptions import HTTPError


class InstaAPI(_InstaAPI):
    def __init__(self, instaDatabase: InstaDatabase, username: str,
                 password: str, **k):
        _InstaAPI.__init__(self, False)
        self._db = instaDatabase
        self.use_cookies = True
        self._try_username = username
        self._try_password = password

    def _load_cookies(self) -> bool:
        c = self._db.get_cookies(self._try_username)
        if c is None:
            return False
        self.ses.cookies = c
        return True

    def _save_cookies(self,):
        self._db.save_cookies(self._try_username, self.ses.cookies)

    def login(self):
        username = self._try_username
        password = self._try_password
        self._get_init_csrftoken()
        login_data = {'username': username, 'password': password}
        try:
            self._make_request(login_endpoint, data=login_data,
                               msg="Login request sent")
        except HTTPError:
            resp_data = self.last_resp.json()
            if resp_data['message'] == 'checkpoint_required':
                self._save_cookies()
                #  TODO: complete verify
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
