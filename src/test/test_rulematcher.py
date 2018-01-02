#importing src
#Author : Bidhya Nandan Sharma
#Date 12/20/2017
import sys
sys.path.append("./")
sys.path.append("../")
#added path 
from rulematcher import RuleMatcher
import unittest

class TestRuleMatcher(unittest.TestCase):

    def test_match_1(self):
        log = "memory: 0.07%, cpu: 0.39%"
        #testing if both limit are crossed
        alert_rule = [{'type':'cpu', 'limit':'0%'},{'type':'memory', 'limit':'0%'}]
        self.assertEqual(RuleMatcher(log, alert_rule).matched,True)
        self.assertNotEqual(RuleMatcher(log, alert_rule).msg,[])
        #testing if only one limit is crossed
        alert_rule = [{'type':'cpu', 'limit':'90%'},{'type':'memory', 'limit':'0%'}]
        self.assertEqual(RuleMatcher(log, alert_rule).matched,True)
        self.assertNotEqual(RuleMatcher(log, alert_rule).msg,[])
        #testing if only one limit is crossed
        alert_rule = [{'type':'cpu', 'limit':'0%'},{'type':'memory', 'limit':'10%'}]
        self.assertEqual(RuleMatcher(log, alert_rule).matched,True)
        self.assertNotEqual(RuleMatcher(log, alert_rule).msg,[])
        #testing if none limit is crossed
        alert_rule = [{'type':'cpu', 'limit':'90%'},{'type':'memory', 'limit':'90%'}]
        self.assertEqual(RuleMatcher(log, alert_rule).matched,False)
        #testing if log is not in specified format
        #both alert won't be alarmed and msg would be empty
        log = "Something is wrong with the message"
        self.assertEqual(RuleMatcher(log, alert_rule).matched,False)

if __name__ == '__main__':
    unittest.main()

