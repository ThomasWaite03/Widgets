import unittest
import boto3

from processors.s3 import S3RequestProcessor
from widgets.request import WidgetRequest


class S3RequestProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.bucket = 'usu-cs5260-magenta-requests'
        self.request_processor = S3RequestProcessor(self.bucket)

    def test_create_widget(self):
        # Process request
        with open('./tests/data/1612306368338', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Get list of bucket objects
        s3_client = boto3.client('s3')
        response = s3_client.list_objects(Bucket=self.bucket)

        # Check to see if object was uploaded to bucket
        true_key = 'widgets/mary-matthews/8123f304-f23f-440b-a6d3-80e979fa4cd6'
        key_in_bucket = False
        if 'Contents' in response:
            for key in response['Contents']:
                if key['Key'] == true_key:
                    key_in_bucket = True

        self.assertTrue(key_in_bucket)


if __name__ == '__main__':
    unittest.main()
