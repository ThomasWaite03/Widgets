import json

from .attribute import Attribute


class Widget:
    def __init__(self, widget_id, owner, label, description, widget_string):
        self._id = widget_id
        self._owner = owner
        self._label = label
        self._description = description
        self._widget_string = widget_string

        # Create attribute objects for the "other attributes"
        self._other_attributes = []
        for other_attr in json.loads(widget_string):
            self._other_attributes += [Attribute(other_attr['name'], other_attr['value'])]

    def get_id(self):
        return self._id

    def get_label(self):
        return self._label

    def get_description(self):
        return self._description

    def get_owner(self):
        return self._owner

    def get_other_attributes(self):
        return self._other_attributes

    def to_string(self):
        return self._widget_string
