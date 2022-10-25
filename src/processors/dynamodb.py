from .processor import RequestProcessor


class DynamoDBRequestProcessor(RequestProcessor):
    def __init__(self, table):
        self.table = table

    def process(self, widget_request):
        print()
