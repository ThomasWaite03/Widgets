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
    pass
