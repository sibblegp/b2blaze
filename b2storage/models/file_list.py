from ..b2_exceptions import B2InvalidBucketName, B2InvalidBucketConfiguration, B2BucketCreationError
from bucket import B2Bucket


class B2BucketFiles:

    def __init__(self, connector, bucket):
        self.connector = connector
        self.bucket = bucket
        self._files_by_name = {}
        self._files_by_id = {}

    @property
    def all(self):
        return self._update_files_list(retrieve=True)

    def _update_files_list(self, retrieve=False):
        path = '/b2_list_buckets'
        response = self.connector.make_request(path=path, method='post', account_id_required=True)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            buckets = []
            self._files_by_name = {}
            self._files_by_id = {}
            for bucket_json in response_json['buckets']:
                new_bucket = B2Bucket(connector=self.connector, parent_list=self, **bucket_json)
                buckets.append(new_bucket)
                self._files_by_name[bucket_json['bucketName']] = new_bucket
                self._files_by_id[bucket_json['bucketId']] = new_bucket
            if retrieve:
                return buckets
        else:
            print(response.json())

    def get(self, file_path=None, file_id=None):
        # self._update_bucket_list()
        # if bucket_name is not None:
        #     return self._files_by_name.get(bucket_name, None)
        # else:
        #     return self._files_by_id.get(bucket_id, None)
        pass

    def upload(self, bucket_name, configuration=None):
        pass