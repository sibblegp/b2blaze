"""
Copyright George Sibble 2018
"""
import b2blaze.b2lib
import sure
from sure import expect
import random
import string
import pytest
from b2blaze.b2_exceptions import B2RequestError, B2FileNotFound

class TestB2(object):
    """

    """
    @classmethod
    def setup_class(cls):
        """

        :return: None
        """
        cls.b2 = b2blaze.b2lib.B2()
        cls.bucket_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7))
        print(cls.bucket_name)

    def test_create_b2_instance(self):
        """Create a B2 instance """
        b2 = b2blaze.b2lib.B2()

    @pytest.mark.bucket
    @pytest.mark.files
    def test_create_bucket(self):
        """ Create a bucket by name. """
        self.bucket = self.b2.buckets.create(self.bucket_name, security=self.b2.buckets.public)
        assert self.bucket

    @pytest.mark.bucket
    @pytest.mark.files
    def test_get_bucket(self):
        """ Get a bucket by name """ 
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        assert bucket

    @pytest.mark.bucket
    def test_get_all_buckets(self):
        """ Get buckets. Number of buckets returned should be >1 """
        buckets = self.b2.buckets.all()
        expect(len(buckets)).should.be.greater_than(1)

    @pytest.mark.bucket
    @pytest.mark.files
    def test_get_nonexistent_bucket(self):
        """ Get a bucket which doesn't exist should return None """ 
        bucket = self.b2.buckets.get(bucket_name='this doesnt exist')
        assert not bucket

    @pytest.mark.files
    def test_create_file_and_retrieve_by_id(self):
        """ Create a file and retrieve by ID """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        contents='Hello World!'.encode('utf-8')     # These fail unless encoded to UTF8
        file = bucket.files.upload(contents=contents, file_name='test/hello.txt')
        file2 = bucket.files.get(file_id=file.file_id)


    @pytest.mark.files
    def test_direct_upload_file(self):
        """ Upload binary file """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        binary_file = open('b2blaze/test_pic.jpg', 'rb')
        uploaded_file = bucket.files.upload(contents=binary_file, file_name='test_pic2.jpg')
        binary_file.close()


    @pytest.mark.files
    def test_get_all_files(self):
        """ Get all files from a bucket """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        files = bucket.files.all()
        print('test_get_files: all files: ', len(files))


    @pytest.mark.files
    def test_get_all_file_versions(self):
        """ Get all file versions from a bucket """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        files = bucket.files.all_file_versions()
        print('test_get_all_file_versions: all versions: ', len(files['file_versions']))
        assert len(files['file_versions']) > 0, 'File versions should exist'


    @pytest.mark.files
    def test_get_file_by_name(self):
        """ Get file by name """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        assert file


    @pytest.mark.files
    def test_get_file_by_id(self):
        """ Get file by id """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        assert file


    @pytest.mark.files
    def test_get_file_versions(self):
        """ Get all versions of a file """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        versions = file.versions()
        assert len(versions) > 0, 'File should have multiple versions'


    @pytest.mark.files
    def test_get_file_doesnt_exist(self):
        """ Get file which doens't exist should raise B2FileNotFound """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        with pytest.raises(B2FileNotFound):
            file = bucket.files.get(file_name='nope.txt')
        with pytest.raises(B2RequestError):
            file2 = bucket.files.get(file_id='abcd')

    @pytest.mark.files
    def test_download_file(self):
        """ Get file by id """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        data = file.download()
        assert len(data.read()) > 0


    @pytest.mark.files
    def test_download_url(self):
        """ Download file url should be publicly GET accessible """
        import requests
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        file = bucket.files.get(file_name='test/hello.txt')
        url = file.url
        downloaded_file = requests.get(url)
        if downloaded_file.status_code != 200:
            print(downloaded_file.json())
            raise ValueError


    @pytest.mark.files
    def test_delete_file(self): 
        """ Should create + upload, then delete a file by name.
            File should no longer exist when searched by name in bucket.
        """
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)

        # Upload file & delete
        contents='Delete this'.encode('utf-8')      # These fail unless encoded to UTF8
        upload = bucket.files.upload(contents=contents, file_name='test/deleteme.txt')
        print('test_delete_file: upload.file_name', upload.file_name)
        print('test_delete_file: upload.file_id', upload.file_id)
        upload.delete()

        # Refresh bucket; getting the the file should fail
        with pytest.raises(B2FileNotFound):
            bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
            file = bucket.files.get(file_name=upload.file_name)
            assert not file, 'Deleted file should not exist'


    @pytest.mark.files
    def test_delete_file_version(self): 
        """ Delete a file version by name. It should still exist when searched."""
        bucket = self.b2.buckets.get(bucket_name=self.bucket_name)

        # Upload file & delete
        file = bucket.files.get(file_name='test/hello.txt')
        assert file, 'File should exist'

        print('test_delete_file_version: file_name', file.file_name)
        print('test_delete_file_version: file_id', file.file_id)
        file.delete_version()

        # Refresh bucket; getting the the file should fail
        with pytest.raises(B2FileNotFound):
            bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
            file2 = bucket.files.get(file_name=file.file_name)
            assert file2, 'Deleted file version only, file should still exist'
    

    @pytest.mark.bucket
    def test_delete_non_empty_bucket(self):
        """ Delete bucket should fail on bucket non-empty """
        self.bucket = self.b2.buckets.get(bucket_name=self.bucket_name)

        # Upload file
        self.bucket.files.upload(contents='Hello World!'.encode('utf-8'), file_name='test/hello.txt')
        assert len(self.bucket.files.all()) > 0, "Bucket should still contain files" 
        
        # Should raise B2RequestError on non-empty
        with pytest.raises(B2RequestError):   
            self.bucket.delete()
        
        # Bucket should still exist
        assert self.b2.buckets.get(bucket_name=self.bucket_name), 'bucket should still exist'


    @pytest.mark.bucket
    @pytest.mark.files
    def test_cleanup_bucket_files(self):
        """ Delete all files from bucket. """
        self.bucket = self.b2.buckets.get(bucket_name=self.bucket_name)
        self.bucket.files.upload(contents='Hello World!'.encode('utf-8'), file_name='test/hello.txt')

        files = self.bucket.files.all()
        assert len(files) > 0, 'Bucket should still contain files'
        for f in files:
            f.delete()
        assert len(self.bucket.files.all()) == 0, 'Bucket should be empty'


    @pytest.mark.bucket
    def test_delete_bucket(self):
        """ Delete bucket """
        self.bucket = self.b2.buckets.get(bucket_name=self.bucket_name)

        # Ascertain it's empty
        files_new = self.bucket.files.all()
        print('files:', ', '.join([f.file_name for f in files_new]))
        assert len(files_new) == 0, "Bucket should contain no files but contains {}".format(len(files_new))
        
        # Delete
        self.bucket.delete()

        # Confirm bucket is gone. bucket.get() nonexistent should return None.
        assert not self.b2.buckets.get(bucket_name=self.bucket_name), 'Deleted bucket still exists'


    # def test_failure_to_create_bucket(self):
    #     expect(self.b2.create_bucket(
    #         ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase)
    #                 for _ in range(4)))).should.have.raised(Exception)
