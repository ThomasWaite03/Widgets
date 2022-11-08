import boto3
import logging
import botocore

from .processor import RequestProcessor
from widgets.widget import Widget


class S3RequestProcessor(RequestProcessor):
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3_client = boto3.client('s3')

    def _create_widget(self, widget_request):
        logging.info(f'Processing S3 create widget request for widget_id: {widget_request.get_widget_id()}')

        owner = widget_request.get_owner().replace(' ', '-').lower()
        widget_key = f'widgets/{owner}/{widget_request.get_widget_id()}'
        data = widget_request.get_widget().to_string().encode()
        self._s3_client.put_object(Bucket=self._bucket, Key=widget_key, Body=data)

    def _update_widget(self, widget_request):
        logging.info(f'Processing S3 update widget request for widget_id: {widget_request.get_widget_id()}')

        owner = widget_request.get_owner().replace(' ', '-').lower()
        widget_key = f'widgets/{owner}/{widget_request.get_widget_id()}'
        updated_info_widget = widget_request.get_widget()

        resp = None
        try:
            resp = self._s3_client.get_object(Key=widget_key, Bucket=self._bucket)
        except botocore.exceptions.ClientError as error:
            logging.warning('Widget cannot be updated, because it does not exist.')

        if resp is not None:
            widget_string = resp['Body'].read().decode('utf-8')
            original_widget = Widget(widget_string)

            if updated_info_widget.get_label() is not None:
                original_widget.set_label(updated_info_widget.get_label())

            if updated_info_widget.get_description() is not None:
                original_widget.set_description(updated_info_widget.get_description())

            for attr in updated_info_widget.get_other_attributes():
                if attr.get_value() == '':
                    original_widget.delete_other_attribute(attr.get_name())
                else:
                    original_widget.add_other_attribute(attr)

            data = original_widget.to_string().encode()
            self._s3_client.put_object(Bucket=self._bucket, Key=widget_key, Body=data)

    def _delete_widget(self, widget_request):
        pass
