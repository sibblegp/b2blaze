# b2blaze 
![CircleCI](https://img.shields.io/circleci/project/github/sibblegp/b2blaze.svg)
[![Code Coverage](https://scrutinizer-ci.com/g/sibblegp/b2blaze/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/sibblegp/b2blaze/?branch=master)


Welcome to the b2blaze library for Python.

Backblaze B2 provides the cheapest cloud object storage and transfer available on the internet. Comparatively, AWS S3 is 320% more expensive to store and 400% more expensive to transfer to the internet.

This library will allow you to easily interact with B2 buckets and files as first class objects in Python 2 and 3. It is licensed under the MIT license so feel free to use it anywhere! If you enjoy it, please feel free to contribute or request features.

## Installation

To install b2blaze, run the following command in the proper environment:

```bash
pip install b2blaze
```

## Setup

You will need a key_id and an application_key to run b2blaze. You can obtain these in the B2 portal. Then, either pass them into B2() or set the environment variables B2_KEY_ID and B2_APPLICATION_KEY.

## Example Usage

b2blaze is built around OOP principles and as such all buckets and files are objects which you can interact with. Let's see an example where we list all of our files in a bucket:

```python
from b2blaze import B2
b2 = B2()
bucket = b2.buckets.get('test_bucket')
files = bucket.files.all()
```

Files will be a list of B2File objects with all of their properties which can then be downloaded by running:

```python
content = files[0].download()
```

This is a BytesIO object that you can manipulate in any way include saving locally or serving on a website.

# Guide

## The B2 Object

```python
from b2blaze import B2
b2 = B2()
```
The B2 object is how you access b2blaze's functionality. You can optionally pass in "key_id" and "application_key" as named arguments but you should probably set them as environment variable as described above.

## Buckets

Buckets are essentially the highest level folders in B2, similar to how buckets are used in AWS S3.

#### Bucket Properties

```python
bucket_id
bucket_name
bucket_type
bucket_info
lifecycle_rules
revision
cors_rules
deleted
```

#### List All Buckets

```python
buckets = b2.buckets.all()
```

#### Create a Bucket

```python
bucket = b2.buckets.create('test_bucket', security=b2.buckets.public)
```

Buckets can either be public or private. This does not change the functionality of the library other than that you will need to manually authorize when using file URLs (see below).

#### Retrieve a bucket

```python
bucket_by_name = b2.buckets.get('test_bucket')
bucket_by_id = b2.buckets.get(bucket_id='abcd')
```

#### Delete a bucket

```python
bucket.delete()
```

This will delete both the bucket and all files within it. There is no confirmation. Use carefully.

## Files

Files are the same files you store locally. They can be stored inside folders placed in buckets but this means they simply have a name like "folder/test.txt". There is no distinction between folders and files.

#### File Properties

```python
file_id
file_name
content_sha1
content_length
content_type
file_info
action
uploadTimestamp
deleted
```

#### List All Files in a Bucket

```python
bucket.files.all()
```

NOTE: There may be tens of thousands of files (or more) in a bucket. This operation will get information and create objects for all of them. It may take quite some time and be computationally expensive to run.

#### Upload a File

```python
text_file = open('hello.txt', 'rb')
new_file = bucket.files.upload(contents=text_file, file_name='folder/hello.txt')
```

NOTE: You don't have to call `.read()` and instead can send the file directly to contents. This will allow the file buffer directly over HTTP to B2 and save a significant amount of memory. Also, `contents` must be binary or a binary stream.

#### Upload a Large File

```python
large_file = open('large_file.bin', 'rb')
new_file = bucket.files.upload_large_file(contents=large_file, file_name='folder/large_file.bin', num_threads=4)
```

NOTE: You cannot call `.read()` on the file because the function will seek and buffer the file over `num_threads` for you. Per [Backblaze recommendation](https://www.backblaze.com/b2/docs/large_files.html), `part_size` defaults to `recommendedPartSize` from `b2_authorize_account` (typically 100MB). `num_threads` defaults to 4 threads. The minimum part size is 5MB and you must have must have at least 2 parts.

#### Retrieve a File's Information (Necessary before Downloading)

```python
file_by_name = bucket.files.get(file_name='folder/hello.txt')
file_by_id = bucket.files.get(file_id='abcd1234')
```

#### Download a file

````python
file = bucket.files.get(file_name='folder/hello.txt')
downloaded_file = file.download()
````

This returns a BytesIO object which you can manipulate in Python using a tool like PIL, serve on a website, or easily save like this:

```python
save_file = open('save_pic.jpg', 'wb')
save_file.write(downloaded_file.read())
save_file.close()
```

#### Delete a file version

```python
file.delete()
```

This deletes a single version of a file. (See the [docs on File Versions](https://www.backblaze.com/b2/docs/b2_delete_file_version.html) at Backblaze for explanation)

#### Hide (aka "Soft-delete") a file

```python
file.hide()
```

This hides a file (aka "soft-delete") so that downloading by name will not find the file, but previous versions of the file are still stored. (See the [docs on Hiding file](https://www.backblaze.com/b2/docs/b2_hide_file.html) at Backblaze for details)

## Testing

Unit testing with pytest
Before running, you must set the environment variables: `B2_KEY_ID` and `B2_APPLICATION_KEY`

** Run tests **

``` bash
python3 ./tests.py
```


## LICENSE

MIT License

Copyright (c) 2018 George Sibble

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

