# api.py
# BackBlaze API endpoints

API_VERSION = '/b2api/v2'
BASE_API_URL = 'https://api.backblazeb2.com' + API_VERSION


class AuthAPI():
    authorize = '/b2_authorize_account'

class FileAPI():
    delete = '/b2_hide_file'
    delete_version = '/b2_delete_file_version'
    file_info = '/b2_get_file_info'
    download_by_id = '/b2_download_file_by_id'


class BucketAPI():
    create = '/b2_create_bucket'
    delete = '/b2_delete_bucket'
    list_buckets = '/b2_list_buckets'
    list_files = '/b2_list_file_names'
    list_file_versions = '/b2_list_file_versions'
    upload_url = '/b2_get_upload_url'
    upload_large = '/b2_start_large_file'
    upload_large_part = '/b2_get_upload_part_url'
    upload_large_finish = '/b2_finish_large_file'
    


class AccountAPI():
  pass

class ApplicationKeyAPI():
  pass