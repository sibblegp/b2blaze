"""
Copyright George Sibble 2018
"""
from io import BytesIO
from ..utilities import b2_url_encode, b2_url_decode, decode_error
from ..b2_exceptions import B2Exception
from ..api import API

class B2File(object):
    """

    """
    def __init__(self, connector, parent_list, fileId, fileName, contentSha1, contentLength, contentType,
                 fileInfo, action, uploadTimestamp, *args, **kwargs):
        """

        :param connector:
        :param parent_list:
        :param fileId:
        :param fileName:
        :param contentSha1:
        :param contentLength:
        :param contentType:
        :param fileInfo:
        :param action:
        :param uploadTimestamp:
        :param args:
        :param kwargs:
        """
        self.file_id = fileId
        # self.file_name_decoded = b2_url_decode(fileName)
         #TODO:  Find out if this is necessary
        self.file_name = fileName
        self.content_sha1 = contentSha1
        self.content_length = contentLength
        self.content_type = contentType
        self.file_info = fileInfo
        self.action = action
        self.uploadTimestamp = uploadTimestamp
        self.connector = connector
        self.parent_list = parent_list
        self.deleted = False

    def get_versions(self, limit=None): 
        """ Fetch list of all versions of the current file.
            Params:
                limit:              (int) Limit number of results returned (optional, default 10000)

            Returns:
                file_versions       (list) B2FileObject of all file versions
        """
        bucket_id = self.parent_list.bucket.bucket_id

        path = API.list_file_versions
        file_versions = []
        params = {
            'bucketId': bucket_id,
            'maxFileCount': limit or 10000,
            'startFileId': self.file_id,
            'startFileName': self.file_name,
        }

        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            files_json = response.json()
            for file_json in files_json['files']:
                new_file = B2File(connector=self.connector, parent_list=self, **file_json)
                file_versions.append(new_file)
        else:
            raise B2Exception.parse(response)
        return file_versions
        

    def hide(self):
        """ Soft-delete a file (hide it from files list, but previous versions are saved.) """
        path = API.delete_file
        params = {
            'bucketId': self.parent_list.bucket.bucket_id,
            'fileName': b2_url_encode(self.file_name)
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            self.deleted = True
        else:
            raise B2Exception.parse(response)


    def delete_all_versions(self, confirm=False):
        """ Delete completely all versions of a file. 
            ** NOTE THAT THIS CAN BE VERY EXPENSIVE IN TERMS OF YOUR API LIMITS **
            Each call to delete_all_versions will result in multiple API calls: 
                One API call per file version to be deleted, per file.
            1. Call '/b2_list_file_versions' to get file versions
            2. Call '/b2_delete_file_version' once for each version of the file

            This means: if you have 10 files with 50 versions each and call delete_all_versions, 
            you will spend (10 + 1) x 50 == 550 API calls against your BackBlaze b2 API limit.

            ** You have been warned! BE CAREFUL!!! **
        """
        print(self.delete_all_versions.__name__, self.delete_all_versions.__doc__) # Print warnings at call time.

        # Confirm deletion
        if not confirm:
            print('To call this function, use delete_all_versions(confirm=True)')
            return False

        versions = self.get_versions()

        version_count = len(versions)
        if not version_count > 0:
            print('No file versions')
        else:
            print(version_count, 'file versions')
            for count, v in enumerate(versions):
                print('deleting [{}/{}]'.format(count + 1 , version_count))
                v.delete()


    def delete(self):
        """ Delete a file version (Does not delete entire file history: only most recent version) """
        path = API.delete_file_version
        params = {
            'fileId': self.file_id,
            'fileName': b2_url_encode(self.file_name)
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if not response.status_code == 200:
            raise B2Exception.parse(response)
        self.deleted = True


    def download(self):
        """ Download latest file version """
        response = self.connector.download_file(file_id=self.file_id)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise B2Exception.parse(response)

    @property
    def url(self):
        """ Return file download URL """
        return self.connector.download_url + '?fileId=' + self.file_id
