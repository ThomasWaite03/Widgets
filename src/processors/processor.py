from abc import ABC, abstractmethod


class RequestProcessor(ABC):

    def process(self, widget_request):
        if widget_request.get_type() == 'create':
            self._create_widget(widget_request)
        elif widget_request.get_type() == 'update':
            self._create_widget(widget_request)
        elif widget_request.get_type() == 'delete':
            self._delete_widget(widget_request)
        else:
            print('WARNING: Invalid request type.')

    @abstractmethod
    def _create_widget(self, widget_request):
        pass

    @abstractmethod
    def _update_widget(self, widget_request):
        pass

    @abstractmethod
    def _delete_widget(self, widget_request):
        pass
