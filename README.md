# b2py
B2 Python Application Library

Welcome to the simpleb2 library for Python. This library will allow you to easily interact with B2 buckets and files as first class objects in Python 2 and 3. It is licensed under the MIT license so feel free to use it anywhere! If you enjoy it, please feel free to contribute or request features.

## Installation

To install simpleb2, run the following command in the proper environment:

```
pip install simpleb2
```

## Setup

You will need a key_id and an application_key to run simpleb2. You can obtain these in the B2 portal. Then, either pass them into B2() or set the environment variables B2_KEY_ID and B2_APPLICATION_KEY.

## Example Usage

SimpleB2 is built around OOP principals and as such all buckets and files are objects which you can interact with. Let's see an example where we list all of our files in a bucket:

```
from simpleb2 import B2
b2 = B2()
bucket = b2.buckets.get('test_bucket')
files = bucket.files.all
```

Files will be a list of B2File objects with all of their properties which can then be downloaded by running:

```
content = files[0].download()
```

This is a BytesIO object that you can manipulate in any way include saving locally or serving on a website.
