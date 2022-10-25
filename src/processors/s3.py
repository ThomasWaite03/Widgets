from .processor import RequestProcessor


class S3RequestProcessor(RequestProcessor):
    def __init__(self, bucket):
        self.bucket = bucket

    def process(self, widget_request):
        print()
