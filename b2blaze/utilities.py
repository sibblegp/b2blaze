"""
Code used under MIT License from https://www.backblaze.com/b2/docs/string_encoding.html

Copyright (c) 2015 Backblaze
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Additional code copyright George Sibble 2018
"""

try:
    from urllib import quote, unquote_plus
except ImportError:
    from urllib.parse import quote, unquote_plus


def b2_url_encode(s):
    return quote(s.encode('utf-8'))


def b2_url_decode(s):
    return unquote_plus(str(s)).decode('utf-8')


def decode_error(response):
    try:
        response_json = response.json()
        return str(response.status_code) + ' - ' + str(response_json)
    except ValueError:
        raise ValueError(str(response.status_code) + ' - Invalid JSON Response')
