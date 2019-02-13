# api.py
# BackBlaze API endpoints

API_VERSION = "/b2api/v2"
BASE_URL = "https://api.backblazeb2.com" + API_VERSION


class API:
    authorize = "/b2_authorize_account"
    delete_file = "/b2_hide_file"
    delete_file_version = "/b2_delete_file_version"
    file_info = "/b2_get_file_info"
    download_file_by_id = "/b2_download_file_by_id"
    list_all_files = "/b2_list_file_names"
    list_file_versions = "/b2_list_file_versions"
    upload_url = "/b2_get_upload_url"
    upload_large = "/b2_start_large_file"
    upload_large_part = "/b2_get_upload_part_url"
    upload_large_finish = "/b2_finish_large_file"
    create_bucket = "/b2_create_bucket"
    delete_bucket = "/b2_delete_bucket"
    list_all_buckets = "/b2_list_buckets"
