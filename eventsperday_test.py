import unittest
from jsoncsvgenerator import eventsperday
import statistics

class TestUsermaker(unittest.TestCase):
    def test_length(self):
        # test if list length is equal to the input
        self.assertAlmostEqual(len(eventsperday(5,1,500)), 500)
        # test if mean is equal to the input mean
        # +1 because everything in the returned list is applied int() which takes floor value)
        # int() because function output list contains integers only (int() used in the function when output)
        self.assertAlmostEqual(int(statistics.mean(eventsperday(5, 1, 500)) + 1), 5)
        # test if standard deviation is equal to the input standard deviation
        self.assertAlmostEqual(int(statistics.stdev(eventsperday(5, 1, 500))), 1)
