import boto3

from .retriever import RequestRetriever


class SQSRequestRetriever(RequestRetriever):
    def __init__(self, queue):
        self._queue = queue
        self._sqs_client = boto3.client('sqs')

    def get_next(self):
        pass
