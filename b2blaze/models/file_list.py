"""
Copyright George Sibble 2018
"""

from .b2_file import B2File
from ..utilities import b2_url_encode, get_content_length, get_part_ranges, decode_error, RangeStream, StreamWithHashProgress
from ..b2_exceptions import B2Exception, B2FileNotFoundError
from multiprocessing.dummy import Pool as ThreadPool
from ..api import API

class B2FileList(object):
    """

    """
    def __init__(self, connector, bucket):
        """

        :param connector:
        :param bucket:
        """
        self.connector = connector
        self.bucket = bucket
        self._files_by_name = {}
        self._files_by_id = {}

    def all(self, include_hidden=False, limit=None):
        """ Return an updated list of all files.
            (This does not include hidden files unless include_hidden flag set to True)

            Parameters:
                include_hidden:         (bool) Include hidden files
                limit:                  (int)  Limit number of file results

        """
        if not include_hidden:
            return self._update_files_list(retrieve=True, limit=limit)
        else:
            results = self.all_file_versions(limit=limit)
            versions = results['file_versions']
            file_ids = results['file_ids']
            if versions:
                # Return only the first file from a given file with multiple versions
                files = [versions[f][0] for f in file_ids]
                return files
        return []   # Return empty set on no results

    def delete_all(self, confirm=False):
        """ Delete all files in the bucket. 
            Parameters:
                confirm:    (bool)  Safety check. Confirm deletion
        """ 
        if not confirm:
            raise Exception('This will delete all files! Pass confirm=True')
        
        all_files = self.all(include_hidden=True)
        try:
            for f in all_files:
                f.delete_all_versions(confirm=True)
        except Exception as E:
            raise B2Exception.parse(E)
        return []

        
    def _update_files_list(self, retrieve=False, limit=None):
        """ Retrieve list of all files in bucket 
            Parameters:
                limit:      (int)  Max number of file results, default 10000
                retrieve:   (bool) Refresh local store. (default: false)
        """
        path = API.list_all_files
        files = []
        new_files_to_retrieve = True
        params = {
            'bucketId': self.bucket.bucket_id,
            'maxFileCount': limit or 10000
        }
        while new_files_to_retrieve:
            response = self.connector.make_request(path=path, method='post', params=params)
            if response.status_code == 200:
                files_json = response.json()
                self._files_by_name = {}
                self._files_by_id = {}
                for file_json in files_json['files']:
                    new_file = B2File(connector=self.connector, parent_list=self, **file_json)
                    files.append(new_file)
                    self._files_by_name[file_json['fileName']] = new_file
                    self._files_by_id[file_json['fileId']] = new_file
                if files_json['nextFileName'] is None:
                    new_files_to_retrieve = False
                else:
                    params['startFileName'] = files_json['nextFileName']
            else:
                raise B2Exception.parse(response)
        if retrieve:
            return files


    def get(self, file_name=None, file_id=None):
        """ Get a file by file name or id.
            Required:
                file_name or file_id

            Parameters:
                file_name:          (str) File name 
                file_id:            (str) File ID 
        """
        if file_name:
            file = self._get_by_name(file_name)

        elif file_id:
            file = self._get_by_id(file_id)
        else:
            raise ValueError('file_name or file_id must be passed')
        
        return file


    def get_versions(self, file_name=None, file_id=None, limit=None):
        """ Return list of all the versions of one file in current bucket. 
            Required:
                file_id or file_name   (either)

            Params:
                file_id:            (str) File id
                file_name:          (str) File id
                limit:              (int) Limit number of results returned (optional)

            Returns:
                file_versions       (list) B2FileObject of all file versions
        """ 
        if file_name:
            file = self.get(file_name)

        elif file_id:
            file = self.get(file_id=file_id)
        else:
            raise ValueError('Either file_id or file_name required for get_versions')
        return file.get_versions()
        

    def all_file_versions(self, limit=None):
        """ Return all the versions of all files in a given bucket.

            Params:
                limit:              (int) Limit number of results returned (optional). Defaults to 10000

            Returns dict: 
                'file_names':       (list) String filenames
                'file_ids':         (list) File IDs
                'file_versions':    (dict) b2blaze File objects, keyed by file name
        """ 

        path = API.list_file_versions
        file_versions = dict()
        file_names = []
        file_ids = []
        new_files_to_retrieve = True
        params = {
            'bucketId': self.bucket.bucket_id,
            'maxFileCount': 10000
        }

        # Limit files
        if limit:
            params['maxFileCount'] = limit

        while new_files_to_retrieve:

            response = self.connector.make_request(path=path, method='post', params=params)
            if response.status_code == 200:
                files_json = response.json()
                for file_json in files_json['files']:
                    new_file = B2File(connector=self.connector, parent_list=self, **file_json)

                    # Append file_id, file_name to lists
                    file_name, file_id = file_json['fileName'], file_json['fileId']
                    file_names.append(file_name)
                    file_ids.append(file_id)
                    
                    # Add file to list keyed by file_id
                    if file_id in file_versions:
                        file_versions[file_id].append(new_file)
                    else:
                        file_versions[file_id] = [new_file]

                if files_json['nextFileName'] is None:
                    new_files_to_retrieve = False
                else:
                    params['startFileName'] = files_json['nextFileName']
            else:
                raise B2Exception.parse(response)
        return {'file_names': file_names, 'file_versions': file_versions, 'file_ids': file_ids}


    def _get_by_name(self, file_name):
        """ Internal method, return single file by file name """ 
        path = API.list_all_files
        params = {
            'prefix': b2_url_encode(file_name),
            'bucketId': self.bucket.bucket_id
        }

        response = self.connector.make_request(path, method='post', params=params)
        file_json = response.json()

        # Handle errors and empty files
        if not response.status_code == 200:
            raise B2Exception.parse(response)
        if not len(file_json['files']) > 0:
            raise B2FileNotFoundError('Filename {} not found'.format(file_name))
        else:
            return B2File(connector=self.connector, parent_list=self, **file_json['files'][0])

    def _get_by_id(self, file_id):
        """ Internal method, return single file by file id """ 
        path = API.file_info
        params = {
            'fileId': file_id
        }
        response = self.connector.make_request(path, method='post', params=params)
        if response.status_code == 200:
            file_json = response.json()
            return B2File(connector=self.connector, parent_list=self, **file_json)
        else:
            raise B2Exception.parse(response)
            

    def upload(self, contents, file_name, mime_content_type=None, content_length=None, progress_listener=None):
        """

        :param contents:
        :param file_name:
        :param mime_content_type:
        :param content_length:
        :param progress_listener:
        :return:
        """
        if file_name[0] == '/':
            file_name = file_name[1:]
        get_upload_url_path = API.upload_url
        params = {
            'bucketId': self.bucket.bucket_id
        }
        upload_url_response = self.connector.make_request(path=get_upload_url_path, method='post', params=params)
        if upload_url_response.status_code == 200:
            upload_url = upload_url_response.json().get('uploadUrl', None)
            auth_token = upload_url_response.json().get('authorizationToken', None)
            upload_response = self.connector.upload_file(file_contents=contents, file_name=file_name,
                                                         upload_url=upload_url, auth_token=auth_token,
                                                         content_length=content_length, progress_listener=progress_listener,
                                                         mime_content_type=mime_content_type)
            if upload_response.status_code == 200:
                new_file = B2File(connector=self.connector, parent_list=self, **upload_response.json())
                # Update file list after upload
                self._update_files_list()
                return new_file
            else:
                raise B2Exception.parse(upload_response)
        else:
            raise B2Exception.parse(upload_url_response)

    def upload_large_file(self, contents, file_name, part_size=None, num_threads=4,
                          mime_content_type=None, content_length=None, progress_listener=None):
        """

        :param contents:
        :param file_name:
        :param part_size:
        :param num_threads:
        :param mime_content_type:
        :param content_length:
        :param progress_listener:
        :return:
        """
        if file_name[0] == '/':
            file_name = file_name[1:]
        if part_size == None:
            part_size = self.connector.recommended_part_size
        if content_length == None:
            content_length = get_content_length(contents)
        start_large_file_path = API.upload_large
        params = {
            'bucketId': self.bucket.bucket_id,
            'fileName': b2_url_encode(file_name),
            'contentType': mime_content_type or 'b2/x-auto'
        }
        large_file_response = self.connector.make_request(path=start_large_file_path, method='post', params=params)
        if large_file_response.status_code == 200:
            file_id = large_file_response.json().get('fileId', None)
            get_upload_part_url_path = API.upload_large_part
            params = {
                'fileId': file_id
            }
            pool = ThreadPool(num_threads)
            def upload_part_worker(args):
                part_number, part_range = args
                offset, content_length = part_range
                with open(contents.name, 'rb') as file:
                    file.seek(offset)
                    stream = RangeStream(file, offset, content_length)
                    upload_part_url_response = self.connector.make_request(path=get_upload_part_url_path, method='post', params=params)
                    if upload_part_url_response.status_code == 200:
                        upload_url = upload_part_url_response.json().get('uploadUrl')
                        auth_token = upload_part_url_response.json().get('authorizationToken')
                        upload_part_response = self.connector.upload_part(file_contents=stream, content_length=content_length,
                                                                          part_number=part_number, upload_url=upload_url,
                                                                          auth_token=auth_token, progress_listener=progress_listener)
                        if upload_part_response.status_code == 200:
                            return upload_part_response.json().get('contentSha1', None)
                        else:
                            raise B2Exception.parse(upload_part_response)
                    else:
                        raise B2Exception.parse(upload_part_url_response)
            sha_list = pool.map(upload_part_worker, enumerate(get_part_ranges(content_length, part_size), 1))
            pool.close()
            pool.join()
            finish_large_file_path = API.upload_large_finish
            params = {
                'fileId': file_id,
                'partSha1Array': sha_list
            }
            finish_large_file_response = self.connector.make_request(path=finish_large_file_path, method='post', params=params)
            if finish_large_file_response.status_code == 200:
                new_file = B2File(connector=self.connector, parent_list=self, **finish_large_file_response.json())
                return new_file
            else:
                raise B2Exception.parse(finish_large_file_response)
        else:
            raise B2Exception.parse(large_file_response)
