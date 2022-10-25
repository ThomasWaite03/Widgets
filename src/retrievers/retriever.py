from abc import ABC, abstractmethod


class RequestRetriever(ABC):

    @abstractmethod
    def get_next(self):
        pass
