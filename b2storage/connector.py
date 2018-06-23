import requests
import datetime
from requests.auth import HTTPBasicAuth
from b2_exceptions import B2AuthorizationError

class B2Connector(object):
    auth_url = 'https://api.backblazeb2.com/b2api/v1'

    def __init__(self, key_id, application_key):
        self.key_id = key_id
        self.application_key = application_key
        self.account_id = None
        self.auth_token = None
        self.authorized_at = None
        self.api_url = None
        self.download_url = None
        self.api_session = None
        #TODO:  Part Size
        self._authorize()


    @property
    def authorized(self):
        if self.auth_token is None:
            return False
        else:
            if (datetime.datetime.utcnow() - self.authorized_at) > datetime.timedelta(hours=23):
                print('Reauthorizing')
                self._authorize()
            else:
                return True


    def _authorize(self):
        path = self.auth_url + '/b2_authorize_account'
        result = requests.get(path, auth=HTTPBasicAuth(self.key_id, self.application_key))
        if result.status_code == 200:
            result_json = result.json()
            self.authorized_at = datetime.datetime.utcnow()
            self.account_id = result_json['accountId']
            self.auth_token = result_json['authorizationToken']
            self.api_url = result_json['apiUrl'] + '/b2api/v1'
            self.download_url = result_json['downloadUrl'] + '/file/'
            self.api_session = requests.Session()
            self.api_session.headers.update({
                'Authorization': self.auth_token
            })
        else:
            raise B2AuthorizationError


    def make_request(self, path, method='get', headers={}, params={}, account_id_required=False):
        if self.authorized:
            url = self.api_url + path
            if method == 'get':
                return self.api_session.get(url, headers=headers)
            elif method == 'post':
                if account_id_required:
                    params.update({
                        'accountId': self.account_id
                    })
                headers.update({
                    'Content-Type': 'application/json'
                })
                return self.api_session.post(url, json=params, headers=headers)
            else:
                raise ValueError
        else:
            raise B2AuthorizationError