import unittest
import boto3

from retrievers.sqs import SQSRequestRetriever
from widgets.request import WidgetRequest


class SQSRequestRetrieverTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        queue_url = 'https://sqs.us-east-1.amazonaws.com/862768396411/cs5260-requests'
        sqs_client = boto3.client('sqs')

        # Purge the queue (delete all messages)
        resp = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        count = resp['Attributes']['ApproximateNumberOfMessages']
        if count != 0:
            sqs_client.purge_queue(QueueUrl=queue_url)

    def setUp(self):
        self.queue = 'cs5260-requests'
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/862768396411/cs5260-requests'
        self.retriever = SQSRequestRetriever(self.queue)
        self.sqs_client = boto3.client('sqs')

    def test_initialization(self):
        client_valid = self.retriever._sqs_client is not None
        bucket_valid = self.retriever._queue_url == self.queue_url
        self.assertTrue(client_valid and bucket_valid)

    def test_get_next_empty_bucket(self):
        self.assertIsNone(self.retriever.get_next())

    def test_get_next_invalid_request(self):
        with open('./tests/data/1612306375892', 'r') as file:
            invalid_widget_string = file.read()
        self.sqs_client.send_message(QueueUrl=self.queue_url, MessageBody=invalid_widget_string)
        self.assertIsNone(self.retriever.get_next())

    def test_get_next_valid_request(self):
        with open('./tests/data/1612306368338', 'r') as file:
            valid_widget_string = file.read()
        self.sqs_client.send_message(QueueUrl=self.queue_url, MessageBody=valid_widget_string)
        self.assertEqual(type(self.retriever.get_next()), WidgetRequest)


if __name__ == '__main__':
    unittest.main()
