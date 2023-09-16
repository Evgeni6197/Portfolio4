import unittest
import datetime

from .helper import *

class Tests(unittest.TestCase):

    def setUp(self):
        global d_t
        now = datetime.datetime.now()
        d_t = convert_datetime_format(now).split()

    def test0(self):
       self.assertTrue(d_t[0].isalpha())

    def test1(self):
        self.assertTrue(d_t[1][:-1].isnumeric())

    def test2(self):
        self.assertTrue(d_t[2][:-1].isnumeric())

if __name__ == '__main__':
    unittest.main()