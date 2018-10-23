"""
Copyright George Sibble 2018
"""
import requests
import datetime
from requests.auth import HTTPBasicAuth
from b2blaze.b2_exceptions import B2AuthorizationError, B2RequestError, B2InvalidRequestType
import sys
from hashlib import sha1
from b2blaze.utilities import b2_url_encode, decode_error, get_content_length, StreamWithHashProgress
from api import BASE_API_URL, API_VERSION, AuthAPI, FileAPI

class B2Connector(object):
    """

    """
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
        self.recommended_part_size = None
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
                self._authorize()
            return True


    def _authorize(self):
        """

        :return:
        """
        path = BASE_API_URL + AuthAPI.authorize

        result = requests.get(path, auth=HTTPBasicAuth(self.key_id, self.application_key))
        if result.status_code == 200:
            result_json = result.json()
            self.authorized_at = datetime.datetime.utcnow()
            self.account_id = result_json['accountId']
            self.auth_token = result_json['authorizationToken']
            self.api_url = result_json['apiUrl'] + API_VERSION
            self.download_url = result_json['downloadUrl'] + API_VERSION + FileAPI.download_by_id
            self.recommended_part_size = result_json['recommendedPartSize']
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

    def upload_file(self, file_contents, file_name, upload_url, auth_token,
                    direct=False, mime_content_type=None, content_length=None, progress_listener=None):
        """

        :param file_contents:
        :param file_name:
        :param upload_url:
        :param auth_token:
        :param mime_content_type:
        :param content_length
        :param progress_listener
        :return:
        """
        if hasattr(file_contents, 'read'):
            if content_length is None:
                content_length = get_content_length(file_contents)
            file_sha = 'hex_digits_at_end'
            data = StreamWithHashProgress(stream=file_contents, progress_listener=progress_listener)
            content_length += data.hash_size()
        else:
            if content_length is None:
                content_length = len(file_contents)
            file_sha = sha1(file_contents).hexdigest()
            data = file_contents

        headers = {
            'Content-Type': mime_content_type or 'b2/x-auto',
            'Content-Length': str(content_length),
            'X-Bz-Content-Sha1': file_sha,
            'X-Bz-File-Name': b2_url_encode(file_name),
            'Authorization': auth_token
        }

        return requests.post(upload_url, headers=headers, data=data)

    def upload_part(self, file_contents, content_length, part_number, upload_url, auth_token, progress_listener=None):
        """

        :param file_contents:
        :param content_length:
        :param part_number:
        :param upload_url:
        :param auth_token:
        :param progress_listener:
        :return:
        """
        file_sha = 'hex_digits_at_end'
        data = StreamWithHashProgress(stream=file_contents, progress_listener=progress_listener)
        content_length += data.hash_size()

        headers = {
            'Content-Length': str(content_length),
            'X-Bz-Content-Sha1': file_sha,
            'X-Bz-Part-Number': str(part_number),
            'Authorization': auth_token
        }

        return requests.post(upload_url, headers=headers, data=data)

    def download_file(self, file_id):
        """

        :param file_id:
        :return:
        """
        url = self.download_url
        params = {
            'fileId': file_id
        }
        headers = {
            'Authorization': self.auth_token
        }

        return requests.get(url, headers=headers, params=params)

