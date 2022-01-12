import unittest
import item

item1 = item.Item("Apple", "1234")
item2 = item.Item("Banana", "5678")
item3 = item.Item("Rotten Apple", "1234")

class TestItem(unittest.TestCase):

    def test_get_name(self):
        self.assertEqual(item1.get_name(), "Apple")
        self.assertEqual(item2.get_name(), "Banana")
        self.assertEqual(item3.get_name(), "Rotten Apple")

    def test_get_id(self):
        self.assertEqual(item1.get_id(), "1234")
        self.assertEqual(item2.get_id(), "5678")
        self.assertEqual(item3.get_id(), "1234")

    def test_is_same_item(self):
        self.assertFalse(item1.is_same_item(item2.get_id()))
        self.assertTrue(item1.is_same_item(item3.get_id()))