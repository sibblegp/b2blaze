"""
Copyright George Sibble 2018
"""
import requests
import datetime
from requests.auth import HTTPBasicAuth
from b2_exceptions import B2AuthorizationError, B2RequestError, B2InvalidRequestType
import sys
from hashlib import sha1
from .utilities import b2_url_encode, decode_error

class B2Connector(object):
    """

    """
    auth_url = 'https://api.backblazeb2.com/b2api/v1'

    def __init__(self, key_id, application_key):
        """

        :param key_id:
        :param application_key:
        """
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
        """

        :return:
        """
        if self.auth_token is None:
            return False
        else:
            if (datetime.datetime.utcnow() - self.authorized_at) > datetime.timedelta(hours=23):
                print('Reauthorizing')
                self._authorize()
            else:
                return True


    def _authorize(self):
        """

        :return:
        """
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
            raise B2AuthorizationError(decode_error(result))


    def make_request(self, path, method='get', headers={}, params={}, account_id_required=False):
        """

        :param path:
        :param method:
        :param headers:
        :param params:
        :param account_id_required:
        :return:
        """
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
                raise B2InvalidRequestType('Request type must be get or post')
        else:
            raise B2AuthorizationError('Unknown Error')

    def upload_file(self, file_contents, file_name, upload_url, auth_token, mime_content_type=None):
        """

        :param file_contents:
        :param file_name:
        :param upload_url:
        :param auth_token:
        :param mime_content_type:
        :return:
        """
        file_size = sys.getsizeof(file_contents)
        file_sha = sha1(file_contents).hexdigest()
        headers = {
            'Content-Type': mime_content_type or 'b2/x-auto',
            'Content-Length': str(file_size),
            'X-Bz-Content-Sha1': file_sha,
            'X-Bz-File-Name': b2_url_encode(file_name),
            'Authorization': auth_token
        }

        return requests.post(upload_url, headers=headers, data=file_contents)

    def download_file(self, file_id):
        """

        :param file_id:
        :return:
        """
        download_by_id_url = self.download_url.split('file/')[0] + '/b2api/v1/b2_download_file_by_id'
        params = {
            'fileId': file_id
        }
        headers = {
            'Authorization': self.auth_token
        }

        return requests.get(download_by_id_url, headers=headers, params=params)

