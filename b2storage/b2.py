# Copyright George Sibble 2018

import os
from exceptions import B2ApplicationKeyNotSet, B2KeyIDNotSet, B2InvalidBucketName, B2InvalidBucketConfiguration
from connector import B2Connector


class B2(object):

    def __init__(self, key_id=None, application_key=None):
        if key_id is None or application_key is None:
            key_id = os.environ.get('B2_ACCOUNT_ID', None)
            application_key = os.environ.get('B2_APPLICATION_KEY', None)
        if key_id is None:
            raise B2KeyIDNotSet
        if application_key is None:
            raise B2ApplicationKeyNotSet
        self.key_id = key_id
        self.application_key = application_key
        self.connector = B2Connector(key_id=self.key_id, application_key=self.application_key)


    def create_bucket(self, Bucket, CreateBucketConfiguration=None):
        if type(Bucket) != str or type(Bucket) != bytes:
            raise B2InvalidBucketName
        if type(CreateBucketConfiguration) != dict and CreateBucketConfiguration is not None:
            raise B2InvalidBucketConfiguration

    def Object(self, bucket, file_name):
        pass


    def Bucket(self, bucket_name):
        pass

    @property
    def buckets(self):
        return []

