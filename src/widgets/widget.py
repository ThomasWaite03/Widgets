import json

from .attribute import Attribute


class Widget:
    def __init__(self, widget_string):
        self._widget_string = widget_string
        widget_json = json.loads(widget_string)

        self._id = widget_json["widgetId"]
        self._owner = widget_json["owner"]

        if 'label' in widget_json and widget_json["label"] != '':
            self._label = widget_json["label"]
        else:
            self._label = None

        if 'description' in widget_json and widget_json["description"] != '':
            self._description = widget_json["description"]
        else:
            self._description = None

        # Create attribute objects for the "other attributes"
        self._other_attributes = []
        for other_attr in widget_json["otherAttributes"]:
            self._other_attributes += [Attribute(other_attr['name'], other_attr['value'])]

    def get_id(self):
        return self._id

    def get_owner(self):
        return self._owner

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

        widget_json = json.loads(self._widget_string)
        widget_json["label"] = label
        self._widget_string = json.dumps(widget_json)

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

        widget_json = json.loads(self._widget_string)
        widget_json["description"] = description
        self._widget_string = json.dumps(widget_json)

    def get_other_attributes(self):
        return self._other_attributes

    def add_other_attribute(self, attribute):
        self.delete_other_attribute(attribute.get_name())
        self._other_attributes += [attribute]

        widget_json = json.loads(self._widget_string)
        widget_json["otherAttributes"] += [
            {
                "name": attribute.get_name(),
                "value": attribute.get_value()
            }
        ]
        self._widget_string = json.dumps(widget_json)

    def delete_other_attribute(self, name):
        idx_to_delete = None
        for idx, attribute in enumerate(self._other_attributes):
            if attribute.get_name() == name:
                idx_to_delete = idx

        if idx_to_delete is not None:
            del(self._other_attributes[idx_to_delete])
            widget_json = json.loads(self._widget_string)
            del(widget_json["otherAttributes"][idx_to_delete])
            self._widget_string = json.dumps(widget_json)

    def to_string(self):
        return self._widget_string
