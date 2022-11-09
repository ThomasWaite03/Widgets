import unittest
import boto3

from processors.dynamodb import DynamoDBRequestProcessor
from widgets.request import WidgetRequest


class DynamoDBRequestProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.table = 'widgets'
        self.request_processor = DynamoDBRequestProcessor(self.table)
        self.dynamo_client = boto3.client('dynamodb')

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
        # Process create request
        with open('./tests/data/1612306370099', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Process an update request to update the widget that was just created
        with open('./tests/data/1612306370542', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        update_widget = test_widget_request.get_widget()
        self.request_processor.process(test_widget_request)

        # Query the DynamoDB table to see if it was deleted
        response = self.dynamo_client.get_item(
            TableName=self.table,
            Key={
                'id': {
                    'S': test_widget_request.get_widget_id()
                }
            }
        )

        if 'Item' not in response:
            updated_correctly = False
        else:
            updated_correctly = True
            for u_attr in update_widget.get_other_attributes():
                found_attribute = False
                if u_attr.get_name() in response['Item'] \
                    and u_attr.get_value() == response['Item'][u_attr.get_name()]['S']:
                    found_attribute = True
                updated_correctly = updated_correctly and found_attribute

            if update_widget.get_label() is not None and 'label' in response['Item']:
                same_label = update_widget.get_label() == response['Item']['label']['S']
                updated_correctly = updated_correctly and same_label

            if update_widget.get_description() is not None and 'description' in response['Item']:
                same_description = update_widget.get_description() == response['Item']['label']['S']
                updated_correctly = updated_correctly and same_description

        self.assertTrue(updated_correctly)

    def test_delete_widget(self):
        # Process create request
        with open('./tests/data/1612306370099', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Process delete request for the widget that was just created
        with open('./tests/data/1612306371375', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Query the DynamoDB table to see if it was deleted
        response = self.dynamo_client.query(
            TableName=self.table,
            ExpressionAttributeValues={
                ':id': {
                    'S': test_widget_request.get_widget_id()
                }
            },
            KeyConditionExpression='id = :id'
        )
        self.assertEqual(response['Count'], 0)


if __name__ == '__main__':
    unittest.main()
