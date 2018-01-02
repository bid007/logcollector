#importing src
#Author : Bidhya Nandan Sharma
#Date 12/20/2017
import sys
sys.path.append("./")
sys.path.append("../")
#added path 
from main import get_econfig_dict
import unittest

class TestEmailConfigReader(unittest.TestCase):

    def test_emailconfig(self):
        good = "test/goodconfig.ini"
        self.assertEqual(type(get_econfig_dict(good)),dict)
        bad = "test/badconfig.ini"
        with self.assertRaises(Exception):
            get_econfig_dict(bad)

if __name__ == '__main__':
    unittest.main()