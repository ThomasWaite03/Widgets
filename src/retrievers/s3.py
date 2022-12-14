import boto3
import json
import logging

from .retriever import RequestRetriever
from widgets.request import WidgetRequest


class S3RequestRetriever(RequestRetriever):
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3_client = boto3.client('s3')

    def get_next(self):
        next_key_response = self._s3_client.list_objects(Bucket=self._bucket, MaxKeys=1)
        if 'Contents' in next_key_response:
            next_key = next_key_response['Contents'][0]['Key']
            obj_response = self._s3_client.get_object(Key=next_key, Bucket=self._bucket)
            obj_str = obj_response['Body'].read().decode('utf-8')

            # Delete object on S3 and then return a WidgetRequest
            self._s3_client.delete_object(Key=next_key, Bucket=self._bucket)

            if obj_str == '' or json.loads(obj_str)['widgetId'] == 'bad':
                logging.warning('Invalid widget request received from S3 bucket.')
                return None
            else:
                return WidgetRequest(obj_str)
        else:
            return None
