
class B2Bucket:

    def __init__(self, connector, parent_list, bucketId, bucketName, bucketType, bucketInfo, lifecycleRules, revision, corsRules,
                 *args, **kwargs):
        self.bucket_id = bucketId
        self.bucket_name = bucketName
        self.bucket_type = bucketType
        self.bucket_info = bucketInfo
        self.lifecycle_rules = lifecycleRules
        self.revision = revision
        self.cors_rules = corsRules
        self.connector = connector
        self.parent_list = parent_list
        self.deleted = False

    def delete(self):
        path = '/b2_delete_bucket'
        params = {
            'bucketId': self.bucket_id
        }
        response = self.connector.make_request(path=path, method='post', params=params, account_id_required=True)
        if response.status_code == 200:
            self.deleted = True
            del self.parent_list._buckets_by_name[self.bucket_name]
            del self.parent_list._buckets_by_id[self.bucket_id]
        else:
            raise ValueError
            #TODO:  Raise Error

    def edit(self):
        pass

    @property
    def files(self):
        return []