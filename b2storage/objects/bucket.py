
class B2Bucket:

    def __init__(self, connector, bucketId, bucketName, bucketType, bucketInfo, lifecycleRules, revision, corsRules,
                 *args, **kwargs):
        self.bucket_id = bucketId
        self.bucket_name = bucketName
        self.bucket_type = bucketType
        self.bucket_info = bucketInfo
        self.lifecycle_rules = lifecycleRules
        self.revision = revision
        self.cors_rules = corsRules
        self.connector = connector
        self.deleted = False

    def delete(self, bucket=None, bucket_id=None):
        path = '/b2_delete_bucket'
        using_bucket = False
        if bucket is not None:
            bucket_id = bucket.bucket_id
            using_bucket = True
        #TODO:  Check bucket ID proper
        params = {
            'bucketId': bucket_id
        }
        response = self.connector.make_request(path=path, method='post', params=params, account_id_required=True)
        if response.status_code == 200:
            if using_bucket:
                bucket.deleted = True
            print(response.json())
        else:
            print(response.json())
            #TODO:  Raise Error

    def edit(self):
        pass
