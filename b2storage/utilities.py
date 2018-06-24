import urllib
import unittest
import json

def b2_url_encode(s):
    return urllib.quote(s.encode('utf-8'))

def b2_url_decode(s):
    return urllib.unquote_plus(str(s)).decode('utf-8')