from io import BytesIO

class B2File:

    def __init__(self, connector, parent_list, fileId, fileName, contentSha1, contentLength, contentType,
                 fileInfo, action, uploadTimestamp, *args, **kwargs):
        self.file_id = fileId
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
        path = '/b2_delete_file_version'
        params = {
            'fileId': self.file_id,
            'fileName': self.file_name
        }
        response = self.connector.make_request(path=path, method='post', params=params)
        if response.status_code == 200:
            self.deleted = True
            del self.parent_list._files_by_name[self.file_name]
            del self.parent_list._files_by_id[self.file_id]
        else:
            print(response.json())
            raise ValueError
            #TODO:  Raise Error

    def download(self):
        response = self.connector.download_file(file_id=self.file_id)
        if response.status_code == 200:
            return BytesIO(response.content)
