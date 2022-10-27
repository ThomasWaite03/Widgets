import unittest
import json
import os

from widgets.request import WidgetRequest


class WidgetRequestTestCase(unittest.TestCase):
    def setUp(self):
        # Read the sample files and add the strings to a class variable
        self.json_requests = []
        for file_name in os.listdir('./tests/data'):
            with open(f'./tests/data/{file_name}', 'r') as file:
                self.json_requests += [file.read()]

        # Create some widget objects to test and store the parameters passed
        self.widget_requests = []
        self.types = []
        self.request_ids = []
        self.widget_ids = []
        self.owners = []
        for json_request_string in self.json_requests:
            if json_request_string != '' and json.loads(json_request_string)['widgetId'] != 'bad':
                json_request = json.loads(json_request_string)
                self.types += [json_request['type']]
                self.request_ids += [json_request['requestId']]
                self.widget_ids += [json_request['widgetId']]
                self.owners += [json_request['owner']]
                self.widget_requests += [WidgetRequest(json_request_string)]

    def test_get_type(self):
        self.assertListEqual(self.types, [r.get_type() for r in self.widget_requests])

    def test_get_request_id(self):
        self.assertListEqual(self.request_ids, [r.get_request_id() for r in self.widget_requests])

    def test_widget_id(self):
        self.assertListEqual(self.widget_ids, [r.get_widget_id() for r in self.widget_requests])

    def test_get_owner(self):
        self.assertListEqual(self.owners, [r.get_owner() for r in self.widget_requests])

    def test_get_widget(self):
        has_correct_widget_ids = True
        has_correct_owners = True
        has_widget_strings = True
        has_correct_labels = True
        has_correct_description = True
        for idx, request in enumerate(self.widget_requests):
            if request.get_type() != 'delete':
                widget = request.get_widget()
                has_correct_widget_ids = has_correct_widget_ids and widget.get_id() == self.widget_ids[idx]
                has_correct_owners = has_correct_owners and widget.get_owner() == self.owners[idx]
                has_widget_strings = has_widget_strings and widget.to_string() is not None

                if 'label' not in json.loads(request._json_request):
                    has_correct_labels = has_correct_labels and widget.get_label() is None
                if 'description' not in json.loads(request._json_request):
                    has_correct_description = has_correct_description and widget.get_description() is None

        # Test passes only if all properties of created widgets are correct
        widgets_created_correctly = has_widget_strings and has_correct_widget_ids and has_correct_owners
        widgets_created_correctly = widgets_created_correctly and has_correct_labels and has_correct_description
        self.assertTrue(widgets_created_correctly)


if __name__ == '__main__':
    unittest.main()
