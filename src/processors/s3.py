import boto3

from .processor import RequestProcessor


class S3RequestProcessor(RequestProcessor):
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3_client = boto3.client('s3')

    def process(self, widget_request):
        if widget_request.get_type() == 'create':
            self.__create_widget(widget_request)
        elif widget_request.get_type() == 'update':
            self.__create_widget(widget_request)
        elif widget_request.get_type() == 'delete':
            self.__delete_widget(widget_request)
        else:
            print('WARNING: Invalid request type.')

    def __create_widget(self, widget_request):
        widget_key = f'widgets/{widget_request.get_owner()}/{widget_request.get_widget_id()}'
        data = widget_request.get_widget().to_string().encode()
        self._s3_client.put_object(Bucket=self._bucket, Key=widget_key, Body=data)

    def __update_widget(self, widget_request):
        pass

    def __delete_widget(self, widget_request):
        pass
