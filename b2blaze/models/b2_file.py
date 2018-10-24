"""
Copyright George Sibble 2018
"""
from io import BytesIO
from ..utilities import b2_url_encode, b2_url_decode, decode_error
from ..b2_exceptions import B2RequestError
from ..api import FileAPI

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
        #self.file_name = b2_url_decode(fileName)
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

    def delete(self):
        """ Soft-delete a file (hide it from files list, but previous versions are saved.)
        :return:
        """
        path = FileAPI.delete
        params = {
            'bucketId': self.parent_list.bucket.bucket_id,
            'fileName': b2_url_encode(self.file_name)
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            self.deleted = True
            # Delete from parent list if exists
            self.parent_list._files_by_name.pop(self.file_name)
            self.parent_list._files_by_id.pop(self.file_id)
        else:
            raise B2RequestError(decode_error(response))

    def versions(self): 
        """ Return list of all versions of the current file. """
        data = self.parent_list.file_versions_by_id(self.file_id, self.file_name)
        if 'file_versions' in data:
            return data['file_versions']
        return None
            

    def delete_version(self):
        """ Delete a file version (Does not delete entire file history: only most recent version)

        :return:
        """
        path = FileAPI.delete_version
        params = {
            'fileId': self.file_id,
            'fileName': b2_url_encode(self.file_name)
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if not response.status_code == 200:
            raise B2RequestError(decode_error(response))

    def download(self):
        """

        :return:
        """
        response = self.connector.download_file(file_id=self.file_id)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise B2RequestError(decode_error(response))

    @property
    def url(self):
        """

        :return: file download url
        """
        return self.connector.download_url + '?fileId=' + self.file_id
