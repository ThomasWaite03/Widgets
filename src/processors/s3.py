import boto3

from .processor import RequestProcessor


class S3RequestProcessor(RequestProcessor):
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3_client = boto3.client('s3')

    def _create_widget(self, widget_request):
        owner = widget_request.get_owner().replace(' ', '-').lower()
        widget_key = f'widgets/{owner}/{widget_request.get_widget_id()}'
        data = widget_request.get_widget().to_string().encode()
        self._s3_client.put_object(Bucket=self._bucket, Key=widget_key, Body=data)

    def _update_widget(self, widget_request):
        pass

    def _delete_widget(self, widget_request):
        pass
