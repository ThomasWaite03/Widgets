import unittest

from widgets.widget import Widget


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.id_a = 'idA'
        self.owner_a = 'owner A'
        self.label_a = 'Label A'
        self.description_a = 'Description A'
        self.widget_string_a = '[{"name": "name", "value": "john"}, {"name": "state", "value": "utah"}]'
        self.widget_a = Widget(self.id_a, self.owner_a, self.label_a, self.description_a, self.widget_string_a)

    def test_get_id(self):
        self.assertEqual(self.widget_a.get_id(), self.id_a)

    def test_get_owner(self):
        self.assertEqual(self.widget_a.get_owner(), self.owner_a)

    def test_get_label(self):
        self.assertEqual(self.widget_a.get_label(), self.label_a)

    def test_get_description(self):
        self.assertEqual(self.widget_a.get_description(), self.description_a)

    def test_to_string(self):
        self.assertEqual(self.widget_a.to_string(), self.widget_string_a)

    def test_get_other_attributes(self):
        other_attributes = self.widget_a.get_other_attributes()
        self.assertEqual(len(other_attributes), 2)
        if len(other_attributes) == 2:
            self.assertEqual(other_attributes[0].get_name(), 'name')
            self.assertEqual(other_attributes[0].get_value(), 'john')
            self.assertEqual(other_attributes[1].get_name(), 'state')
            self.assertEqual(other_attributes[1].get_value(), 'utah')


if __name__ == '__main__':
    unittest.main()
