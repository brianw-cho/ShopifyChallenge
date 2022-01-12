import unittest
from item_manager import ItemManager

manager = ItemManager()

class TestItemManager(unittest.TestCase):

    def test_create_item(self):
        manager.create_item("Apple", "1234", 5)
        self.assertTrue(manager.contains("1234"))

    def test_delete_item(self):
        manager.create_item("Orange", "5678", 3)
        manager.delete_item("5678")
        self.assertFalse(manager.contains("5678"))

    def test_set_num(self):
        manager.create_item("Bananas", "5823", 6)
        manager.set_num("5823", 9)
        self.assertEqual(manager.get_num("5823"), 9)