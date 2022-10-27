import unittest
import boto3

from retrievers.s3 import S3RequestRetriever
from widgets.request import WidgetRequest


class S3RequestRetrieverTestCase(unittest.TestCase):
    def setUp(self):
        self.bucket = 'usu-cs5260-magenta-requests'
        self.retriever = S3RequestRetriever(self.bucket)

        # Clear out the bucket
        self.s3_client = boto3.client('s3')
        response = self.s3_client.list_objects(Bucket=self.bucket)
        if 'Contents' in response:
            for key in response['Contents']:
                self.s3_client.delete_object(Bucket=self.bucket, Key=key['Key'])

    def test_initialization(self):
        client_valid = self.retriever._s3_client is not None
        bucket_valid = self.retriever._bucket == self.bucket
        self.assertTrue(client_valid and bucket_valid)

    def test_get_next_empty_bucket(self):
        self.assertIsNone(self.retriever.get_next())

    def test_get_next_invalid_request(self):
        with open('./tests/data/1612306375892', 'r') as file:
            invalid_file = file.read()
        self.s3_client.put_object(Body=invalid_file.encode(), Bucket=self.bucket, Key='1612306375892')
        self.assertIsNone(self.retriever.get_next())

    def test_get_next_valid_request(self):
        with open('./tests/data/1612306368338', 'r') as file:
            valid_file = file.read()
        self.s3_client.put_object(Body=valid_file.encode(), Bucket=self.bucket, Key='1612306368338')
        self.assertEqual(type(self.retriever.get_next()), WidgetRequest)


if __name__ == '__main__':
    unittest.main()
