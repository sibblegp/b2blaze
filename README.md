# b2blaze

Welcome to the b2blaze library for Python.

Backblaze B2 provides the cheapest cloud object storage and transfer available on the internet. Comparatively, AWS S3 is 320% more expensive to store and 400% more expensive to transfer to the internet.

This library will allow you to easily interact with B2 buckets and files as first class objects in Python 2 and 3. It is licensed under the MIT license so feel free to use it anywhere! If you enjoy it, please feel free to contribute or request features.

## Installation

To install b2blaze, run the following command in the proper environment:

```
pip install b2blaze
```

## Setup

You will need a key_id and an application_key to run b2blaze. You can obtain these in the B2 portal. Then, either pass them into B2() or set the environment variables B2_KEY_ID and B2_APPLICATION_KEY.

## Example Usage

b2blaze is built around OOP principals and as such all buckets and files are objects which you can interact with. Let's see an example where we list all of our files in a bucket:

```
from b2blaze import B2
b2 = B2()
bucket = b2.buckets.get('test_bucket')
files = bucket.files.all()
```

Files will be a list of B2File objects with all of their properties which can then be downloaded by running:

```
content = files[0].download()
```

This is a BytesIO object that you can manipulate in any way include saving locally or serving on a website.

# Guide

## The B2 Object

```angular2html
from b2blaze import B2
b2 = B2()
```
The B2 object is how you access b2blaze's functionality. You can optionally pass in "key_id" and "application_key" as named arguments but you should probably set them as environment variable as described above.

## Buckets

Buckets are essentially the highest level folders in B2, similar to how buckets are used in AWS S3.

#### Bucket Properties

```angular2html
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

```angular2html
buckets = b2.buckets.all()
```

#### Create a Bucket

```angular2html
bucket = b2.buckets.create('test_bucket', security=b2.buckets.public)
```

Buckets can either be public or private. This does not change the functionality of the library other than that you will need to manually authorize when using file URLs (see below).

#### Retrieve a bucket

```angular2html
bucket_by_name = b2.buckets.get('test_bucket')
bucket_by_id = b2.buckets.get(bucket_id='abcd')
```

#### Delete a bucket

```angular2html
bucket.delete()
```

This will delete both the bucket and all files within it. There is no confirmation. Use carefully.

## Files

Files are the same files you store locally. They can be stored inside folders placed in buckets but this means they simply have a name like "folder/test.txt". There is no distinction between folders and files.

#### File Properties

```angular2html
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

```angular2html
bucket.files.all()
```

NOTE: There may be tens of thousands of files (or more) in a bucket. This operation will get information and create objects for all of them. It may take quite some time and be computationally expensive to run.

#### Create (upload) a File

```angular2html
text_file = open('hello.txt').read()
new_file = bucket.files.upload(contents=text_file, file_name='folder/hello.txt')
```

#### Retrieve a File's Information (Necessary before Downloading)

```angular2html
file_by_name = bucket.files.get(file_name='folder/hello.txt')
file_by_id = bucket.files.get(file_id='abcd1234')
```

#### Download a file

````angular2html
file = bucket.files.get(file_name='folder/hello.txt')
downloaded_file = file.download()
````

This returns a BytesIO object which you can manipulate in Python using a tool like PIL, serve on a website, or easily save like this:

```angular2html
save_file = open('save_pic.jpg', 'wb')
save_file.write(downloaded_file.read())
save_file.close()
```

#### Delete a file

```angular2html
file.delete()
```

NOTE: There is no confirmation and this will delete all of a file's versions.

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

