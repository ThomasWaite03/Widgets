import json

from .widget import Widget


class WidgetRequest:
    def __init__(self, json_request, receipt_handle=None):
        self._json_request = json_request
        request = json.loads(json_request)
        self._type = request['type']
        self._request_id = request['requestId']
        self._widget_id = request['widgetId']
        self._owner = request['owner']
        self.receipt_handle = receipt_handle

    def get_type(self):
        return self._type

    def get_request_id(self):
        return self._request_id

    def get_widget_id(self):
        return self._widget_id

    def get_owner(self):
        return self._owner

    def get_widget(self):
        request = json.loads(self._json_request)
        del(request["type"])
        del(request["requestId"])

        widget_string = json.dumps(request)
        return Widget(widget_string)
