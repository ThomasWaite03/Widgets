import unittest
import json

from lambda_functions.widget_request_handler import *


class WidgetRequestHandlerTestCase(unittest.TestCase):
    def test_create_request(self):
        with open('./tests/lambda_events/create_widget_event.json', 'r') as file:
            event_string = file.read()
        event = json.loads(event_string)
        response = widget_request_handler(event, None)
        self.assertEqual(response["statusCode"], 200)

    def test_update_request(self):
        with open('./tests/lambda_events/update_widget_event.json', 'r') as file:
            event_string = file.read()
        event = json.loads(event_string)
        response = widget_request_handler(event, None)
        self.assertEqual(response["statusCode"], 200)

    def test_delete_request(self):
        with open('./tests/lambda_events/delete_widget_event.json', 'r') as file:
            event_string = file.read()
        event = json.loads(event_string)
        response = widget_request_handler(event, None)
        self.assertEqual(response["statusCode"], 200)

    def test_malformed_request(self):
        with open('./tests/lambda_events/bad_widget_event.json', 'r') as file:
            event_string = file.read()
        event = json.loads(event_string)
        response = widget_request_handler(event, None)
        self.assertEqual(response["statusCode"], 400)


if __name__ == '__main__':
    unittest.main()
