import unittest

from widgets.widget import Widget


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.id = 'idA'
        self.owner = 'owner A'
        self.label = 'Label A'
        self.description = 'Description A'
        self.widget_string = '[{"name": "name", "value": "john"}, {"name": "state", "value": "utah"}]'
        self.widget = Widget(self.id, self.owner, self.label, self.description, self.widget_string)

    def test_get_id(self):
        self.assertEqual(self.widget.get_id(), self.id)

    def test_get_owner(self):
        self.assertEqual(self.widget.get_owner(), self.owner)

    def test_get_label(self):
        self.assertEqual(self.widget.get_label(), self.label)

    def test_get_description(self):
        self.assertEqual(self.widget.get_description(), self.description)

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


if __name__ == '__main__':
    unittest.main()
