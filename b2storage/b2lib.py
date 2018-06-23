# Copyright George Sibble 2018

import os
from b2_exceptions import B2ApplicationKeyNotSet, B2KeyIDNotSet, B2InvalidBucketName, B2InvalidBucketConfiguration
from b2_exceptions import B2BucketCreationError
from connector import B2Connector


class B2(object):

    def __init__(self, key_id=None, application_key=None):
        if key_id is None or application_key is None:
            key_id = os.environ.get('B2_KEY_ID', None)
            application_key = os.environ.get('B2_APPLICATION_KEY', None)
        if key_id is None:
            raise B2KeyIDNotSet
        if application_key is None:
            raise B2ApplicationKeyNotSet
        self.key_id = key_id
        self.application_key = application_key
        self.connector = B2Connector(key_id=self.key_id, application_key=self.application_key)


    def create_bucket(self, Bucket, CreateBucketConfiguration=None):
        path = '/b2_create_bucket'
        if type(Bucket) != str or type(Bucket) != bytes:
            raise B2InvalidBucketName
        if type(CreateBucketConfiguration) != dict and CreateBucketConfiguration is not None:
            raise B2InvalidBucketConfiguration
        params = {
            'bucketName': Bucket,
            'bucketType': 'allPublic',
            #TODO: bucketInfo
            #TODO: corsRules
            #TODO: lifeCycleRules
        }
        response = self.connector.make_request(path=path, method='post', params=params, account_id_required=True)
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.status_code)
            raise B2BucketCreationError(str(response.json()))

    def Object(self, bucket, file_name):
        pass


    def Bucket(self, bucket_name):
        pass


    @property
    def buckets(self):
        return []

