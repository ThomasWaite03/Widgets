import time

from context import get_strategies


def main():
    request_retriever, request_processor = get_strategies()
    start_time = time.time()
    max_seconds = 30

    while time.time() - start_time < max_seconds:
        widget_request = request_retriever.get_next()
        if widget_request is None:
            time.sleep(0.1)
        else:
            request_processor.process(widget_request)


if __name__ == "__main__":
    main()
