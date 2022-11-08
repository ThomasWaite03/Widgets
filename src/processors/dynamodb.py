import boto3
import botocore
import logging

from .processor import RequestProcessor


class DynamoDBRequestProcessor(RequestProcessor):
    def __init__(self, table):
        self._table = table
        self._dynamo_client = boto3.client('dynamodb')

    def _create_widget(self, widget_request):
        logging.info(f'Processing DynamoDB create widget request for widget_id: {widget_request.get_widget_id()}')

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
        logging.info(f'Processing DynamoDB update widget request for widget_id: {widget_request.get_widget_id()}')
        updated_info_widget = widget_request.get_widget()

        # Query the DynamoDB table
        resp = self._dynamo_client.query(
            TableName=self._table,
            ExpressionAttributeValues={
                ':id': {
                    'S': updated_info_widget.get_id()
                }
            },
            KeyConditionExpression='id = :id'
        )

        if resp['Count'] == 0:
            logging.warning('Widget cannot be updated, because it does not exist.')
        else:
            # Prepare values for boto3 update command
            attr_names = {}
            attr_values = {}
            attr_to_delete = []
            update_string = "SET "
            for idx, attr in enumerate(updated_info_widget.get_other_attributes()):
                attr_names[f"#ATTR{idx}"] = attr.get_name()
                if attr.get_value() == '':
                    attr_to_delete += [f"#ATTR{idx}"]
                else:
                    attr_values[f":v{idx}"] = {
                        "S": attr.get_value()
                    }
                    update_string += f"#ATTR{idx} = :v{idx}, "
            update_string = update_string[:-2]

            # Update the label if necessary
            if updated_info_widget.get_label() is not None:
                attr_names["#ATTR_LABEL"] = "label"
                attr_values[f":v_label"] = {
                    "S": updated_info_widget.get_label()
                }
                update_string += ", #ATTR_LABEL = :v_label"

            # Update the description if necessary
            if updated_info_widget.get_description() is not None:
                attr_names["#ATTR_DESCR"] = "description"
                attr_values[f":v_descr"] = {
                    "S": updated_info_widget.get_description()
                }
                update_string += ", #ATTR_DESCR = :v_descr"

            # Add the attributes to delete to the update string if there are any
            if len(attr_to_delete) > 0:
                update_string += " REMOVE " + ", ".join(attr_to_delete)

            # Replace attributes if they exist, otherwise add them to the item
            self._dynamo_client.update_item(
                TableName=self._table,
                Key={
                    "id": {
                        "S": updated_info_widget.get_id()
                    }
                },
                ExpressionAttributeNames=attr_names,
                ExpressionAttributeValues=attr_values,
                UpdateExpression=update_string
            )

    def _delete_widget(self, widget_request):
        logging.info(f'Processing DynamoDB delete widget request for widget_id: {widget_request.get_widget_id()}')

        # Query the table to see if the widget exists
        resp = self._dynamo_client.query(
            TableName=self._table,
            ExpressionAttributeValues={
                ':id': {
                    'S': widget_request.get_widget_id()
                }
            },
            KeyConditionExpression='id = :id'
        )

        if resp['Count'] == 0:
            logging.warning('Widget cannot be deleted, because it does not exist.')
        else:
            # Delete the widget item from the table
            self._dynamo_client.delete_item(
                TableName=self._table,
                Key={
                    'id': {
                        'S': widget_request.get_widget_id()
                    }
                }
            )
