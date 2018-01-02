#importing src
#Author : Bidhya Nandan Sharma
#Date 12/20/2017
import sys
sys.path.append("./")
sys.path.append("../")
#added path 
from config_reader import XmlToDict
import unittest

class TestXmlToDict(unittest.TestCase):

    def test_parse_valid(self):
        #test file for good case and its expected result
        test_file = "test/test.xml"
        result = {
            '192.168.2.1' : {'ip':'192.168.2.1', 'port':'22', 'username':'carnd', 'password':'carnd',
            'mail':'cbody@gmail.com', 'alerts':[{'type':'memory', 'limit':'10%'}, {'type':'cpu', 'limit':'20%'}]
            },
            '192.168.2.3' : {'ip':'192.168.2.3', 'port':'22', 'username':'carnd', 'password':'carnd',
            'mail':'bbody@gmail.com', 'alerts':[{'type':'memory', 'limit':'30%'}, {'type':'cpu', 'limit':'40%'}]
            }}
        self.assertEqual(XmlToDict(test_file).get_clients(), result)
        #test file for bad case and its expected result it keyError
        error_file = "test/error.xml"
        with self.assertRaises(KeyError):
            XmlToDict(error_file).get_clients()

if __name__ == '__main__':
    unittest.main()