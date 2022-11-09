import unittest
import json

from widgets.widget import Widget
from widgets.attribute import Attribute


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.id = 'idA'
        self.owner = 'owner A'
        self.label = 'Label A'
        self.description = 'Description A'

        widget_obj = {
            'widgetId': self.id,
            'owner': self.owner,
            'label': self.label,
            'description': self.description,
            'otherAttributes': [
                {"name": "name", "value": "john"},
                {"name": "state", "value": "utah"}
            ]
        }
        self.widget_string = json.dumps(widget_obj)
        self.widget = Widget(self.widget_string)

    def test_get_id(self):
        self.assertEqual(self.widget.get_id(), self.id)

    def test_get_owner(self):
        self.assertEqual(self.widget.get_owner(), self.owner)

    def test_get_label(self):
        self.assertEqual(self.widget.get_label(), self.label)

    def test_set_label(self):
        new_label = 'new label!'
        self.widget.set_label(new_label)
        self.assertEqual(self.widget.get_label(), new_label)

    def test_get_description(self):
        self.assertEqual(self.widget.get_description(), self.description)

    def test_set_description(self):
        new_description = 'new description!'
        self.widget.set_description(new_description)
        self.assertEqual(self.widget.get_description(), new_description)

    def test_to_string(self):
        self.assertEqual(self.widget.to_string(), self.widget_string)

    def test_get_other_attributes(self):
        other_attributes = self.widget.get_other_attributes()
        self.assertEqual(len(other_attributes), 2)
        if len(other_attributes) == 2:
            self.assertEqual(other_attributes[0].get_name(), 'name')
            self.assertEqual(other_attributes[0].get_value(), 'john')
            self.assertEqual(other_attributes[1].get_name(), 'state')
            self.assertEqual(other_attributes[1].get_value(), 'utah')

    def test_add_other_attribute(self):
        new_attribute = Attribute('height', '6 ft')
        self.widget.add_other_attribute(new_attribute)

        attribute_added = False
        for attr in self.widget.get_other_attributes():
            if attr.get_name() == new_attribute.get_name() and attr.get_value() == new_attribute.get_value():
                attribute_added = True
        self.assertTrue(attribute_added)

    def test_delete_other_attribute(self):
        attribute_name_to_delete = 'state'
        self.widget.delete_other_attribute(attribute_name_to_delete)

        attribute_present = False
        for attr in self.widget.get_other_attributes():
            if attr.get_name() == attribute_name_to_delete:
                attribute_present = True
        self.assertFalse(attribute_present)


if __name__ == '__main__':
    unittest.main()
