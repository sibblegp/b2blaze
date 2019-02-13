"""
Copyright George Sibble 2018
"""
from .file_list import B2FileList
from ..b2_exceptions import B2Exception
from ..api import API


class B2Bucket(object):
    """

    """

    def __init__(
        self,
        connector,
        parent_list,
        bucketId,
        bucketName,
        bucketType,
        bucketInfo,
        lifecycleRules,
        revision,
        corsRules,
        *args,
        **kwargs
    ):
        """

        :param connector:
        :param parent_list:
        :param bucketId:
        :param bucketName:
        :param bucketType:
        :param bucketInfo:
        :param lifecycleRules:
        :param revision:
        :param corsRules:
        :param args:
        :param kwargs:
        """
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

    def delete(self, delete_files=False, confirm_non_empty=False):
        """ Delete a bucket.

        Params:
            delete_files:           (bool)  Delete all files first.
            confirm_non_empty:      (bool)  Confirm deleting on bucket not empty.
        """
        path = API.delete_bucket
        files = self.files.all(include_hidden=True)
        if delete_files:
            if not confirm_non_empty:
                raise B2Exception(
                    "Bucket is not empty! Must confirm deletion of all files with confirm_non_empty=True"
                )
            else:
                print("Deleting all files from bucket. Beware API limits!")
                self.files.delete_all(confirm=True)

        params = {"bucketId": self.bucket_id}
        response = self.connector.make_request(
            path=path, method="post", params=params, account_id_required=True
        )
        if response.status_code == 200:
            self.deleted = True
            del self.parent_list._buckets_by_name[self.bucket_name]
            del self.parent_list._buckets_by_id[self.bucket_id]
        else:
            raise B2Exception.parse(response)

    def edit(self):
        # TODO:  Edit details
        pass

    @property
    def files(self):
        """ List of files in the bucket. B2FileList instance. """
        return B2FileList(connector=self.connector, bucket=self)
