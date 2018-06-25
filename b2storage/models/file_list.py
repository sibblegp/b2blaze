"""
Copyright George Sibble 2018
"""

from ..b2_exceptions import B2InvalidBucketName, B2InvalidBucketConfiguration, B2BucketCreationError

from b2_file import B2File

class B2FileList(object):
    """

    """
    def __init__(self, connector, bucket):
        """

        :param connector:
        :param bucket:
        """
        self.connector = connector
        self.bucket = bucket
        self._files_by_name = {}
        self._files_by_id = {}

    @property
    def all(self):
        """

        :return:
        """
        return self._update_files_list(retrieve=True)

    def _update_files_list(self, retrieve=False):
        """

        :param retrieve:
        :return:
        """
        path = '/b2_list_file_names'
        params = {
            'bucketId': self.bucket.bucket_id,
            'maxFileCount': 10000
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            files_json = response.json()
            files = []
            self._files_by_name = {}
            self._files_by_id = {}
            for file_json in files_json['files']:
                new_file = B2File(connector=self.connector, parent_list=self, **file_json)
                files.append(new_file)
                self._files_by_name[file_json['fileName']] = new_file
                self._files_by_id[file_json['fileId']] = new_file
            if retrieve:
               return files
        else:
            print(response.json())
            raise ValueError

    def get(self, file_name=None, file_id=None):
        """

        :param file_name:
        :param file_id:
        :return:
        """
        self._update_files_list()
        if file_name is not None:
            return self._files_by_name.get(file_name, None)
        else:
            return self._files_by_id.get(file_id, None)
        pass

    def upload(self, contents, file_name, mime_content_type=None):
        """

        :param contents:
        :param file_name:
        :param mime_content_type:
        :return:
        """
        get_upload_url_path = '/b2_get_upload_url'
        params = {
            'bucketId': self.bucket.bucket_id
        }
        upload_url_request = self.connector.make_request(path=get_upload_url_path, method='post', params=params)
        upload_url = None
        auth_token = None
        if upload_url_request.status_code == 200:
            upload_url = upload_url_request.json().get('uploadUrl', None)
            auth_token = upload_url_request.json().get('authorizationToken', None)
            upload_response = self.connector.upload_file(file_contents=contents, file_name=file_name,
                                                         upload_url=upload_url, auth_token=auth_token)
            new_file = B2File(connector=self.connector, parent_list=self, **upload_response.json())
            return new_file
        else:
            print(upload_url_request.json())
            raise ValueError