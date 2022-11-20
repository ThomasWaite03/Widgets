import json
import boto3


def widget_request_handler(event, context):
    if is_valid_request(event):
        return enqueue_request(event['body'])
    else:
        return create_error_message()


def create_error_message(error):
    return ''


def enqueue_request(formatted_request):
    return ''


def is_valid_request(event):
    if 'body' in event and event['body'] != '':
        request_str = event['body']
        request = json.loads(request_str)
        attributes_present = all(a in request for a in ['widgetId', 'owner', 'type', 'requestId'])
        if attributes_present and request['widgetId'] != 'bad':
            return True
    return False
