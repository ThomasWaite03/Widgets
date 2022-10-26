import boto3

from .processor import RequestProcessor


class DynamoDBRequestProcessor(RequestProcessor):
    def __init__(self, table):
        self._table = table
        self._dynamo_client = boto3.client('dynamodb')

    def _create_widget(self, widget_request):
        widget = widget_request.get_widget()

        item = {}
        for attribute in widget.get_other_attributes():
            item[attribute.get_name()] = {"S": attribute.get_value()}
        item["id"] = {"S": widget.get_id()}
        item["owner"] = {"S": widget.get_owner()}

        if widget.get_label() is not None:
            item["label"] = {"S": widget.get_label()}

        if widget.get_description() is not None:
            item["description"] = {"S": widget.get_description()}

        self._dynamo_client.put_item(TableName=self._table, Item=item)

    def _update_widget(self, widget_request):
        pass

    def _delete_widget(self, widget_request):
        pass
