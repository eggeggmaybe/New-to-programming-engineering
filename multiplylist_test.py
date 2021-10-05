import unittest
from jsoncsvgenerator import multiplylist

lst = range(1, 11)

class TestUsermaker(unittest.TestCase):
    def test_length(self):
        # test if list length is equal to the input
        self.assertAlmostEqual(len(multiplylist(lst, 3)), 10)
        # test if the output is equal to the expected one
        self.assertAlmostEqual(multiplylist(lst, 3)[3], 12)
