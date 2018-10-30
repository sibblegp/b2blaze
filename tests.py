"""
Copyright George Sibble 2018
"""
import b2blaze.b2lib
import sure
from sure import expect
from datetime import datetime
import pytest
from b2blaze.b2_exceptions import B2Exception, B2RequestError, B2FileNotFoundError

class TestB2(object):
    """ Tests for the b2blaze library """

    @classmethod
    def setup_class(cls):
        """

        :return: None
        """
        cls.b2 = b2blaze.b2lib.B2()
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        cls.bucket_name = 'testbucket-' + timestamp
        print('test bucket: ', cls.bucket_name)

    # Helper methods
    def test_create_b2_instance(self):
        """Create a B2 instance """
        b2 = b2blaze.b2lib.B2()


    @classmethod
    def create_bucket(cls):
        return cls.b2.buckets.create(cls.bucket_name, security=cls.b2.buckets.public)

    @classmethod
    def getbucket(cls):
        return cls.b2.buckets.get(bucket_name=cls.bucket_name) or cls.create_bucket()

    @classmethod
    def upload_textfile(cls, contents="hello there", file_name='test/hello.txt'):
        """ Upload text file with name 'test/hello.txt' """
        contents=contents.encode('utf-8')     # These fail unless encoded to UTF8
        bucket = cls.getbucket()
        return bucket.files.upload(contents=contents, file_name=file_name)


    @classmethod
    def is_b2_file(cls, obj):
        """ hacky method for checking object class/type is B2File"""
        if 'B2File' in str(type(obj)):
            return True
        return False

    ##   Tests    ##
    @pytest.mark.bucket
    @pytest.mark.files
    @pytest.mark.versions
    def test_create_bucket(self):
        """ Create a bucket by name. """
        self.bucket = self.b2.buckets.create(self.bucket_name, security=self.b2.buckets.public)
        assert self.bucket

    @pytest.mark.bucket
    def test_get_bucket(self):
        """ Get a bucket by name """ 
        bucket = self.getbucket()
        assert bucket

    @pytest.mark.bucket
    def test_get_all_buckets(self):
        """ Get buckets. Number of buckets returned should be >1 """
        buckets = self.b2.buckets.all()
        expect(len(buckets)).should.be.greater_than(1)

    @pytest.mark.bucket
    def test_get_nonexistent_bucket(self):
        """ Get a bucket which doesn't exist should return None """ 
        bucket = self.b2.buckets.get(bucket_name='this doesnt exist')
        assert not bucket

    @pytest.mark.files
    def test_create_file_and_retrieve_by_id(self):
        """ Create a file and retrieve by ID """
        bucket = self.getbucket()
        contents='Hello World!'.encode('utf-8')     # These fail unless encoded to UTF8
        file = bucket.files.upload(contents=contents, file_name='test/hello.txt')
        file2 = bucket.files.get(file_id=file.file_id)

        # It should be a B2File
        assert self.is_b2_file(file2), 'Should be a B2File object'


    @pytest.mark.files
    def test_direct_upload_file(self):
        """ Upload binary file """
        bucket = self.getbucket()
        binary_file = open('b2blaze/test_pic.jpg', 'rb')
        uploaded_file = bucket.files.upload(contents=binary_file, file_name='test_pic2.jpg')
        binary_file.close()
        assert self.is_b2_file(uploaded_file)


    @pytest.mark.files
    def test_get_all_files(self):
        """ Get all files from a bucket. Returned objects are B2Files """
        bucket = self.getbucket()
        files = bucket.files.all()
        print('test_get_files: all files: ', len(files))

        # check type
        assert self.is_b2_file(files[0]), 'Should be a B2File object'



    @pytest.mark.versions
    @pytest.mark.files
    def test_get_all_file_versions(self):
        """ Get all file versions from a bucket """
        bucket = self.getbucket()
        file = self.upload_textfile()
        files = bucket.files.all_file_versions()
        print('test_get_all_file_versions: all versions: ', len(files['file_versions']))
        assert len(files['file_versions']) > 0, 'File versions should exist'


    @pytest.mark.files
    def test_get_file_by_name(self):
        """ Get file by name """
        bucket = self.getbucket()
        file = self.upload_textfile()

        # check type
        assert self.is_b2_file(file), 'Should be a B2File object'


    @pytest.mark.files
    def test_get_file_by_id(self):
        """ Get file by id """
        bucket = self.getbucket()
        file = self.upload_textfile()

        # check type
        assert self.is_b2_file(file), 'Should be a B2File object'


    @pytest.mark.versions
    @pytest.mark.files
    def test_get_file_versions(self):
        """ Get all versions of a file via the file.get_versions method. 
            Returned data should be a list, and items should be of type B2File
        """
        bucket = self.getbucket()
        file = bucket.files.get(file_name='test/hello.txt')
        versions = file.get_versions()
        assert len(versions) > 0, 'File should have multiple versions'
        
        # check type
        assert self.is_b2_file(versions[0]), 'Should be a B2File object'


    @pytest.mark.versions
    @pytest.mark.files
    def test_bucket_get_file_versions_by_name(self):
        """ Get all versions of a file by name file_list.get_versions method. 
            Returned data should be a list, and items should be of type B2File
        """
        bucket = self.getbucket()
        versions = bucket.files.get_versions(file_name='test/hello.txt')
        assert len(versions) > 0, 'File should have multiple versions'
        assert self.is_b2_file(versions[0]), 'Should be a B2File object'


    @pytest.mark.versions
    @pytest.mark.files
    def test_bucket_get_file_versions_by_id(self):
        """ Get all versions of a file by id file_list.get_versions method. 
            Returned data should be a list, and items should be of type B2File
        """
        bucket = self.getbucket()
        file = bucket.files.get(file_name='test/hello.txt')
        versions = bucket.files.get_versions(file_id=file.file_id)
        assert len(versions) > 0, 'File should have multiple versions'
        assert self.is_b2_file(versions[0]), 'Should be a B2File object'


    @pytest.mark.files
    @pytest.mark.b2errors
    def test_get_file_doesnt_exist(self):
        """ Get file which doesn't exist should raise B2FileNotFoundError, get by ID should raise B2RequestError """
        bucket = self.getbucket()
        with pytest.raises(B2FileNotFoundError):
            file = bucket.files.get(file_name='nope.txt')
        with pytest.raises(B2RequestError):
            file2 = bucket.files.get(file_id='abcd')


    @pytest.mark.files
    def test_download_file(self):
        """ Get file by id """
        bucket = self.getbucket()
        file = self.upload_textfile()
        data = file.download()
        assert len(data.read()) > 0


    @pytest.mark.files
    def test_download_url(self):
        """ Download file url should be publicly GET accessible """
        import requests
        bucket = self.getbucket()
        file = self.upload_textfile()
        url = file.url
        downloaded_file = requests.get(url)
        if downloaded_file.status_code != 200:
            print(downloaded_file.json())
            raise ValueError


    @pytest.mark.files
    @pytest.mark.b2errors
    def test_hide_file(self): 
        """ Should create + upload, then hide / soft-delete a file by name.
            File should no longer be returned when searched by name in bucket.
        """
        bucket = self.getbucket()
        upload = self.upload_textfile(contents='Delete this', file_name='test/deleteme.txt')
        
        # Delete
        print('test_delete_file: upload.file_id', upload.file_id)
        print('test_delete_file: upload.file_name', upload.file_name)
        upload.hide()

        # Refresh bucket; getting the the file should fail
        with pytest.raises(B2FileNotFoundError):
            bucket = self.getbucket()
            file = bucket.files.get(file_name=upload.file_name)
            assert not file, 'Deleted file should not be in files list'


    @pytest.mark.files
    @pytest.mark.versions
    def test_delete_file_version(self): 
        """ Delete a file version by name. It should still exist when searched."""
        bucket = self.getbucket()

        # Upload file & delete
        file = self.upload_textfile()
        file2 = self.upload_textfile()

        # Update versions
        versions = file.get_versions()

        assert len(versions) > 1, 'File should should have multiple version'

        # Delete version
        print('test_delete_file_version: file_name', file.file_name)
        print('test_delete_file_version: file_id', file.file_id)
        file.delete_version()

        # Refresh bucket; getting the the file should fail
        file2 = bucket.files.get(file_name=file.file_name)
        assert file2, 'Deleted file version only, file should still exist'
        assert self.is_b2_file(file2), 'Should be a B2File object'
    

    # @pytest.mark.versions
    @pytest.mark.files
    def test_delete_all_file_versions(self): 
        """ Delete all versions of a file. It should be gone completely from bucket."""
        bucket = self.getbucket()

        # Create file, make sure we have multiple versions
        contents='Hello World!'.encode('utf-8')     # These fail unless encoded to UTF8
        upload = bucket.files.upload(contents=contents, file_name='test/hello.txt')
        
        # Get
        # versions = bucket.files.get_versions(file_name='test/hello.txt')
        file = bucket.files.get(file_name='test/hello.txt')
        versions = file.get_versions()
        assert len(versions) > 0, 'File should should have multiple version'

        # Delete
        print('test_delete_all_file_versions: file_name', file.file_name)
        print('test_delete_all_file_versions: file_id', file.file_id)
        file.delete_all_versions(confirm=True)

        # Refresh bucket; getting the the file should fail
        with pytest.raises(B2FileNotFoundError):
            bucket = self.getbucket()
            file2 = bucket.files.get(file_name=file.file_name)
            assert not file2, 'Deleted all file versions, file should not exist'
    

    @pytest.mark.bucket
    def test_delete_non_empty_bucket(self):
        """ Delete bucket should fail on bucket non-empty """
        bucket = self.getbucket()

        # Upload file
        self.upload_textfile()
        assert len(bucket.files.all()) > 0, "Bucket should still contain files" 
        
        # Should raise exception on non-empty without confirm
        with pytest.raises(B2RequestError):   
            bucket.delete()    # Try to delete without confirmation

        # Bucket should still exist
        assert self.b2.buckets.get(bucket_name=bucket.bucket_name), 'bucket should still exist'
        
        # # Delete with confirmation
        # bucket.delete(delete_files=True, confirm_non_empty=True)
        
        # # Bucket should be gone
        # assert self.b2.buckets.get(bucket_name=bucket.bucket_name), 'bucket should not exist'


    @pytest.mark.bucket
    @pytest.mark.files
    @pytest.mark.versions
    def test_bucket_delete_all_files(self):
        """ Delete all files from bucket. """
        bucket = self.getbucket()
        self.upload_textfile()

        files = bucket.files.all()
        assert len(files) > 0, 'Bucket should still contain files'
        
        # Delete all files
        bucket.files.delete_all()
        assert len(bucket.files.all()) == 0, 'Bucket should be empty'


    @pytest.mark.bucket
    def test_delete_bucket(self):
        """ Delete empty bucket"""
        bucket = self.getbucket()

        # Ascertain it's empty
        files_new = bucket.files.all(include_hidden=True)
        assert len(files_new) == 0, "Bucket should contain no files but contains {}".format(len(files_new))
        
        # Delete
        bucket.delete()

        # Confirm bucket is gone. bucket.get() nonexistent should return None.
        assert not self.b2.buckets.get(bucket_name=bucket.bucket_name), 'Deleted bucket still exists'

def main():
    import pytest
    pytest_args = [ __file__, '--verbose'] 
    pytest.main(pytest_args)

if __name__ == '__main__':
    main()