import unittest

from widgets.attribute import Attribute


class AttributeTestCase(unittest.TestCase):
    def setUp(self):
        self.name = 'exampleName'
        self.value = 'exampleValue'
        self.attribute = Attribute(self.name, self.value)

    def test_get_name(self):
        self.assertEqual(self.attribute.get_name(), self.name)

    def test_get_value(self):
        self.assertEqual(self.attribute.get_value(), self.value)


if __name__ == '__main__':
    unittest.main()
