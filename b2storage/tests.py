import b2lib
import sure
from sure import expect
from nose import with_setup
import random
import string
from b2_exceptions import B2BucketCreationError

class TestB2:

    @classmethod
    def setup_class(cls):
        cls.b2 = b2lib.B2()
        cls.bucket_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7))
        print(cls.bucket_name)

    def test_create_b2_instance(self):
        b2 = b2lib.B2()

    def test_create_bucket(self):
        self.bucket = self.b2.buckets.create(self.bucket_name)


    def test_create_file(self):
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        bucket.files.upload(contents='Hello World!', file_name='hello.txt')

    def test_download_file(self):
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='hello.txt')
        file.download()

    def test_get_buckets(self):
        buckets = self.b2.buckets.all
        expect(len(buckets)).should.be.greater_than(1)

    def test_get_files(self):
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        files = bucket.files.all


    def test_z_delete_bucket(self):
        self.bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        self.bucket.delete()
        print(self.bucket.deleted)
        #TODO: Assert cannot retrieve bucket by ID or name

    # def test_failure_to_create_bucket(self):
    #     expect(self.b2.create_bucket(
    #         ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase)
    #                 for _ in range(4)))).should.have.raised(Exception)
