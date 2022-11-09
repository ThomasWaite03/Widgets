import unittest
import boto3
import json

from processors.s3 import S3RequestProcessor
from widgets.request import WidgetRequest
from widgets.widget import Widget


class S3RequestProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.bucket = 'usu-cs5260-magenta-requests'
        self.request_processor = S3RequestProcessor(self.bucket)
        self.s3_client = boto3.client('s3')

    def test_create_widget(self):
        # Process request
        with open('./tests/data/1612306368338', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Get list of bucket objects
        response = self.s3_client.list_objects(Bucket=self.bucket)

        # Check to see if object was uploaded to bucket
        true_key = 'widgets/mary-matthews/8123f304-f23f-440b-a6d3-80e979fa4cd6'
        key_in_bucket = False
        if 'Contents' in response:
            for key in response['Contents']:
                if key['Key'] == true_key:
                    key_in_bucket = True

        self.assertTrue(key_in_bucket)

    def test_update_widget(self):
        # Process create request
        with open('./tests/data/1612306370099', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Process update request to update the recently created widget
        with open('./tests/data/1612306370542', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        update_widget = test_widget_request.get_widget()
        self.request_processor.process(test_widget_request)

        response = self.s3_client.get_object(
            Bucket=self.bucket,
            Key='widgets/john-jones/5c94f104-a9b3-4fed-a039-2cc4c631d042'
        )

        # See if the widget had its attributes updated
        if response is not None:
            widget_string = response['Body'].read().decode('utf-8')
            current_widget = Widget(widget_string)

            updated_correctly = True
            for u_attr in update_widget.get_other_attributes():
                found_attribute = False
                for c_attr in current_widget.get_other_attributes():
                    if u_attr.get_name() == c_attr.get_name() and u_attr.get_value() == c_attr.get_value():
                        found_attribute = True
                updated_correctly = updated_correctly and found_attribute

            if update_widget.get_label() is not None:
                same_label = update_widget.get_label() == current_widget.get_label()
                updated_correctly = updated_correctly and same_label

            if update_widget.get_description() is not None:
                same_description = update_widget.get_description() == current_widget.get_description()
                updated_correctly = updated_correctly and same_description
        else:
            updated_correctly = False

        self.assertTrue(updated_correctly)

    def test_delete_widget(self):
        # Process create request
        with open('./tests/data/1612306370099', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Process delete request to delete recently created widget
        with open('./tests/data/1612306371375', 'r') as file:
            request_string = file.read()
        test_widget_request = WidgetRequest(request_string)
        self.request_processor.process(test_widget_request)

        # Check to see if the deleted widget was actually deleted
        response = self.s3_client.list_objects(Bucket=self.bucket)
        true_key = 'widgets/john-jones/5c94f104-a9b3-4fed-a039-2cc4c631d042'
        key_in_bucket = False
        if 'Contents' in response:
            for key in response['Contents']:
                if key['Key'] == true_key:
                    key_in_bucket = True

        self.assertFalse(key_in_bucket)


if __name__ == '__main__':
    unittest.main()
