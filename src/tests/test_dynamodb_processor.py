import unittest
import boto3

from processors.dynamodb import DynamoDBRequestProcessor
from widgets.request import WidgetRequest


class DynamoDBRequestProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.table = 'widgets'
        self.request_processor = DynamoDBRequestProcessor(self.table)

    def test_create_widget(self):
        # Process request
        with open('./tests/data/1612306368338', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Get list of bucket objects
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.query(
            TableName=self.table,
            KeyConditionExpression='id = :widget_id',
            ExpressionAttributeValues={
                ':widget_id': {'S': '8123f304-f23f-440b-a6d3-80e979fa4cd6'}
            }
        )
        count = response['Count']

        # Remove the added item
        dynamodb_client.delete_item(
            TableName=self.table,
            Key={
                'id': {
                    'S': '8123f304-f23f-440b-a6d3-80e979fa4cd6'
                }
            }
        )
        self.assertEqual(count, 1)

    def test_update_widget(self):
        pass

    def test_delete_widget(self):
        pass


if __name__ == '__main__':
    unittest.main()
