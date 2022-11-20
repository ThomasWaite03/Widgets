import json
import logging
import time
import boto3
import botocore

client = boto3.client('sqs')

# Set up logging configuration
time_string = time.strftime('%m%d%Y%H%M%S')
format_str = '%(asctime)s - %(message)s'
logging.basicConfig(format=format_str, level=logging.INFO)


def widget_request_handler(event, context):
    if is_valid_request(event):
        enqueue_request(event['body'])
        return {
            "statusCode": 200
        }
    else:
        return create_error_message({
            "status": 400,
            "error": "Bad Request",
            "msg": "Your widget request was not formatted correctly or was incomplete."
        })


def create_error_message(error):
    return {
        "statusCode": error["status"],
        "headers": {
            "Content-Type": "text/html",
            "x-amzn-ErrorType": error["error"]
        },
        "isBase64Encoded": False,
        "body": f"{error['status']} ERROR {error['error']}: {error['msg']}"
    }


def enqueue_request(request_str):
    try:
        response = client.get_queue_url(QueueName='cs5260-requests')
        queue_url = response["QueueUrl"]
        client.send_message(QueueUrl=queue_url, MessageBody=request_str)
        logging.info('Successfully sent widget request to SQS queue.')
    except botocore.exceptions.ClientError:
        logging.error('Failed to enqueue request.')


def is_valid_request(event):
    if 'body' in event and event['body'] != '':
        request_str = event['body']
        request = json.loads(request_str)
        attributes_present = all(a in request for a in ['widgetId', 'owner', 'type', 'requestId'])
        if attributes_present and request['widgetId'] != 'bad':
            return True
    logging.warning('Invalid request made.')
    return False
