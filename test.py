import unittest
from sep_chain_ht import MyHashTable

class TestData(unittest.TestCase):
    def test_MyHashTable_init(self):
        test_table = MyHashTable()
        self.assertAlmostEqual(test_table.hash_table,[[], [], [], [], [], [], [], [], [], [], []])
    def test_MyHashTable_insert(self):
        test_table = MyHashTable()
        test_table.insert(1,"cat")
        self.assertAlmostEqual(test_table.hash_table,[[], [(1, 'cat')], [], [], [], [], [], [], [], [], []])
    def test_MyHashTable_get(self):
        test_table = MyHashTable()
        test_table.insert(1,"cat")
        self.assertAlmostEqual(test_table.get(1),(1, 'cat'))
    def test_MyHashTable_remove(self):
        test_table = MyHashTable()
        test_table.insert(1,"cat")
        self.assertAlmostEqual(test_table.hash_table,[[], [(1, 'cat')], [], [], [], [], [], [], [], [], []])
        test_table.remove(1)
        self.assertAlmostEqual(test_table.hash_table,[[], [], [], [], [], [], [], [], [], [], []])
    def test_MyHashTable_size_loadfactor_collisionnumber(self):
        test_table = MyHashTable()
        test_table.insert(1,"cat")
        test_table.insert(4,"dog")
        test_table.insert(7,"caog")
        self.assertAlmostEqual(test_table.size(),3)
        self.assertAlmostEqual(test_table.load_factor(),0.272727272727)
        self.assertAlmostEqual(test_table.collisions(),0)
if __name__ == ("__main__"):
    unittest.main()
