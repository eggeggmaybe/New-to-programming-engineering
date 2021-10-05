import unittest
from jsoncsvgenerator import usermaker

class TestUsermaker(unittest.TestCase):
    def test_length(self):
        # test if list length is equal to the input
        self.assertAlmostEqual(len(usermaker(100)), 100)
        self.assertAlmostEqual(len(usermaker(0)), 0)
    def test_type(self):
        # test if list elements are string type
        self.assertIsInstance(usermaker(100)[50], str)
