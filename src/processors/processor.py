from abc import ABC, abstractmethod


class RequestProcessor(ABC):

    @abstractmethod
    def process(self, widget_request):
        pass
