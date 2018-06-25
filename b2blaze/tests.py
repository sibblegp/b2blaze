"""
Copyright George Sibble 2018
"""
import b2lib
import sure
from sure import expect
import random
import string
import pytest
from b2_exceptions import B2RequestError, B2FileNotFound

class TestB2(object):
    """

    """
    @classmethod
    def setup_class(cls):
        """

        :return: None
        """
        cls.b2 = b2lib.B2()
        cls.bucket_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7))
        print(cls.bucket_name)

    def test_create_b2_instance(self):
        """

        :return: None
        """
        b2 = b2lib.B2()

    def test_create_bucket(self):
        """

        :return: None
        """
        self.bucket = self.b2.buckets.create(self.bucket_name, security=self.b2.buckets.public)

    def test_create_file_and_retrieve_by_id(self):
        """

        :return: None
        """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.upload(contents='Hello World!', file_name='test/hello.txt')
        file2 = bucket.files.get(file_id=file.file_id)

    def test_create_z_binary_file(self):
        """

        :return:
        """
        #from time import sleep
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        binary_file = open('test_pic.jpg')
        uploaded_file = bucket.files.upload(contents=binary_file.read(), file_name='test_pic.jpg')
        binary_file.close()
        #sleep(3)
        #downloaded_file = uploaded_file.download()
        #save_file = open('save_pic.jpg', 'wb')
        #save_file.write(downloaded_file.read())
        #save_file.close()

    def test_download_file(self):
        """

        :return: None
        """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        file.download()

    def test_download_url(self):
        """

        :return: None
        """
        import requests
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        url = file.url
        downloaded_file = requests.get(url)
        if downloaded_file.status_code != 200:
            print(downloaded_file.json())
            raise ValueError

    def test_get_buckets(self):
        """

        :return: None
        """
        buckets = self.b2.buckets.all
        expect(len(buckets)).should.be.greater_than(1)

    def test_get_files(self):
        """

        :return: None
        """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        files = bucket.files.all

    def test_get_file_doesnt_exist(self):
        """

        :return:
        """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        with pytest.raises(B2FileNotFound):
            file = bucket.files.get(file_name='nope.txt')
        with pytest.raises(B2RequestError):
            file2 = bucket.files.get(file_id='abcd')

    def test_z_delete_bucket(self):
        """

        :return: None
        """
        self.bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        self.bucket.delete()
        #TODO: Assert cannot retrieve bucket by ID or name

    # def test_failure_to_create_bucket(self):
    #     expect(self.b2.create_bucket(
    #         ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase)
    #                 for _ in range(4)))).should.have.raised(Exception)
