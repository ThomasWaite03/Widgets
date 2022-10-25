from context import get_strategies


def main():
    request_retriever, request_processor = get_strategies()
    widget_request = request_retriever.get_next()


if __name__ == "__main__":
    main()
