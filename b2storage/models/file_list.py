from ..b2_exceptions import B2InvalidBucketName, B2InvalidBucketConfiguration, B2BucketCreationError


class B2FileList:

    def __init__(self, connector, bucket):
        self.connector = connector
        self.bucket = bucket
        self._files_by_name = {}
        self._files_by_id = {}

    @property
    def all(self):
        return self._update_files_list(retrieve=True)

    def _update_files_list(self, retrieve=False):
        path = '/b2_list_file_names'
        params = {
            'bucketId': self.bucket.bucket_id,
            'maxFileCount': 10000
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            files = []
            self._files_by_name = {}
            self._files_by_id = {}
            #TODO:  Make into files
            #for files_json in response_json['buckets']:
                #new_bucket = B2Bucket(connector=self.connector, parent_list=self, **bucket_json)
                #buckets.append(new_bucket)
                #self._files_by_name[bucket_json['bucketName']] = new_bucket
                #self._files_by_id[bucket_json['bucketId']] = new_bucket
            #if retrieve:
            #    return buckets
        else:
            print(response.json())

    def get(self, file_path=None, file_id=None):
        # self._update_bucket_list()
        # if bucket_name is not None:
        #     return self._files_by_name.get(bucket_name, None)
        # else:
        #     return self._files_by_id.get(bucket_id, None)
        pass

    def upload(self, contents, file_name, mime_content_type=None):
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
            print(upload_response.status_code)
            print(upload_response.json())
        else:
            print(upload_url_request.json())
            raise ValueError
