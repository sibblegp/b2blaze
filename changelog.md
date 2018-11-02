
## Changelog

#### v0.2.1

**Python version update**
Python version:
- Python 3 required!

**Nonbreaking API changes:**

B2File:
- hide added
- delete_all_versions(confirm=False) added

B2FileList
- all(introduced new parameter: include_hidden)
- delete_all(confirm=False) added
- get_versions(file_name=None, file_id=None, limit=None) added
- all_file_versions(limit=None) added

b2_exceptions.py
- Changed API error classes to match Backblaze API docs
- added base API exception B2Exception.
- Handle non-200 status code responses with 'raise B2Exception.parse(response)`

tests.py
- added and cleaned up integration tests
- tests can now be run with `python tests.py`
