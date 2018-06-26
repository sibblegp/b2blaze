"""
Copyright George Sibble 2018
"""

from ..b2_exceptions import B2InvalidBucketName, B2InvalidBucketConfiguration, B2BucketCreationError, B2RequestError
from ..utilities import decode_error
from .bucket import B2Bucket


class B2Buckets(object):
    """

    """
    public = 'allPublic'
    private = 'allPrivate'

    def __init__(self, connector):
        """

        :param connector:
        """
        self.connector = connector
        self._buckets_by_name = {}
        self._buckets_by_id = {}

    def all(self):
        """

        :return:
        """
        return self._update_bucket_list(retrieve=True)

    def _update_bucket_list(self, retrieve=False):
        """

        :param retrieve:
        :return:
        """
        path = '/b2_list_buckets'
        response = self.connector.make_request(path=path, method='post', account_id_required=True)
        if response.status_code == 200:
            response_json = response.json()
            buckets = []
            self._buckets_by_name = {}
            self._buckets_by_id = {}
            for bucket_json in response_json['buckets']:
                new_bucket = B2Bucket(connector=self.connector, parent_list=self, **bucket_json)
                buckets.append(new_bucket)
                self._buckets_by_name[bucket_json['bucketName']] = new_bucket
                self._buckets_by_id[bucket_json['bucketId']] = new_bucket
            if retrieve:
                return buckets
        else:
            raise B2RequestError(decode_error(response))

    def get(self, bucket_name=None, bucket_id=None):
        """

        :param bucket_name:
        :param bucket_id:
        :return:
        """
        self._update_bucket_list()
        if bucket_name is not None:
            return self._buckets_by_name.get(bucket_name, None)
        else:
            return self._buckets_by_id.get(bucket_id, None)

    def create(self, bucket_name, security, configuration=None):
        """

        :param bucket_name:
        :param configuration:
        :return:
        """
        path = '/b2_create_bucket'
        if type(bucket_name) != str and type(bucket_name) != bytes:
            raise B2InvalidBucketName
        if type(configuration) != dict and configuration is not None:
            raise B2InvalidBucketConfiguration
        params = {
            'bucketName': bucket_name,
            'bucketType': security,
            #TODO: bucketInfo
            #TODO: corsRules
            #TODO: lifeCycleRules
        }
        response = self.connector.make_request(path=path, method='post', params=params, account_id_required=True)
        if response.status_code == 200:
            bucket_json = response.json()
            new_bucket = B2Bucket(connector=self.connector, parent_list=self, **bucket_json)
            self._buckets_by_name[bucket_json['bucketName']] = new_bucket
            self._buckets_by_id[bucket_json['bucketId']] = new_bucket
            return new_bucket
        else:
            raise B2RequestError(decode_error(response))