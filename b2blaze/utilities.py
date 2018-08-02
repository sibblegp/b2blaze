"""
Code used under MIT License from https://www.backblaze.com/b2/docs/string_encoding.html

Copyright (c) 2015 Backblaze
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Additional code copyright George Sibble 2018
"""
import os
from hashlib import sha1

try:
    from urllib import quote, unquote_plus
except ImportError:
    from urllib.parse import quote, unquote_plus


def b2_url_encode(s):
    return quote(s.encode('utf-8'))


def b2_url_decode(s):
    return unquote_plus(str(s)).decode('utf-8')

def get_content_length(file):
    if hasattr(file, 'name') and os.path.isfile(file.name):
        return os.path.getsize(file.name)
    else:
        raise Exception('Content-Length could not be automatically determined.')

def decode_error(response):
    try:
        response_json = response.json()
        return str(response.status_code) + ' - ' + str(response_json)
    except ValueError:
        raise ValueError(str(response.status_code) + ' - Invalid JSON Response')

def get_part_ranges(content_length, part_size):
    parts = []
    next_offest = 0
    while content_length > 0:
        if content_length < part_size:
            part_size = content_length
        parts.append((next_offest, part_size))
        next_offest += part_size
        content_length -= part_size
    return parts

class RangeStream:
    """
    Wraps a file-like object (read only) and reads the selected
    range of the file.
    """

    def __init__(self, stream, offset, length):
        """

        :param stream:
        :param offset:
        :param length:
        :return: None
        """
        self.stream = stream
        self.offset = offset
        self.remaining = length

    def __enter__(self):
        self.stream.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.stream.__exit__(exc_type, exc_val, exc_tb)

    def seek(self, pos):
        self.stream.seek(self.offset + pos)

    def read(self, size=None):
        if size is None:
            to_read = self.remaining
        else:
            to_read = min(size, self.remaining)
        data = self.stream.read(to_read)
        self.remaining -= len(data)
        return data

class StreamWithHashProgress:
    """
    Wraps a file-like object (read-only), hashes on-the-fly, and
    updates a progress_listener as data is read.
    """

    def __init__(self, stream, progress_listener=None):
        """

        :param stream:
        :param progress_listener:
        :return: None
        """
        self.stream = stream
        self.progress_listener = progress_listener
        self.bytes_completed = 0
        self.digest = sha1()
        self.hash = None
        self.hash_read = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.stream.__exit__(exc_type, exc_val, exc_tb)

    def read(self, size=None):
        data = b''
        if self.hash is None:
            # Read some bytes from stream
            if size is None:
                data = self.stream.read()
            else:
                data = self.stream.read(size)

            # Update hash
            self.digest.update(data)

            # Check for end of stream
            if size is None or len(data) < size:
                self.hash = self.digest.hexdigest()
                if size is not None:
                    size -= len(data)

            # Update progress listener
            self._update(len(data))

        else:
            # The end of stream was reached, return hash now
            size = size or len(self.hash)
            data += str.encode(self.hash[self.hash_read:self.hash_read + size])
            self.hash_read += size

        return data

    def _update(self, delta):
        self.bytes_completed += delta
        if self.progress_listener is not None:
            self.progress_listener(self.bytes_completed)

    def get_hash(self):
        return self.hash

    def hash_size(self):
        return self.digest.digest_size * 2
