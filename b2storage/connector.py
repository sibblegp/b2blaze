import requests
import datetime
from requests.auth import HTTPBasicAuth
from exceptions import B2AuthorizationError

class B2Connector(object):
    auth_url = 'https://api.backblazeb2.com/b2api/v1'

    def __init__(self, key_id, application_key):
        self.key_id = key_id
        self.application_id = application_id
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
        path = '/b2_authorize_account'
        result = requests.get(self.auth_url, auth=HTTPBasicAuth(self.key_id, self.application_id))
        if result.status_code == 200:
            result_json = result.json()
            self.authorized_at = datetime.datetime.utcnow()
            self.auth_token = result_json['authorizationToken']
            self.api_url = result_json['apiUrl']
            self.download_url = result_json['downloadUrl']
        else:
            raise B2AuthorizationError

    def make_request(self, path, method='get', headers=None, params=None):
        if self.authorized:
            url = self.api_url + path
        