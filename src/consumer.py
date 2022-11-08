import time
import logging

from context import get_strategies
from retrievers.sqs import SQSRequestRetriever


def main():
    # Set up logging configuration
    time_string = time.strftime('%m%d%Y%H%M%S')
    log_filename = f'./logs/consumer-log-{time_string}.txt'
    format_str = '%(asctime)s - %(message)s'
    logging.basicConfig(filename=log_filename, filemode='w', format=format_str, level=logging.INFO)

    # These 3 lines are from the logging module documentation and makes the logger print to the console
    # Source: https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    # Get the request retriever and request processor per the user's command line args
    request_retriever, request_processor = get_strategies()
    start_time = time.time()
    max_seconds = 30

    while time.time() - start_time < max_seconds:
        widget_request = request_retriever.get_next()
        if widget_request is None:
            time.sleep(0.1)
        else:
            request_processor.process(widget_request)
            if isinstance(request_retriever, SQSRequestRetriever):
                request_retriever.delete_last(widget_request)


if __name__ == "__main__":
    main()
