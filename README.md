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
files = bucket.files.all
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
buckets = b2.buckets.all
```

#### Create a Bucket

```angular2html
bucket = b2.buckets.create('test_bucket', security=self.b2.buckets.public)
```

Buckets can either be public or private. This does not change the functionality of the library other than that you will need to manually authorize when using file URLs (see below).

#### Retrieve a bucket

```angular2html
bucket = b2.buckets.get('test_bucket')
```

#### Delete a bucket

```angular2html
bucket.delete()
```

This will delete both the bucket and all files within it. There is no confirmation. Use carefully.
