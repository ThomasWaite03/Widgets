import boto3
import logging
import sys

from .retriever import RequestRetriever
from widgets.request import WidgetRequest


class SQSRequestRetriever(RequestRetriever):
    def __init__(self, queue):
        self._sqs_client = boto3.client('sqs')
        self._cached_requests = []

        # Get the url of the queue given its name
        try:
            queue_url_resp = self._sqs_client.get_queue_url(
                QueueName=queue
            )

            self._queue_url = queue_url_resp['QueueUrl']
        except Exception as ex:
            logging.error('SQSRequestRetriever failed possibly due to invalid queue name.')
            sys.exit(1)

    def get_next(self):
        # If there are no more saved requests, get more
        if len(self._cached_requests) == 0:
            messages = self._sqs_client.receive_message(
                QueueUrl=self._queue_url,
                MaxNumberOfMessages=10
            )

            if 'Messages' in messages:
                messages = messages['Messages']
            else:
                return None

            for msg in messages:
                if 'Body' in msg and 'ReceiptHandle' in msg:
                    self._cached_requests.append(WidgetRequest(msg['Body'], receipt_handle=msg['ReceiptHandle']))

        return self._cached_requests.pop()

    def delete_last(self, widget_request):
        # If the request comes from SQS, delete it from the queue
        if widget_request.receipt_handle is not None:
            self._sqs_client.delete_message(
                QueueUrl=self._queue_url,
                ReceiptHandle=widget_request.receipt_handle
            )
