import unittest
from table import HashTable


class Matrix1(unittest.TestCase):
    def setUp(self):
        self.table = HashTable(25)

    def test_insert(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        self.table.insert("key3", "value3")

        self.assertEqual("value2", self.table.search("key2"))

    def test_update(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        self.table.insert("key3", "value3")
        self.table.update("key2", "new_value2")

        self.assertEqual("new_value2", self.table.search("key2"))

    def test_delete(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        self.table.insert("key3", "value3")
        self.table.delete("key2")

        self.assertEqual(None, self.table.search("key2"))

    def test_many_items(self):
        for i in range(10):
            self.table.insert(str(i), i)

        self.assertEqual(None, self.table.search("25"))

    def test_str(self):
        for i in range(25):
            self.table.insert(str(i), i)

        self.table.delete('10')

        self.assertEqual(None, self.table.search("10"))



if __name__ == "__main__":
    unittest.main()
